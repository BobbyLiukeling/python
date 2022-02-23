# -*- coding: utf-8 -*-
# @Time : 2021/10/10 0010 20:05
# @Author : Bobby_Liukeling
# @File : torsion.py

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem.Draw.MolDrawing import MolDrawing, DrawingOptions
import pickle
from rdkit.Chem import PyMol
from rdkit.Chem import Draw
import pdb

mol = Chem.MolFromMol2File('test.mol2')
# print(Chem.MolToSmiles(mol))
# mol = Chem.AddHs(mol)
# AllChem.EmbedMolecule(mol)
# AllChem.MMFFOptimizeMolecule(mol)

# img = Draw.MolsToGridImage([mol,],legends=['test',],subImgSize=(600,600))
# img.show()
pdb.set_trace()

