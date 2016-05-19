from Thermal_Models import estimate_parameters, \
                           physiological_growth_model, \
                           Boltzmann_Arrhenius, \
                           schoolfield_two_factor, \
                           schoolfield_original_simple, \
                           schoolfield_original, \
                           read_database, \
                           fit_models, \
                           split_datasets, \
                           rank_and_flatten, \
                           compile_models
import numpy as np
import pandas as pd
from datetime import datetime

starttime = datetime.now()

data_path = '../Data/database.csv'
data = read_database(data_path) 

Datasets = split_datasets(data)
model_names = ['schoolfield_two_factor', 'schoolfield_original_simple', 'schoolfield_original']
all_models = []

aux_parameters = ['FinalID', 'OriginalID', 'Citation', 'Latitude', 'Longitude', 'ConKingdom', 'ConPhylum', 'ConClass',
                  'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'OptimalConditions', 'Best_Guess']                
                  
for i in Datasets.keys():
    dataset = Datasets[i]
    est_params = estimate_parameters(dataset, aux_parameters)
    models = fit_models(model_names, est_params, tag = i)
    
    if models:
        all_models.append(models)
        best_model = max(models)
        print(best_model)
        best_model.plot('../Results/fits')
         
all_models = rank_and_flatten(all_models)
compile_models(all_models, path = '../Results/summary.csv', aux_cols = aux_parameters)
compile_models(all_models, path = '../Data/summaries/summary.csv', aux_cols = aux_parameters)

print('Completed in: ', datetime.now() - starttime)