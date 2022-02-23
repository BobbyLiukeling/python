
using Microsoft.VisualBasic;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization;

namespace PatternGenetic
{
    // exposes algorithm and helper functions 
    public class GAHelper
    {
        #region "Public Members & Variables"
        // Population Size
        public int PopulationSize;
        public int Folding;
        // First population
        public genotype[] population = new genotype[201];
        public genotype[] TopGenomeByPopulation = new genotype[201];
        //New population
        public int TopGenome = 0;
        public genotype[] newpopulation = new genotype[200];
        // ProteinStructure Value from User Input
        public string ProteinStructure;
        // ProteinStructure.Length
        public int ProteinLength;
        //Array to that stores all the indexes of hydropohobic positions from the input protein sequence
        public int[] HydrophobicPosition;
        //Array containing number of hydrophobic occurrences present in the input protein sequence
        public int HydrophobicOccurences;
        //Index in the New population
        public int CurrentPosNewPopulation;
        public int CompleteFitness = 0;
        // Elite rate value from User Input
        public decimal eliteRate;
        // cross over rate from User Input
        public decimal crossOverRate;
        // Mutation rate from User Input
        public decimal mutationRate;
        public int mutationPositionInNewPopulation;
        public int Generation = 0;
        // Maximum generations from User Input
        public int maxGenerations;
        //This method checks the input protein structure and if it is hydrophoibc it stores it correspoing index into an array.
        #endregion

        public object SetHydroPhobicArray()
        {
            int HydrophobicIndex = 1;
            ProteinLength = ProteinStructure.Length;
            HydrophobicPosition = new int[ProteinLength + 1];
            HydrophobicOccurences = 0;
            char[] hOccurence = ProteinStructure.ToCharArray();
            for (int index = 1; index <= ProteinLength; index++)
            {
                if ((hOccurence[index - 1] == 'h'))
                {
                    HydrophobicPosition[HydrophobicIndex] = index;
                    HydrophobicIndex = HydrophobicIndex + 1;
                    HydrophobicOccurences = HydrophobicOccurences + 1;
                }
            }
            return null;
        }
        public object Initialization()
        {
            int i = 0;
            for (i = 1; i <= PopulationSize; i++)
            {
                Folding = 0;
                RandomOrientation(i);

                while ((Folding == 0))
                {
                    RandomOrientation(i);
                }
                population[i].Fitness = ComputeFitness(i);
                CompleteFitness = CompleteFitness + population[i].Fitness;
            }
            return null;
        }
        //Compute Fitness for a given protein structure
        public int ComputeFitness(long n)
        {
            int isSequential = 0;
            int Fitness = 0;
            int latticeDistance = 0;
            for (int i = 1; i <= HydrophobicOccurences - 1; i++)
            {
                for (int j = i + 1; j <= HydrophobicOccurences; j++)
                {
                    isSequential = (Math.Abs(HydrophobicPosition[i] - HydrophobicPosition[j]));
                    ///*Not Sequential */
                    if ((isSequential != 1))
                    {
                        latticeDistance = Math.Abs(population[n].X[HydrophobicPosition[i]] - population[n].X[HydrophobicPosition[j]]) + Math.Abs(population[n].Y[HydrophobicPosition[i]] - population[n].Y[HydrophobicPosition[j]]);
                        if ((latticeDistance == 1))
                        {
                            Fitness = Fitness - 1;
                        }
                    }
                }
            }
            return Fitness;
        }

        // Generate elite population
        public void GenerateElitePopulation()
        {
            newpopulation = new genotype[PopulationSize + 1];
            int elitePopulation = 0;
            elitePopulation = Convert.ToInt32(eliteRate * PopulationSize);
            Array.ConstrainedCopy(population, 1, newpopulation, 1, elitePopulation);
        }

