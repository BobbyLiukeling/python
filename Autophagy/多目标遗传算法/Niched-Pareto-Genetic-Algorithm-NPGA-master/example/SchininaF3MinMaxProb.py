import math
import sys
sys.path.append(r"F:/Code/Python/Autophagy/多目标遗传算法/Niched-Pareto-Genetic-Algorithm-NPGA-master")
import NPGA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def scaleMinMax(x, xmin, xmax, mindesired, maxdesired):
	return ((x - xmin) / (xmax - xmin) * (maxdesired - mindesired) + mindesired)

def graytodec(bin_list):
	"""
	Convert from Gray coding to binary coding.
	We assume big endian encoding.
	"""
	b = bin_list[0]
	d = int(b) * (2**(len(bin_list)-1))
	for i, e in enumerate(range(len(bin_list) - 2, -1, -1)):
		b = str(int(b != bin_list[i + 1]))
		d += int(b) * (2**e)
	return d

def decodechromosome(bits):
	dec = graytodec(bits)
	max_current = math.pow(2, len(bits)) - 1
	value = scaleMinMax(dec, 0, max_current, -10, 10)
	return value

class StaticGen:
	Generation = 1


def display(statistics):

	xpop = []
	ypop = []
	for individual in statistics.population:
		xpop.append(decodechromosome(individual.Genes))
		ypop.append(individual.Fitness)

	xbest = []
	ybest = []
	for specie in statistics.Species:
		xbest.append(decodechromosome(specie.Genes))
		ybest.append(specie.Fitness)

	xEUbest = [decodechromosome(statistics.EuclideanBetter.Genes)]
	yEUbest = [statistics.EuclideanBetter.Fitness]

	x = np.linspace(-10,10,100)
	y21 = [F1(i) for i in x if True]
	y22 = [F2(i) for i in x if True]
	y33 = [F3(i) for i in x if True]

	plt.figure(1)
	plt.clf()

	plt.axis([-10, 10, -1.5, 3])
	plt.plot(x, y21, 'k')
	plt.plot(x, y22, 'k')
	plt.plot(x, y33, 'k')
	plt.plot(xpop, ypop, 'ko')
	plt.plot(xbest, ybest, 'go')
	plt.plot(xEUbest, yEUbest, 'ro')
	plt.title('Simple MO problem, GENERATION: ' + str(StaticGen.Generation))
	plt.xlabel('x')
	plt.ylabel('y')
	plt.grid()

	plt.draw()
	plt.pause(0.001)
	plt.show(block=False)

	f1x = []
	f2x = []
	f3x = []
	for point in statistics.ParetoSet:
		f1x.append(point.Fitness[0])
		f2x.append(point.Fitness[1])
		f3x.append(point.Fitness[2])
	fig = plt.figure(2)
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(f1x, f3x, f2x, c='k', marker='o')
	#plt.title('Pareto Front')
	plt.grid()
	plt.draw()
	plt.pause(0.001)
	plt.show(block=False)

	print(statistics.EuclideanBetter.Genes, end='\t')
	print(statistics.EuclideanBetter.Fitness)

	StaticGen.Generation = StaticGen.Generation + 1


def F1(x):
	return x * 0.04 + math.sin(x)

def F2(x):
	return 0.01 * (x - 2) * (x - 2) + 0.7

def F3(x):
	return 0.00001 * x + 0.5

def getfitness(candidate):
	x = decodechromosome(candidate)
	return [[F1(x), 'maximize'], [F2(x), 'minimize'], [F3(x), 'minimize']]

def test():
	geneset = '01'
	genelen = [128]

	def fnDisplay(statistics): display(statistics)
	def fnGetFitness(genes): return getfitness(genes)

	optimalFitness = [1, 0.701, 0.51]

	GA = NPGA.NichedParetoGeneticAlgorithm(
							fnGetFitness, fnDisplay, optimalFitness,
							geneset, genelen, population_size = 50,
							max_generation = 200, crossover_rate = 0.8,
							mutation_rate = 1/100, niche_radius = 0.08,
							candidate_size = 2, prc_tournament_size = 0.2,
							fastmode = True)
	paretosolution = GA.Evolution()

test()
plt.show()
