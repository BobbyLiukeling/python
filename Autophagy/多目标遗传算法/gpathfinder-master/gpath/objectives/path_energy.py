#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############
# GPathFinder: Identification of ligand pathways by a multi-objective
# genetic algorithm
# 
# https://github.com/insilichem/gpathfinder
#
# Copyright 2019 José-Emilio Sánchez Aparicio, Giuseppe Sciortino,
# Daniel Villadrich Herrmannsdoerfer, Pablo Orenes Chueca, 
# Jaime Rodríguez-Guerra Pedregal and Jean-Didier Maréchal
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############

"""
This objective is a wrapper around OpenMM, providing a GPU-accelerated energy
calculation of the system with a simple forcefield evaluation.
"""

# Python
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import os
import logging
# 3rd party
from Molecule import atom_positions
import simtk.openmm.app as openmm_app
from simtk import unit, openmm
from mdtraj import Topology as MDTrajTopology
from openmoltools.amber import run_antechamber
from openmoltools.utils import create_ffxml_file
import numpy
# GPATH
from gpath import parse
from gpath.objectives import ObjectiveProvider

logger = logging.getLogger(__name__)
_openmm_builtin_forcefields = os.listdir(os.path.join(openmm_app.__path__[0], 'data'))

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def enable(**kwargs):
    kwargs = Energy.validate(kwargs)
    return Energy(**kwargs)