        //Generates cross over population
        public void GenerateCrossOverPopulation()
        {
            int crossOverStartIndex = Convert.ToInt32(eliteRate * PopulationSize + 1);
            int crossOverLastIndex = Convert.ToInt32(crossOverRate * PopulationSize + crossOverStartIndex - 1);
            int crossOverPoint = 0;
            int i = 0;
            int j = 0;
            int maxEndPoint = ProteinLength - 3;
            for (int Index = crossOverStartIndex; Index <= crossOverLastIndex; Index++)
            {
                CurrentPosNewPopulation = Index;
                while (!(i > 0))
                {
                    i = RandomSelection();
                }
                while (!(j > 0))
                {
                    j = RandomSelection();
                }
                newpopulation[CurrentPosNewPopulation] = new genotype();
                VBMath.Randomize();
                crossOverPoint = Convert.ToInt32(maxEndPoint * VBMath.Rnd() + 2);
                int Success = Convert.ToInt32(CrossOver(i, j, crossOverPoint));
                while (Success == 0)
                {
                    while (!(i > 0))
                    {
                        i = RandomSelection();
                    }
                    while (!(j > 0))
                    {
                        j = RandomSelection();
                    }
                    VBMath.Randomize();
                    crossOverPoint = Convert.ToInt32(maxEndPoint * VBMath.Rnd() + 2);
                    Success = Convert.ToInt32(CrossOver(i, j, crossOverPoint));
                }
            }
        }

