# -*- coding: utf-8 -*-
# @Time : 2021/10/10 0010 10:23
# @Author : Bobby_Liukeling
# @File : QM9_download.py

from rdkit import Chem
from rdkit.Chem import AllChem
# from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import PyMol
import pickle
import pdb
from rdkit.Chem import Draw
import numpy as np
times = 10
smi = 'CCCCC[C@H](O)/C=C/[C@@H]1[C@@H](C/C=C\CCCC(O)=O)[C@@H]2C[C@H]1OO2'
mol = Chem.MolFromSmiles(smi)

mol2 = Chem.MolFromMolFile('foo.mol')

mol1 = mol
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol)
AllChem.MMFFOptimizeMolecule(mol)
mol2 = mol
cids = AllChem.EmbedMultipleConfs(mol, numConfs=times)
# pdb.set_trace()

# mol.GetConformer(1)  # 访问指定构象
# mol.GetConformers()  # 获取构象

# conf = mol.GetConformer(0)
# for i, (x,y,z) in enumerate(conf.GetPositions()[:10]):
#     atom = mol.GetAtomWithIdx(i)
#     print('{}\tx: {:.2f}\ty: {:.2f}\tz: {:.2f}'.format(atom.GetSymbol(),x,y,z))

# mols = []
# for i in range(times):
#     print('*'*10)
#     conf = mol.GetConformer(i)
    # props = conf.GetPropsAsDict()
    # print(mol.GetConformer(i).GetPositions()[1])  # 访问指定构象
    # print()  # 访问指定构象
    # pdb.set_trace()
    # mol.GetConformers()  # 获取构象
    # mols.append(mol)
# print(mol.GetConformers())

img = Draw.MolsToGridImage([mol,mol2],legends=['test1','test2'],subImgSize=(600,600))
img.show()

#rmslist 包含第一个符合者和所有其他人之间的 RMS 值。也可以计算两个特定构象异构体（例如 1 和 9）之间的 RMS。
# rmslist = []
# AllChem.AlignMolConformers(mol, RMSlist=rmslist)
# mols = []
# smils = []
# for i in range(len(cids)):
#     mols.append(mol.GetConformer(id=i))

    # smils.append(Chem.MolToSmiles(mol.GetConformer(id=i), doRandom=True))

# pdb.set_trace()


# img = Draw.MolsToGridImage([mol.GetConformer(id=x) for x in range(10)],
#                      legends=[str(penalized_logP(s)) for s in sampled_valid])

# img = Draw.MolsToGridImage(mols)
# img.show()
# img.save('test.png')


def generate_structure_from_smiles(smiles):

    # Generate a 3D structure from smiles

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)

    status = AllChem.EmbedMolecule(mol)
    status = AllChem.UFFOptimizeMolecule(mol)

    conformer = mol.GetConformer()
    coordinates = conformer.GetPositions()
    coordinates = np.array(coordinates)

    atoms = get_atoms(mol)

    return atoms, coordinates

def get_atoms(mol):
    atoms = [a.GetAtomicNum() for a in mol.GetAtoms()]
    return atoms



mol = generate_structure_from_smiles(smi)

pdb.set_trace()