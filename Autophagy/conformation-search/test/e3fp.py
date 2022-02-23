# -*- coding: utf-8 -*-
# @Time : 2021/10/19 0019 15:32
# @Author : Bobby_Liukeling
# @File : e3fp.py

import sys,os,pdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
sys.path.append(BASE_DIR)
print(sys.path)
pdb.set_trace()

fprint_params = {'bits': 4096, 'radius_multiplier': 1.5, 'rdkit_invariants': True}
confgen_params = {'max_energy_diff': 20.0, 'first': 3}
smiles = "COC(=O)C(C1CCCCN1)C2=CC=CC=C2"
from e3fp.pipeline import confs_from_smiles
mol = confs_from_smiles(smiles, "ritalin", confgen_params=confgen_params)
mol.GetNumConformers()