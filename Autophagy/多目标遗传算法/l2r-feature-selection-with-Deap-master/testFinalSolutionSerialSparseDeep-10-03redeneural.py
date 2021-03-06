import json
from rpy2 import robjects

import evaluateIndividuoSerial
import l2rCodesSerial
import numpy as np


import re
import math
from sklearn.preprocessing import StandardScaler
import keras
from subprocess import check_output
from sklearn import linear_model
from subprocess import call
from h_l2rMeasures import modelEvaluation, getQueries
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
import os



def compare(x_vet, y_vet, min_p_value=0.1):
    # USANDO o R para calcular t-test
    rd1 = (robjects.FloatVector(x_vet))
    rd2 = (robjects.FloatVector(y_vet))
    rvtest = robjects.r['t.test']
    pvalue = rvtest(rd1, rd2, paired=True)[2][0]

    return pvalue < min_p_value, pvalue


DATASETS = ['lastfm', 'movielens', 'youtube']
params = ['diversityprecision', 'noveltydiversity', 'noveltydiversityprecision', 'noveltyprecision']
full = '1' * 13

for dataset in DATASETS:
    for param in params:

        NOME_COLECAO_BASE = './r1/' + dataset + '-Fold' + '0obj_' + param + '.json'
        COLECAO_BASE = {}

        try:
            with open(NOME_COLECAO_BASE, 'r') as fp:
                COLECAO_BASE = json.load(fp)

            for item in COLECAO_BASE:
                for att in COLECAO_BASE[item]:
                    try:
                        if len(COLECAO_BASE[item][att]) > 1:
                            COLECAO_BASE[item][att] = np.array(COLECAO_BASE[item][att])
                    except:
                        pass
        except:
            print(param + ' ' + dataset + 'error')
            break

        # nsga é 1, spea é 2, 3 ambos
        bestNSGA = 0
        bestSPEA = 0
        bestindNSGA = ''
        bestindSPEA = ''
        if 'precision' in param:
            for ind in COLECAO_BASE:
                if COLECAO_BASE[ind]['method'] == 1 or COLECAO_BASE[ind]['method'] == 3:
                    mean = np.mean(COLECAO_BASE[ind]['precision'])
                    if mean > bestNSGA:
                        bestNSGA = mean
                        bestindNSGA = ind
                if COLECAO_BASE[ind]['method'] == 2 or COLECAO_BASE[ind]['method'] == 3:
                    mean = np.mean(COLECAO_BASE[ind]['precision'])
                    if mean > bestSPEA:
                        bestSPEA = mean
                        bestindSPEA = ind
        else:
            # if 'diversity' in param:
            for ind in COLECAO_BASE:
                if COLECAO_BASE[ind]['method'] == 1 or COLECAO_BASE[ind]['method'] == 3:
                    mean = np.mean(COLECAO_BASE[ind]['diversity'])
                    if mean > bestNSGA:
                        bestNSGA = mean
                        bestindNSGA = ind
                if COLECAO_BASE[ind]['method'] == 2 or COLECAO_BASE[ind]['method'] == 3:
                    mean = np.mean(COLECAO_BASE[ind]['diversity'])
                    if mean > bestSPEA:
                        bestSPEA = mean
                        bestindSPEA = ind

        print(param + ' ' + dataset + 'bestIndSpea:' + bestindSPEA)
        print(param + ' ' + dataset + 'bestIndNSGA:' + bestindNSGA)
        # model = RF
        diversitys = []
        noveltys = []
        ndcgs = []

        # NSGA best IND RF
        ENSEMBLE = 1  # random forest
        NTREES = 20
        SEED = 1887
        NUM_FOLD = '0'
        METRIC = "NDCG"
        sparse = True
        ALGORITHM = 'rf'
        print('reading and training NSGA bestind')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', bestindNSGA, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', bestindNSGA, sparse)
        # print(len(X_train[0]))

        model = l2rCodesSerial.getTheModel(ENSEMBLE, NTREES, 0.3, SEED, dataset)
        model.fit(X_train, y_train)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))

        # SPEA best IND RF
        print('reading and training SPEA bestind')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', bestindSPEA, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', bestindSPEA, sparse)
        # print(len(X_train[0]))

        model = l2rCodesSerial.getTheModel(ENSEMBLE, NTREES, 0.3, SEED, dataset)
        model.fit(X_train, y_train)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))

        # FULL best IND RF
        print('reading and training FULL')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', full, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', full, sparse)
        # print(len(X_train[0]))

        model = l2rCodesSerial.getTheModel(ENSEMBLE, NTREES, 0.3, SEED, dataset)
        model.fit(X_train, y_train)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))

        # model = RN full
        print('reading and training RN nsga best Ind')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', bestindNSGA, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', bestindNSGA, sparse)
        # nneurons = 100
        # nlayers = 1
        # lr = 0.001
        # dropout = 0.2
        parameters = []
        parameters.append([800, 0.01])
        # nneurons = 100
        nneurons = 20
        nlayers = 1
        lr = 0.001
        dropout = 0.2

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        model = keras.models.Sequential()

        # input layer
        model.add(keras.layers.normalization.BatchNormalization(input_shape=tuple([X_train.shape[1]])))
        model.add(keras.layers.core.Dense(nneurons, activation='relu'))
        model.add(keras.layers.core.Dropout(rate=dropout))

        # Hidden layers
        for i in range(nlayers):
            model.add(keras.layers.normalization.BatchNormalization())
            model.add(keras.layers.core.Dense(nneurons, activation='relu'))
            model.add(keras.layers.core.Dropout(rate=dropout))

        model.add(keras.layers.core.Dense(1, activation='sigmoid'))

        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=lr))
        # model.fit(X_train, y_train, epochs=50, verbose=0)
        model.fit(X_train, y_train, epochs=10, verbose=0)

        X_test = scaler.transform(X_test)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))

        ##############################################
        # model = RN full
        print('reading and training RN spea best Ind')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', bestindSPEA, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', bestindSPEA, sparse)
        # nneurons = 100
        # nlayers = 1
        # lr = 0.001
        # dropout = 0.2
        parameters = []
        parameters.append([800, 0.01])
        # nneurons = 100
        nneurons = 20
        nlayers = 1
        lr = 0.001
        dropout = 0.2

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        model = keras.models.Sequential()

        # input layer
        model.add(keras.layers.normalization.BatchNormalization(input_shape=tuple([X_train.shape[1]])))
        model.add(keras.layers.core.Dense(nneurons, activation='relu'))
        model.add(keras.layers.core.Dropout(rate=dropout))

        # Hidden layers
        for i in range(nlayers):
            model.add(keras.layers.normalization.BatchNormalization())
            model.add(keras.layers.core.Dense(nneurons, activation='relu'))
            model.add(keras.layers.core.Dropout(rate=dropout))

        model.add(keras.layers.core.Dense(1, activation='sigmoid'))

        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=lr))
        # model.fit(X_train, y_train, epochs=50, verbose=0)
        model.fit(X_train, y_train, epochs=10, verbose=0)

        X_test = scaler.transform(X_test)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))
        ##########################################################################
        # model = RN full
        print('reading and training RN FULL')
        X_train, y_train, query_id_train = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'train', full, sparse)
        X_test, y_test, query_id_test = l2rCodesSerial.load_L2R_file(
            './dataset/' + dataset + '/' + NUM_FOLD + '.' + 'test', full, sparse)
        # nneurons = 100
        # nlayers = 1
        # lr = 0.001
        # dropout = 0.2
        parameters = []
        parameters.append([800, 0.01])
        # nneurons = 100
        nneurons = 20
        nlayers = 1
        lr = 0.001
        dropout = 0.2

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        model = keras.models.Sequential()

        # input layer
        model.add(keras.layers.normalization.BatchNormalization(input_shape=tuple([X_train.shape[1]])))
        model.add(keras.layers.core.Dense(nneurons, activation='relu'))
        model.add(keras.layers.core.Dropout(rate=dropout))

        # Hidden layers
        for i in range(nlayers):
            model.add(keras.layers.normalization.BatchNormalization())
            model.add(keras.layers.core.Dense(nneurons, activation='relu'))
            model.add(keras.layers.core.Dropout(rate=dropout))

        model.add(keras.layers.core.Dense(1, activation='sigmoid'))

        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=lr))
        # model.fit(X_train, y_train, epochs=50, verbose=0)
        model.fit(X_train, y_train, epochs=10, verbose=0)

        X_test = scaler.transform(X_test)
        resScore = model.predict(X_test)

        scoreTest = [0] * len(y_test)
        c = 0
        for i in resScore:
            scoreTest[c] = i
            c = c + 1

        ndcg, queries = l2rCodesSerial.getEvaluation(scoreTest, query_id_test, y_test, dataset, METRIC, "test")
        ndcgs.append(queries)
        diversitys.append(evaluateIndividuoSerial.getDiversity(scoreTest, y_test, query_id_test))
        noveltys.append(evaluateIndividuoSerial.getNovelty(scoreTest, y_test, query_id_test))

        print('Start Comparison:')
        # num = 6
        num = 6
        for i in range(num):
            for j in range(num):
                if j > i:
                    print(compare(diversitys[i], diversitys[j]))

        for i in range(num):
            for j in range(num):
                if j > i:
                    print(compare(noveltys[i], noveltys[j]))

        for i in range(num):
            for j in range(num):
                if j > i:
                    print(compare(ndcgs[i], ndcgs[j]))
