# -*- coding: utf-8 -*-
# @Time : 2021/9/29 0029 19:24
# @Author : Bobby_Liukeling
# @File : train.py
# Genetic Algorithm Optimization in TensorFlow
#
# We are going to implement a genetic algorithm to optimize to find out the maximum value of the function
# f(x)=x+10sin(5x)+7cos(4x)
# in the range [0, 9].
#
# We will use TensorFlow's update function to run the different parts of the genetic algorithm.

# import os
# from math import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops

ops.reset_default_graph()


# genetic algorithm parameters
upper_limit = 9
low_limit = 0
precision = 4
population_size = (upper_limit - low_limit) * pow(10, precision)
features = 50
selection = 0.2
pop_size = 10000
mutation = 1.0 / pop_size
generations = 200
num_parents = int(pop_size * selection)
num_children = pop_size - num_parents

# start a graph session
sess = tf.compat.v1.Session()

# create ground truth
truth = np.sin(2 * np.pi * (np.arange(features, dtype=np.float32)) / features)

# initialize population array
population = tf.Variable(np.random.randn(pop_size, features), dtype=tf.float32)

# initialize placeholders
# tf.compat.v1.placeholder
tf.compat.v1.disable_eager_execution()
truth_ph = tf.compat.v1.placeholder(tf.float32, [1, features])
crossover_mat_ph = tf.compat.v1.placeholder(tf.float32, [num_children, features])
mutation_val_ph = tf.compat.v1.placeholder(tf.float32, [num_children, features])

# calculate fitness (MSE)
fitness = -tf.reduce_mean(tf.square(tf.subtract(population, truth_ph)), 1)
top_vals, top_ind = tf.nn.top_k(fitness, k=pop_size)

# get best fit individual
best_val = tf.reduce_min(top_vals)
best_ind = tf.argmin(top_vals, 0)
best_individual = tf.gather(population, best_ind)

# get parents
population_sorted = tf.gather(population, top_ind)
parents = tf.slice(population_sorted, [0, 0], [num_parents, features])

# get offspring
# indices to shuffle-gather parents
rand_parent1_ix = np.random.choice(num_parents, num_children)
rand_parent2_ix = np.random.choice(num_parents, num_children)
# gather parents by shuffled indices, expand back out to pop_size too
rand_parent1 = tf.gather(parents, rand_parent1_ix)
rand_parent2 = tf.gather(parents, rand_parent2_ix)
rand_parent1_sel = tf.multiply(rand_parent1, crossover_mat_ph)
rand_parent2_sel = tf.multiply(rand_parent2, tf.subtract(1., crossover_mat_ph))
children_after_sel = tf.add(rand_parent1_sel, rand_parent2_sel)

# mutate children
mutated_children = tf.add(children_after_sel, mutation_val_ph)

# combine children and parents into new population
new_population = tf.concat(axis=0, values=[parents, mutated_children])

step = tf.group(population.assign(new_population))

init = tf.global_variables_initializer()
sess.run(init)

# run through generations
for i in range(generations):
    # create cross-over matrices for plugging in.
    crossover_mat = np.ones(shape=[num_children, features])
    crossover_point = np.random.choice(np.arange(1, features - 1, step=1), num_children)
    for pop_ix in range(num_children):
        crossover_mat[pop_ix, 0:crossover_point[pop_ix]] = 0.
    # generate mutation probability matrices
    mutation_prob_mat = np.random.uniform(size=[num_children, features])
    mutation_values = np.random.normal(size=[num_children, features])
    mutation_values[mutation_prob_mat >= mutation] = 0

    # run GA step
    feed_dict = {truth_ph: truth.reshape([1, features]),
                 crossover_mat_ph: crossover_mat,
                 mutation_val_ph: mutation_values}
    step.run(feed_dict, session=sess)
    best_individual_val = sess.run(best_individual, feed_dict=feed_dict)

    best_fit = sess.run(best_val, feed_dict=feed_dict)
    print('Generation: {}, Best Fitness (lowest MSE): {:.2}'.format(i, -best_fit))

plt.plot(truth, label="True Values")
plt.plot(np.squeeze(best_individual_val), label="Best Individual")
plt.axis((0, features, -1.25, 1.25))
plt.legend(loc='upper right')
plt.show()