        //This function will fill the remaining population in new population array
        public void FillRemainingNewPopulation()
        {
            try
            {
                int remainingNewPopulationStartIndex = Convert.ToInt32(eliteRate * PopulationSize + crossOverRate * PopulationSize + 1);
                Array.ConstrainedCopy(population, remainingNewPopulationStartIndex, newpopulation, remainingNewPopulationStartIndex, PopulationSize - remainingNewPopulationStartIndex + 1);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public object RandomOrientation(long m)
        {

            int PreviousDirection = 0;
            int PresentDirection = 0;
            int i = 0;
            int temp1 = 0;
            int temp2 = 0;
            int temp3 = 0;
            int X = 0;
            int Y = 0;
            int j = 0;
            int Flag = 0;
            int Step2 = 0;
            int[] a = new int[5];
            int[] Ax = new int[5];
            int[] Ay = new int[5];

            //                                        3
            //             Select Direction as:     2 X 1
            //                                        4
            //
            population[m] = new genotype();
            Folding = 1;
            population[m].X[1] = 0;
            population[m].Y[1] = 0;
            population[m].X[2] = 1;
            population[m].Y[2] = 0;
            PreviousDirection = 1;



            for (i = 3; i <= ProteinLength; i++)
            {
                switch (PreviousDirection)
                {
                    case 1:
                        a[1] = 1;
                        Ax[1] = 1;
                        Ay[1] = 0;
                        a[2] = 3;
                        Ax[2] = 0;
                        Ay[2] = 1;
                        a[3] = 4;
                        Ax[3] = 0;
                        Ay[3] = -1;
                        break;
                    case 2:
                        a[1] = 2;
                        Ax[1] = -1;
                        Ay[1] = 0;
                        a[2] = 3;
                        Ax[2] = 0;
                        Ay[2] = 1;
                        a[3] = 4;
                        Ax[3] = 0;
                        Ay[3] = -1;
                        break;
                    case 3:
                        a[1] = 1;
                        Ax[1] = 1;
                        Ay[1] = 0;
                        a[2] = 2;
                        Ax[2] = -1;
                        Ay[2] = 0;
                        a[3] = 3;
                        Ax[3] = 0;
                        Ay[3] = 1;
                        break;
                    case 4:
                        a[1] = 1;
                        Ax[1] = 1;
                        Ay[1] = 0;
                        a[2] = 2;
                        Ax[2] = -1;
                        Ay[2] = 0;
                        a[3] = 4;
                        Ax[3] = 0;
                        Ay[3] = -1;
                        break;
                }

                temp1 = Convert.ToInt32(3 * VBMath.Rnd() + 1);
                PresentDirection = temp1;
                temp2 = 0;
                temp3 = 0;
                X = population[m].X[i - 1] + Ax[temp1];
                Y = population[m].Y[i - 1] + Ay[temp1];
                Flag = 0;

                for (j = 1; j <= i - 1; j++)
                {
                    if ((X == population[m].X[j] & Y == population[m].Y[j]))
                    {
                        Flag = 1;
                        goto MyJump1;
                    }
                }
            MyJump1:

                if ((Flag == 1))
                {
                    Flag = 0;
                    Step2 = 6 - temp1;
                    switch (Step2)
                    {
                        case 3:
                            if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                            {
                                temp2 = 1;
                            }
                            else
                            {
                                temp2 = 2;
                            }
                            break;
                        case 4:
                            if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                            {
                                temp2 = 1;
                            }
                            else
                            {
                                temp2 = 3;
                            }
                            break;
                        case 5:
                            if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                            {
                                temp2 = 2;
                            }
                            else
                            {
                                temp2 = 3;
                            }
                            break;
                    }

                    PresentDirection = temp2;
                    temp3 = 6 - (temp1 + temp2);
                    X = population[m].X[i - 1] + Ax[temp2];
                    Y = population[m].Y[i - 1] + Ay[temp2];

                    for (j = 1; j <= i - 1; j++)
                    {
                        if ((X == population[m].X[j] & Y == population[m].Y[j]))
                        {
                            Flag = 1;
                            goto MyJump2;
                        }
                    }
                MyJump2:
                    if ((Flag == 1))
                    {
                        Flag = 0;
                        PresentDirection = temp3;
                        X = population[m].X[i - 1] + Ax[temp3];
                        Y = population[m].Y[i - 1] + Ay[temp3];
                        for (j = 1; j <= i - 1; j++)
                        {
                            if ((X == population[m].X[j] & Y == population[m].Y[j]))
                            {
                                Flag = 1;
                                Folding = 0;
                                //GoTo MyJump3

                            }
                        }
                    }
                }
                PreviousDirection = a[PresentDirection];
                population[m].X[i] = population[m].X[i - 1] + Ax[PresentDirection];
                population[m].Y[i] = population[m].Y[i - 1] + Ay[PresentDirection];
            }
        MyJump3:
            return null;
        }

        //Random selection
        public int RandomSelection()
        {
            VBMath.Randomize();
            int rndVar = Convert.ToInt32(VBMath.Rnd() * Math.Abs(CompleteFitness));
            int index = 0;
            for (index = 1; index <= PopulationSize; index++)
            {
                rndVar = rndVar - Math.Abs(population[index].Fitness);
                if ((rndVar < 0))
                {
                    return index - 1;
                }
            }
            return Convert.ToInt32(null);
        }
        public long CrossOver(long i, long j, int n)
        {
            long functionReturnValue = 0;

            long PrevDirection = 0;
            long k = 0;
            long z = 0;
            long p = 0;
            long temp1 = 0;
            long temp2 = 0;
            long temp3 = 0;
            long Collision = 0;
            long dx = 0;
            long dy = 0;
            long Step2 = 0;
            long id = 0;
            long[] a = new long[5];
            long[] Ax = new long[5];
            long[] Ay = new long[5];

            id = CurrentPosNewPopulation;

            ///* Detect Previous Direction */
            if ((population[i].X[n] == population[i].X[n - 1]))
            {
                p = population[i].Y[n - 1] - population[i].Y[n];
                if ((p == 1))
                {
                    PrevDirection = 3;
                }
                else
                {
                    PrevDirection = 4;
                }

            }
            else
            {
                p = population[i].X[n - 1] - population[i].X[n];
                if ((p == 1))
                {
                    PrevDirection = 1;
                }
                else
                {
                    PrevDirection = 2;
                }
            }


            switch (PrevDirection)
            {
                case 1:
                    Ax[1] = -1;
                    Ay[1] = 0;
                    Ax[2] = 0;
                    Ay[2] = 1;
                    Ax[3] = 0;
                    Ay[3] = -1;
                    break;
                case 2:
                    Ax[1] = 1;
                    Ay[1] = 0;
                    Ax[2] = 0;
                    Ay[2] = 1;
                    Ax[3] = 0;
                    Ay[3] = -1;
                    break;
                case 3:
                    Ax[1] = 1;
                    Ay[1] = 0;
                    Ax[2] = -1;
                    Ay[2] = 0;
                    Ax[3] = 0;
                    Ay[3] = -1;

                    break;
                case 4:
                    Ax[1] = 1;
                    Ay[1] = 0;
                    Ax[2] = -1;
                    Ay[2] = 0;
                    Ax[3] = 0;
                    Ay[3] = 1;
                    break;
            }

            temp1 = Convert.ToInt32(VBMath.Rnd() * 3 + 1);

            newpopulation[id].X[n + 1] = Convert.ToInt32(population[i].X[n] + Ax[temp1]);
            newpopulation[id].Y[n + 1] = Convert.ToInt32(population[i].Y[n] + Ay[temp1]);
            Collision = 0;

            dx = newpopulation[id].X[n + 1] - population[j].X[n + 1];
            dy = newpopulation[id].Y[n + 1] - population[j].Y[n + 1];

            for (k = n + 1; k <= ProteinLength; k++)
            {
                newpopulation[id].X[k] = Convert.ToInt32(population[j].X[k] + dx);
                newpopulation[id].Y[k] = Convert.ToInt32(population[j].Y[k] + dy);

                for (z = 1; z <= n; z++)
                {
                    if (((newpopulation[id].X[k] == population[i].X[z]) & (newpopulation[id].Y[k] == population[i].Y[z])))
                    {
                        Collision = 1;
                        goto MyOut1;
                    }
                }
            }
        MyOut1:

            ///* ======> Second try ==== */
            if ((Collision == 1))
            {
                Collision = 0;
                Step2 = 6 - temp1;
                switch (Step2)
                {
                    case 3:
                        if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                        {
                            temp2 = 1;
                        }
                        else
                        {
                            temp2 = 2;
                        }

                        break;
                    case 4:
                        if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                        {
                            temp2 = 1;
                        }
                        else
                        {
                            temp2 = 3;
                        }

                        break;
                    case 5:
                        if (Convert.ToInt32(VBMath.Rnd() * 2 + 1) == 1)
                        {
                            temp2 = 2;
                        }
                        else
                        {
                            temp2 = 3;
                        }
                        break;
                }

                temp3 = 6 - (temp1 + temp2);
                newpopulation[id].X[n + 1] = Convert.ToInt32(population[i].X[n] + Ax[temp2]);
                newpopulation[id].Y[n + 1] = Convert.ToInt32(population[i].Y[n] + Ay[temp2]);
                dx = newpopulation[id].X[n + 1] - population[j].X[n + 1];
                dy = newpopulation[id].Y[n + 1] - population[j].Y[n + 1];


                for (k = n + 1; k <= ProteinLength; k++)
                {
                    newpopulation[id].X[k] = Convert.ToInt32(population[j].X[k] + dx);
                    newpopulation[id].Y[k] = Convert.ToInt32(population[j].Y[k] + dy);

                    for (z = 1; z <= n; z++)
                    {
                        if (((newpopulation[id].X[k] == population[i].X[z]) & (newpopulation[id].Y[k] == population[i].Y[z])))
                        {
                            Collision = 1;
                            goto MyOut2;
                        }
                    }
                }
            MyOut2:

                if ((Collision == 1))
                {
                    Collision = 0;
                    newpopulation[id].X[n + 1] = Convert.ToInt32(population[i].X[n] + Ax[temp3]);
                    newpopulation[id].Y[n + 1] = Convert.ToInt32(population[i].Y[n] + Ay[temp3]);
                    dx = newpopulation[id].X[n + 1] - population[j].X[n + 1];
                    dy = newpopulation[id].Y[n + 1] - population[j].Y[n + 1];
                    for (k = n + 1; k <= ProteinLength; k++)
                    {
                        newpopulation[id].X[k] = Convert.ToInt32(population[j].X[k] + dx);
                        newpopulation[id].Y[k] = Convert.ToInt32(population[j].Y[k] + dy);
                        for (z = 1; z <= n; z++)
                        {
                            if (((newpopulation[id].X[k] == population[i].X[z]) & (newpopulation[id].Y[k] == population[i].Y[z])))
                            {
                                Collision = 1;
                                goto MyOut3;
                            }
                        }
                    }
                }
                ///* 3rd try if ends */
            }
        MyOut3:
            ///* 2nd try if ends */

            if (Collision == 0)
            {
                for (k = 1; k <= n; k++)
                {
                    newpopulation[id].X[k] = population[i].X[k];
                    newpopulation[id].Y[k] = population[i].Y[k];
                }
                functionReturnValue = 1;
            }
            return functionReturnValue;

        }

        //mutation calculation

        public void GenerateMutation()
        {
            int mutationPopulation = Convert.ToInt32(mutationRate * PopulationSize);
            VBMath.Randomize();
            int geneToBeMutated = Convert.ToInt32(199 * VBMath.Rnd() + 1);
            VBMath.Randomize();
            int maxEndPoint = ProteinLength - 3;
            int mutationPoint = Convert.ToInt32(maxEndPoint * VBMath.Rnd() + 2);
            try
            {
                VBMath.Randomize();
                mutationPositionInNewPopulation = Convert.ToInt32(189 * VBMath.Rnd() + 11);
                for (int index = 1; index <= mutationPopulation; index++)
                {
                    mutationPositionInNewPopulation = mutationPositionInNewPopulation;
                    int MutationStatus = Convert.ToInt32(Mutation(geneToBeMutated, mutationPoint));
                    while (MutationStatus == 0)
                    {
                        geneToBeMutated = Convert.ToInt32(199 * VBMath.Rnd() + 1);
                        mutationPoint = Convert.ToInt32(maxEndPoint * VBMath.Rnd() + 2);
                        MutationStatus = Convert.ToInt32(Mutation(geneToBeMutated, mutationPoint));
                    }
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public long Mutation(long i, int n)
        {
            long functionReturnValue = 0;
            long id = 0;
            long a = 0;
            long b = 0;
            long A_Limit = 0;
            long choice = 0;
            long Collision = 0;
            long k = 0;
            long z = 0;
            long p = 0;
            int[] Ary = new int[4];

            id = mutationPositionInNewPopulation;

            // possible rotations 90ß,180ß,270ß
            //           index       1   2    3
            //


            Ary[1] = 1;
            Ary[2] = 2;
            Ary[3] = 3;
            A_Limit = 3;

            a = population[i].X[n];
            ///* (a, b) rotating point */
            b = population[i].Y[n];
            try
            {

                do
                {
                    Collision = 0;
                    if ((A_Limit > 1))
                    {
                        VBMath.Randomize();
                        //choice = Convert.ToInt32(A_Limit * VBMath.Rnd() + 1);
                        choice = Convert.ToInt32(new Random().Next(1, Convert.ToInt32(A_Limit)).ToString());
                    }
                    else
                    {
                        choice = A_Limit;
                    }

                    
                    p = Ary[choice];
                    for (k = choice; k <= A_Limit - 1; k++)
                    {
                        Ary[k] = Ary[k + 1];
                    }

                    A_Limit = A_Limit - 1;

                    for (k = n + 1; k <= ProteinLength; k++)
                    {
                        switch (p)
                        {

                            case 1:
                                newpopulation[id].X[k] = Convert.ToInt32(a + b - population[i].Y[k]);
                                ///* X' = [a+b]-Y  */
                                newpopulation[id].Y[k] = Convert.ToInt32(population[i].X[k] + b - a);
                                ///* Y' = [X+b]-a  */
                                break;
                            case 2:
                                newpopulation[id].X[k] = Convert.ToInt32(2 * a - population[i].X[k]);
                                ///* X' = [2a - X] */
                                newpopulation[id].Y[k] = Convert.ToInt32(2 * b - population[i].Y[k]);
                                ///* Y' = [2b-Y]   */
                                break;
                            case 3:
                                newpopulation[id].X[k] = Convert.ToInt32(population[i].Y[k] + a - b);
                                ///* X' =  Y+a-b   */
                                newpopulation[id].Y[k] = Convert.ToInt32(a + b - population[i].X[k]);
                                ///* Y' =  [a+b]-X */
                                break;
                        }


                        for (z = 1; z <= n; z++)
                        {
                            if (((newpopulation[id].X[k] == population[i].X[z]) & (newpopulation[id].Y[k] == population[i].Y[z])))
                            {
                                Collision = 1;
                                goto MyJump;
                            }
                        }
                    }

                    if ((Collision == 0))
                    {
                        A_Limit = 0;
                    }

                } while (!(A_Limit == 0));

            MyJump:
                if ((Collision == 0))
                {
                    for (k = 1; k <= n; k++)
                    {
                        newpopulation[id].X[k] = population[i].X[k];
                        newpopulation[id].Y[k] = population[i].Y[k];
                    }
                    functionReturnValue = 1;
                }
                else
                {
                    functionReturnValue = 0;
                }
                return functionReturnValue;
            }
            catch (Exception ex)
            {
                //MessageBox.Show(A_Limit.ToString() + "--" + choice);
                return functionReturnValue;
            }
        }
    }
}
