# -*- coding: utf-8 -*-
# @Time : 2021/12/27 0027 13:50
# @Author : Bobby_Liukeling
# @File : load_npy.py

import numpy as np

path = "last_data/all_nparry.npy"
# data = np.load(path,allow_pickle=True)

a = 1

# s  = /home/xiaoming/Cynthia -q MCDB/static/data/ccompare/temp/'+randname + '.mol2 -t  MCDB/static/data/ccompare/all.mol2 -o MCDB/static/data/ccompare/temp/'+randname+' -n 300 -sCutoff 1'

s = "obabel dsgdb9nsd_{}.xyz -ixyz -opdb -O {}/dsgdb9nsd_{}.pdb"
#obabel dsgdb9nsd_000003.pdb -O A.sdf   #将pdb文件转化为sdf文件

#obabel 4cpa.pdb -O A.mol2
#obabel 121p.pdb -O B.mol2
#shaep -q B.mol2 A.mol2 -s out.sdf similarity.txt

#Cynthia -q A.sdf -t B.sdf -o output

from chembl_webresource_client.new_client import new_client

print(new_client.target)

# s = ChEMBL ID;"Name";"Synonyms";"Type";"Max Phase";"Molecular Weight";"Targets";"Bioactivities";"AlogP";"Polar Surface Area";"HBA";"HBD";"#RO5 Violations";"#Rotatable Bonds";"Passes Ro3";"QED Weighted";"CX Acidic pKa";"CX Basic pKa";"CX LogP";"CX LogD";"Aromatic Rings";"Structure Type";"Inorganic Flag";"Heavy Atoms";"HBA (Lipinski)";"HBD (Lipinski)";"#RO5 Violations (Lipinski)";"Molecular Weight (Monoisotopic)";"Molecular Species";"Molecular Formula";"Smiles"
# b = CHEMBL3989817;"DIPROLEANDOMYCIN";"DIPROLEANDOMYCIN";"Small molecule";"0";"800.00";"";"";"3.83";"178.12";"15";"1";"2";"10";"N";"0.19";"12.83";"8.38";"5.26";"4.24";"0";"MOL";"0";"56";"15";"1";"2";"799.4718";"NEUTRAL";"C41H69NO14";"CCC(=O)O[C@H]1[C@H](C)O[C@@H](O[C@@H]2[C@@H](C)C(=O)O[C@H](C)[C@H](C)[C@H](OC(=O)CC)[C@@H](C)C(=O)[C@]3(CO3)C[C@H](C)[C@H](O[C@@H]3O[C@H](C)C[C@H](N(C)C)[C@H]3O)[C@H]2C)C[C@@H]1OC"