class Energy(ObjectiveProvider):

    """
    Calculate the energy of a system
    
    Parameters
    ----------
    targets : list of str, default=None
        If set, which molecules should be evaluated. Else, all will be evaluated.
    forcefields : list of str, default=('amber99sbildn.xml',)
        Which forcefields to use
    auto_parametrize: list of str, default=None
        List of Molecule instances GPATH should try to auto parametrize with antechamber.
    parameters : list of 2-item list of str
        List of (gaff.mol2, .frcmod) files to use as parametrization source.
    platform : str
        Which platform to use for calculations. Choose between CPU, CUDA, OpenCL.
    minimize : bool
        Whether to minimize the structure or not. Only valid when one target is chosen.
    minimization_tolerance : float, optional=10
        Convergence criteria for energy minimization. In kJ/mol.
    minimization_iterations : int, optional=10
        Max attempts to converge at minimization.
    frozen_atoms : str
        MDTraj DSL query that will select atoms to be froze; e.g., ``backbone``
    system_options : dict
        Key-value options that will be passed to ``.createSystem()`` calls. Useful
        for implicit solvent declaration, custom non bonded methods, and so on.
    Returns
    -------
    float
        The estimated potential energy, in kJ/mol
    """

    _validate = {
        'targets': [parse.Molecule_name],
        'forcefields': [parse.Any(parse.ExpandUserPathExists, parse.In(_openmm_builtin_forcefields))],
        'auto_parametrize': [parse.Molecule_name],
        'parameters': [parse.All([parse.ExpandUserPathExists], parse.Length(min=2, max=2))],
        'platform': parse.In(['CUDA', 'OpenCL', 'CPU']),
        'minimize': parse.Coerce(bool),
        'minimization_tolerance': float,
        'minimization_iterations': int,
        'frozen_atoms': parse.Any(None, parse.Coerce(str)),
        'system_options': parse.Any(dict, None)
        }

    def __init__(self, targets=None, forcefields=('amber99sbildn.xml',),
                 auto_parametrize=None, parameters=None, platform=None,
                 minimize=False, minimization_tolerance=10, minimization_iterations=10,
                 system_options=None, frozen_atoms=None, *args, **kwargs):
        if kwargs.get('precision', 6) < 6:
            kwargs['precision'] = 6
        ObjectiveProvider.__init__(self, **kwargs)
        self.auto_parametrize = auto_parametrize
        self.minimize = minimize
        self.minimization_tolerance = minimization_tolerance
        self.minimization_iterations = minimization_iterations
        self.frozen_atoms = frozen_atoms
        self.system_options = {'nonbondedMethod': openmm_app.CutoffNonPeriodic,
                               'nonbondedCutoff': 1.0*unit.nanometers,
                               'rigidWater': True, 'constraints': None}
        if system_options:
            self.system_options.update(self._prepare_system_options(system_options))
        self._targets = targets
        self._parameters = parameters
        self.platform = platform
        self.topology = None
        self._simulation = None
        self._state = None

        if len(forcefields) == 1 and forcefields[0].endswith('.prmtop'):
            self.forcefield = openmm_app.AmberPrmtopFile(forcefields[0])
            self.topology = self.forcefield.topology
        else:
            additional_ffxml = []
            if parameters:
                additional_ffxml.append(create_ffxml_file(*zip(*parameters)))
            if auto_parametrize:
                filenames = [g.path for m in auto_parametrize
                            for g in self.environment.cfg.genes
                            if g.name == m]
                additional_ffxml.append(self._gaff2xml(*filenames))

            self._forcefields = tuple(forcefields) + tuple(additional_ffxml)

            self.forcefield = openmm_app.ForceField(*self._forcefields)

    def evaluate(self, individual):
        """
        Calculates the energy of current individual
        Notes
        -----
        For static calculations, where molecules are essentially always the same,
        but with different coordinates, we only need to generate topologies once.
        However, for dynamic jobs, with potentially different molecules involved
        each time, we cannot guarantee having the same topology. As a result,
        we generate it again for each evaluation.
        """
        molecules = self.molecules(individual)
        coordinates = self.chimera_molecule_to_openmm_positions(*molecules)

        # Build topology if it's first time or a dynamic job
        if self.topology is None or not self._gpath_is_static(individual):
            self.topology = self.chimera_molecule_to_openmm_topology(*molecules)
            self._simulation = None  # This forces a Simulation rebuild

        return self.calculate_energy(coordinates)

    def molecules(self, individual):
        if self._targets is None:
            return [m.compound.mol for m in individual._molecules.values()]
        else:
            return [individual.find_molecule(t).compound.mol for t in self._targets]

    @property
    def simulation(self):
        """
        Build a new OpenMM simulation if not yet defined and return it
        Notes
        -----
        self.topology must be defined previously! (Only with XML force fields)
        Use self.chimera_molecule_to_openmm_topology to set it.
        """
        if self._simulation is None:
            if isinstance(self.forcefield, openmm_app.ForceField):
                args = (self.topology,)
            else:
                args = ()
            system = self.forcefield.createSystem(*args, **self.system_options)
            if self.frozen_atoms:
                for i in self._subset():
                    system.setParticleMass(i, 0.0)  # This freezes the particle

            integrator = openmm.VerletIntegrator(0.001)
            if self.platform is not None:
                platform = openmm.Platform.getPlatformByName(self.platform),
            else:
                platform = ()
            self._simulation = openmm_app.Simulation(self.topology, system, integrator, *platform)
        return self._simulation

    def minimize_energy(self, molecules, individual):
        """
        Set up an OpenMM simulation with default parameters
        and make a minimization of the target molecules

        Parameters
        ----------
        molecule : list of chimera.Molecule
        individual : gpath.base.Individual
            The individual to be analyzed for dynamic behaviour
        Returns
        -------
        positions : simtk.unit.Quantity
            Positions of the atoms in the minimized system
        potential_energy : float
            Potential energy of the system, in kJ/mol
        """
        coordinates = self.chimera_molecule_to_openmm_positions(*molecules)

        # Build topology if it's first time or a dynamic job
        if self.topology is None or not self._gpath_is_static(individual):
            self.topology = self.chimera_molecule_to_openmm_topology(*molecules)
            self._simulation = None  # This forces a Simulation rebuild
        self.simulation.context.setPositions(coordinates)

        self.simulation.minimizeEnergy(
                tolerance=self.minimization_tolerance*unit.kilojoule_per_mole,
                maxIterations=self.minimization_iterations)
        # Retrieve positions and energy of the minimized system
        self._state = self.simulation.context.getState(getPositions=True, getEnergy=True)
        return self._state.getPositions()/unit.angstrom, self._state.getPotentialEnergy()._value

    def calculate_energy(self, coordinates):
        """
        Set up an OpenMM simulation with default parameters
        and return the potential energy of the initial state
        Parameters
        ----------
        coordinates : simtk.unit.Quantity
            Positions of the atoms in the system
        Returns
        -------
        potential_energy : float
            Potential energy of the system, in kJ/mol
        """
        self.simulation.context.setPositions(coordinates)
        if self.minimize:
            self.simulation.minimizeEnergy(
                tolerance=self.minimization_tolerance*unit.kilojoule_per_mole,
                maxIterations=self.minimization_iterations)
        # Retrieve energy
        self._state = self.simulation.context.getState(getEnergy=True, getPositions=True)
        return self._state.getPotentialEnergy()._value

    @staticmethod
    def chimera_molecule_to_openmm_topology(*molecules):
        """
        Convert a Chimera Molecule object to OpenMM structure,
        providing topology and coordinates.
        Parameters
        ----------
        molecule : chimera.Molecule
        Returns
        -------
        topology : simtk.openmm.app.topology.Topology
        coordinates : simtk.unit.Quantity
        """
        # Create topology

        atoms, residues, chains = {}, {}, {}
        topology = openmm_app.Topology()
        for i, mol in enumerate(molecules):
            for a in mol.atoms:
                chain_id = (i, a.residue.id.chainId)
                try:
                    chain = chains[chain_id]
                except KeyError:
                    chain = chains[chain_id] = topology.addChain()

                r = a.residue
                try:
                    residue = residues[r]
                except KeyError:
                    residue = residues[r] = topology.addResidue(r.type, chain)
                name = a.name
                element = openmm_app.Element.getByAtomicNumber(a.element.number)
                serial = a.serialNumber
                atoms[a] = topology.addAtom(name, element, residue, serial)

            for b in mol.bonds:
                topology.addBond(atoms[b.atoms[0]], atoms[b.atoms[1]])

        return topology

    @staticmethod
    def chimera_molecule_to_openmm_positions(*molecules):
        # Get positions
        positions = [atom_positions(m.atoms) for m in molecules]
        all_positions = numpy.concatenate(positions)
        return unit.Quantity(all_positions, unit=unit.angstrom)

    @staticmethod
    def _gaff2xml(*filenames, **kwargs):
        """
        Use OpenMolTools wrapper to run antechamber programatically
        and auto parametrize requested molecules.
        Parameters
        ----------
        filenames: list of str
            List of the filenames of the molecules to parametrize
        Returns
        -------
        ffxmls : StringIO
            Compiled ffxml file produced by antechamber and openmoltools converter
        """
        frcmods, gaffmol2s = [], []
        for filename in filenames:
            name = '.'.join(filename.split('.')[:-1])
            gaffmol2, frcmod = run_antechamber(name, filename, **kwargs)
            frcmods.append(frcmod)
            gaffmol2s.append(gaffmol2)
        return create_ffxml_file(gaffmol2s, frcmods)

    def _gpath_is_static(self, individual):
        """
        Check if this essay is performing topology changes.
        Genes that can change topologies:
            - gpath.genes.rotamers with mutations ON
            - gpath.genes.molecule with block building enabled
        Parameters
        ----------
        individual : gpath.base.Individual
            The individual to be analyzed for dynamic behaviour
        Returns
        -------
        bool
        """
        for gene in individual.genes.values():
            if gene.__class__.__name__ == 'Mutamers':
                if gene.mutations:
                    return False
            if gene.__class__.__name__ == 'Molecule':
                if len(gene.catalog) > 1:
                    return False

        return True

    def _prepare_system_options(self, mapping):
        if not mapping:
            return mapping
        for key, value in mapping.items():
            if key in ('implicitSolvent', 'nonbondedMethod'):
                mapping[key] = getattr(openmm_app, value)
        return mapping

    def _subset(self, query=None):
        if query is None:
            query = self.frozen_atoms
        if query:
            mdtop = MDTrajTopology.from_openmm(self.topology)
            return mdtop.select(query)
        return []


