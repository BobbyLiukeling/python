using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PatternGenetic
{
    //template for genotype objects 
    public class genotype : IComparable
    {
        public int Fitness;
        public int[] X = new int[65];

        public int[] Y = new int[65];
        //This extension defines sorting behaviour based on Fitness in ascending order
        public int CompareTo(object gene)
        {
            if (((genotype)gene).Fitness < this.Fitness)
            {
                return 1;
            }
            else if (((genotype)gene).Fitness == this.Fitness)
            {
                return 0;
            }
            else if (((genotype)gene).Fitness > this.Fitness)
            {
                return -1;
            }
            return Convert.ToInt32(null);
        }
    }
}
