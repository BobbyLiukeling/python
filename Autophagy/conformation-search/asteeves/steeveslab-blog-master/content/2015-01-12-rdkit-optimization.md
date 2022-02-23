Title: Force-field optimization of molecules in RDKit
Date: 2015-01-12 12:00
Category: IPython notebook
Tags: python, notebook, rdkit, optimization, MMFF, PyMOL
Slug: optimizing-in-rdkit
Authors: Adam Steeves

{% img png /images/ibuprofen_mmff_pymol.png %}

In my [previous post](http://asteeves.github.io/blog/2015/01/12/molecules-in-rdkit/),
I built a molecule in RDKit and saved it for later use. The construction process 
may not have created a molecule that is suitable for our purposes. Let's examine
the geometry of the molceule and visualize it using the PyMOL xmlrpc server.

{% notebook RDKit_KulikLab_02_Geometry.ipynb cells[1:] %}


