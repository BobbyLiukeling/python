#!/usr/bin/env python
# (C) 2017 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

import os
import sys

from openeye import oechem
from openeye import oefastrocs
from openeye import oeshape

oepy = os.path.join(os.path.dirname(__file__), "..", "python")
sys.path.insert(0, os.path.realpath(oepy))


def main(argv=[__name__]):
    if len(argv) < 3:
        oechem.OEThrow.Usage("%s <database> [<queries> ... ]" % argv[0])

    if not oefastrocs.OEFastROCSIsGPUReady():
        oechem.OEThrow.Info("No supported GPU available!")
        return 0

    dbname = argv[1]
    if oechem.OEIsGZip(dbname):
        oechem.OEThrow.Fatal("%s is an unsupported database file format as it is gzipped.\n"
                             "Preferred formats are .oeb, .sdf or .oez" % dbname)

    # read in database
    ifs = oechem.oemolistream()
    if not ifs.open(dbname):
        oechem.OEThrow.Fatal("Unable to open '%s'" % dbname)

    print("Opening database file %s ..." % dbname)
    timer = oechem.OEWallTimer()
    dbase = oefastrocs.OEShapeDatabase()
    moldb = oechem.OEMolDatabase()
    if not moldb.Open(ifs):
        oechem.OEThrow.Fatal("Unable to open '%s'" % dbname)

    dots = oechem.OEThreadedDots(10000, 200, "conformers")
    if not dbase.Open(moldb, dots):
        oechem.OEThrow.Fatal("Unable to initialize OEShapeDatabase on '%s'" % dbname)

    dots.Total()
    print("%f seconds to load database" % timer.Elapsed())

    for qfname in argv[2:]:

        ext = oechem.OEGetFileExtension(qfname)
        base = qfname[:-(len(ext) + 1)]

        if ext == 'sq':
            query = oeshape.OEShapeQuery()
            if not oeshape.OEReadShapeQuery(qfname, query):
                oechem.OEThrow.Fatal("Unable to open '%s'" % qfname)
            ext = 'oeb'
        else:
            # read in query
            qfs = oechem.oemolistream()
            if not qfs.open(qfname):
                oechem.OEThrow.Fatal("Unable to open '%s'" % qfname)

            query = oechem.OEGraphMol()
            if not oechem.OEReadMolecule(qfs, query):
                oechem.OEThrow.Fatal("Unable to read query from '%s'" % qfname)

        # write out everthing to a similary named file
        ofs = oechem.oemolostream()
        ofname = base + "_results." + ext
        if not ofs.open(ofname):
            oechem.OEThrow.Fatal("Unable to open '%s'" % argv[4])

        print("Searching for %s" % qfname)
        numHits = moldb.NumMols()
        opts = oefastrocs.OEShapeDatabaseOptions()
        opts.SetLimit(numHits)
        for score in dbase.GetSortedScores(query, opts):
            dbmol = oechem.OEMol()
            molidx = score.GetMolIdx()
            if not moldb.GetMolecule(dbmol, molidx):
                print("Unable to retrieve molecule '%u' from the database" % molidx)
                continue

            mol = oechem.OEGraphMol(dbmol.GetConf(oechem.OEHasConfIdx(score.GetConfIdx())))

            oechem.OESetSDData(mol, "ShapeTanimoto", "%.4f" % score.GetShapeTanimoto())
            oechem.OESetSDData(mol, "ColorTanimoto", "%.4f" % score.GetColorTanimoto())
            oechem.OESetSDData(mol, "TanimotoCombo", "%.4f" % score.GetTanimotoCombo())
            score.Transform(mol)

            oechem.OEWriteMolecule(ofs, mol)
        print("Wrote results to %s" % ofname)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
