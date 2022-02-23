# -*- coding: utf-8 -*-
# @Time : 2021/12/7 0007 16:50
# @Author : Bobby_Liukeling
# @File : try_20211207.py

import tensorflow as tf
import numpy as np
import os
import ast
import logging
import string
import random
import yaml
from datetime import datetime

from dimenet.model.dimenet import DimeNet
from dimenet.model.dimenet_pp import DimeNetPP
from dimenet.model.activations import swish
from dimenet.training.trainer import Trainer
from dimenet.training.metrics import Metrics
from dimenet.training.data_container import DataContainer
from dimenet.training.data_provider import DataProvider



# config.yaml for DimeNet, config_pp.yaml for DimeNet++
with open('config_pp.yaml', 'r') as c:
    config = yaml.safe_load(c)

# For strings that yaml doesn't parse (e.g. None)
#设置参数
for key, val in config.items():
    if type(val) is str:
        try:
            config[key] = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            pass

model_name = config['model_name']

if model_name == "dimenet":
    num_bilinear = config['num_bilinear']
elif model_name == "dimenet++":
    out_emb_size = config['out_emb_size']
    int_emb_size = config['int_emb_size']
    basis_emb_size = config['basis_emb_size']
    extensive = config['extensive']
else:
    raise ValueError(f"Unknown model name: '{model_name}'")

emb_size = config['emb_size']
num_blocks = config['num_blocks']

num_spherical = config['num_spherical']
num_radial = config['num_radial']
output_init = config['output_init']

cutoff = config['cutoff']
envelope_exponent = config['envelope_exponent']

num_before_skip = config['num_before_skip']
num_after_skip = config['num_after_skip']
num_dense_output = config['num_dense_output']

num_train = config['num_train']
num_valid = config['num_valid']
data_seed = config['data_seed']
dataset = config['dataset']
logdir = config['logdir']

num_steps = config['num_steps']
ema_decay = config['ema_decay']

learning_rate = config['learning_rate']
warmup_steps = config['warmup_steps']
decay_rate = config['decay_rate']
decay_steps = config['decay_steps']

batch_size = config['batch_size']
evaluation_interval = config['evaluation_interval']
save_interval = config['save_interval']
restart = config['restart']
comment = config['comment']
targets = config['targets']

data_container = DataContainer(dataset, cutoff=cutoff, target_keys=targets)
data_provider = DataProvider(data_container, num_train, num_valid, batch_size,
                             seed=data_seed, randomized=True)

a = 0