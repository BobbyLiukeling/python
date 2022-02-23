# -*- coding: utf-8 -*-
# @Time : 2021/9/29 0029 20:34
# @Author : Bobby_Liukeling
# @File : try.py
#求解函数 f(x) = x + 10*sin(5*x) + 7*cos(4*x) 在区间[0,9]的最大值。
import math
import random
class GA():
    #initalise
    def __init__(self, length, count):
        #length of chromosome
        self.length = length
        #number of chromosome
        self.count = count
        # randomly get initial population
        self.population = self.get_population(length, count)

    def get_population(self, length, count):
        # get a list of count numbers chromosome (length : length)
        return [self.get_chromosome(length) for i in range(count)]

    def get_chromosome(self, length):
        #randomly get a chromosome which length is length
        # a bit ( 0, 1 ) represent a gene
        chromosome = 0
        for i in range(length):
            chromosome |= ( 1 << i ) * random.randint(0, 1)
        return chromosome

    def evolve(self, retain_rate = 0.2, random_select_rate = 0.5, mutation_rate = 0.01 ):
        #进化函数
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

    def fitness(self, chromosome):#适应条件
        # decode and compute fitness function
        x = self.decode(chromosome)
        return  x + 10 * math.sin(5 * x) + 7 * math.cos(4 * x)

    def selection(self, retain_rate, random_select_rate):
        #英语不好表达了，我就用汉语了
        #通过适应度大小从大到小进行排序，最后生成的仍然是二进制的列表
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]

        # 选出适应性强的染色体,挑选20%作为父类
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]

        # 从剩余的80%里面选出适应性不强，但是幸存的染色体（概率0.5）
        for chromosome in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append(chromosome)
        return parents

    def crossover(self, parents):
        #交叉产生后代
        # 新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群。
        children = []
        #需要繁殖的数量
        target_count = len(self.population) - len(parents)
        while len(children) < target_count:
            malelocation = random.randint(0, len(parents) - 1)
            femalelocation = random.randint(0, len(parents) - 1)
            male = parents[malelocation]
            female = parents[femalelocation]
            if malelocation != femalelocation:
                #随机选择交叉点
                cross_pos = random.randint(0, self.length)
                #生成掩码，方便位运算
                mask = 0
                for i in range(cross_pos):
                    mask |= (1 << i )
                #孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
                child = (male & mask) | (female & ~mask)
                children.append(child)
        #经过繁殖后，孩子和父母的数量与原始种群数量相等，在这里可以更新种群。
        self.population = parents + children

    def mutation(self, rate):#变异函数
        #对种群中的所有个体，随机改变某个个体中的某个基因
        for i in range(len(self.population)):
            if random.random() < rate:
                j = random.randint(0, self.length)
                self.population[i] ^= 1 << j    #^是异或运算

    def decode(self, chromosome):
        #将二进制还原成十进制
        return chromosome * 9.0 / (2**self.length-1)

    def result(self):
        #获得当前最优的个体值
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [ x[1] for x in sorted(graded, reverse = True)]
        return ga.decode(graded[0])


if __name__ == '__main__':
    #染色体长度为17，群落数量是300
    ga = GA(17, 300)
    for x in range(200): #200是迭代次数？？
        ga.evolve()
    print(ga.result())
