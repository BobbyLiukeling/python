# -*- coding: utf-8 -*-
# @Time : 2021/10/12 0012 8:51
# @Author : Bobby_Liukeling
# @File : MultiConf.py
# -*- coding: utf-8 -*-

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem.Draw.MolDrawing import MolDrawing, DrawingOptions
import pdb

import pickle
from rdkit.Chem import PyMol
times = 5 #构象次数
# smi = "CCCCC[C@H](O)/C=C/[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C/C=C\CCC[C]([O-])O"
smi = "CCCCC[C@H](O)/C=C/[C@@H]1[C@@H](C/C=C\CCCC(O)=O)[C@@H]2C[C@H]1OO2"
ibuH = Chem.MolFromSmiles(smi)

ibuH = Chem.AddHs(ibuH,explicitOnly=False)
# ibuH = pickle.load(open('../ibuH.pkl','rb'))

cids = AllChem.EmbedMultipleConfs(ibuH,
                                  clearConfs=True,
                                  numConfs=times,
                                  pruneRmsThresh=1)

for cid in cids:
    # pdb.set_trace()
    AllChem.MMFFOptimizeMolecule(ibuH,confId=cid)

for i in range(len(cids)):
    conf = ibuH.GetConformer(i)
    conf.GetPositions()
    pdb.set_trace()



v= PyMol.MolViewer()
v.DeleteAll()
for cid in cids:
    v.ShowMol(ibuH,confId=cid,name='Conf-%d'%cid,showOnly=False)
v.server.do('set grid_mode, on')

v.server.do('ray')
v.GetPNG()



# pdb.set_trace()