def calculate_energy(filename, forcefields=None):
    """
    Calculate energy from PDB file with desired forcefields. If not specified,
    amber99sbildn will be used. Returns potential energy in kJ/mol.
    """
    if not forcefields:
        forcefields = ['amber99sbildn.xml']

    mol = openmm_app.PDBFile(filename)
    ff = openmm_app.ForceField(*forcefields)
    system = ff.createSystem(mol.topology,
                             nonbondedMethod=openmm_app.CutoffNonPeriodic,
                             nonbondedCutoff=1.0*unit.nanometers,
                             rigidWater=True, constraints=None)
    integrator = openmm.VerletIntegrator(0.001)
    sim = openmm_app.Simulation(mol.topology, system, integrator)
    sim.context.setPositions(mol.positions)
    state = sim.context.getState(getEnergy=True)
    potential_energy = state.getPotentialEnergy()

    return potential_energy._value


def _test_topology_equality(t1, t2):
    """
    Test if two topologies are identical
    Parameters
    ----------
    t1, t2 : simtk.openmm.app.topology.Topology
    Returns
    -------
    bool
    Notes
    -----
    Ripped straight from ``mdtraj.core.topology.__eq__``. It might be slow, though.
    """
    if not isinstance(t1, openmm_app.topology.Topology):
        return False
    if not isinstance(t2, openmm_app.topology.Topology):
        return False

    if t1 is t2:
        return True

    if len(t1._chains) != len(t2._chains):
        return False

    for c1, c2 in zip(t1.chains(), t2.chains()):
        if c1.index != c2.index:
            return False
        if len(c1._residues) != len(c2._residues):
            return False

        for r1, r2 in zip(c1.residues(), c2.residues()):
            if (r1.index != r1.index) or (r1.name != r2.name):  # or (r1.resSeq != r2.resSeq):
                return False
            if len(r1._atoms) != len(r2._atoms):
                return False

            for a1, a2 in zip(r1.atoms(), r2.atoms()):
                if (a1.index != a2.index) or (a1.name != a2.name):
                    return False
                if a1.element is not None and a2.element is not None:
                    if a1.element != a2.element:
                        return False
                    # for attr in ['atomic_number', 'name', 'symbol']:
                    #    if getattr(a1.element, attr) != getattr(a2.element, attr):
                    #        return False

    if len(t1._bonds) != len(t2._bonds):
        return False

    # the bond ordering is somewhat ambiguous, so try and fix it for comparison
    t1_sorted_bonds = sorted([(a1.index, b1.index) for (a1, b1) in t1.bonds()])
    t2_sorted_bonds = sorted([(a2.index, b2.index) for (a2, b2) in t2.bonds()])

    for i in range(len(t1._bonds)):
        (a1, b1) = t1_sorted_bonds[i]
        (a2, b2) = t2_sorted_bonds[i]
        if (a1 != a2) or (b1 != b2):
            return False

    return True

if __name__ == "__main__":
    import sys
    print(calculate_energy(sys.argv[1], forcefields=sys.argv[2:]))