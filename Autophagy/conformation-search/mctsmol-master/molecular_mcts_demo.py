from mctsmol import *
from rdkit import Chem


if __name__ == '__main__':
    allowed_angle_values = [60., 120., 180., 240., 300.]
    num_simulations = 100 #模拟的分子角度方向数目
    energy_function = mmff94_potential

    mcts = MolecularMCTS(allowed_angle_values, energy_function)

    # state = mcts.init_state("c1(Cc2ccc(C#C[C@@H](N(C(N)=O)O)C)s2)ccc(F)cc1")  # molecule_2
    #将smiles分子式转化为mol分子式
    state = mcts.init_state("CCCCC[C@H](O)/C=C/[C@@H]1[C@@H](C/C=C\CCCC(O)=O)[C@@H]2C[C@H]1OO2")  # molecule_100
    # state = mcts.init_state("COC1=CC(N)=C(Cl)C=C1C(=O)N[C@H]1CCN(C[C@H]1OC)CCCOC1C=CC(F)=CC=1")  # molecule_71
    # state = mcts.init_state("CC(C)/N=C(\\N)/N=C(\\N)/NOCCCOC1C=CC(=CC=1Cl)OC(F)(F)F")  # molecule_96
    num_angles = mcts.get_num_angles() #分子节点个数

    while len(state[1]) < num_angles:
        state = mcts.search(state, num_simulations)
        print("angles: %s; energy: %s" % (state[1], energy_function(state[0])))

    print("final state: %s (energy: %s)" %(state[1], energy_function(state[0])))

    with open('molecular_mcts.mol', 'w') as f:
        state[0].SetProp("_Name", "optimized_structure")
        f.write(Chem.MolToMolBlock(state[0]))
