#!/usr/bin/env python
# coding: utf-8

# # Model selection
#
# Cross-validation is used here to select the best model. In this script it is used to test the best machine learning model for use in this context.
#
# <u>Tests using the following models :</u>
# * Linear regression
# * Random forest regressor
# * XGBoost
# * Extra Trees Regressor
#
# <u> The following variables are included in the model:</u>
# * Weather variables (rain, temperature, windspeed)
# * Time variables (Day of week, month, year, time of day, public holiday)
# * Sensor environment variables (within a 500m buffer of the sensor):
#     * Betweenness of the street
#     * Buildings in proximity to the sensor
#     * Landmarks in proximity to the sensor
#     * Furniture in proximity to the sensor
#     * Lights in proximity to the sensor

# In[1]:


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
import numpy as np
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import xgboost as xgb
from sklearn.pipeline import Pipeline
import folium
import branca.colormap as cm
from eli5.sklearn import PermutationImportance
import joblib
import os
import psutil

# Move to the modelling directory
try:
    os.chdir("./MelbourneAnalysis/3. Modelling")
except FileNotFoundError as e:
    print(f"Unable to change directory, assuming that we are already in the correct directory: {os.getcwd()}")

from Functions import *


# In[2]:


buffer_size_m = 400
input_csv ="../Cleaned_data/FormattedDataForModelling/formatted_data_for_modelling_allsensors_{}_outlierremovaleachsensor.csv".format(buffer_size_m)


# ## Run models with cross-validation

# ### Define the error metrics for the cross-validation to return, and the parameters of the cross validation

# In[3]:


error_metrics = ['neg_mean_absolute_error', 'r2', 'neg_root_mean_squared_error', 'neg_mean_absolute_percentage_error']
cv_parameters = KFold(n_splits=10, random_state=1, shuffle=True)


# In[4]:


lr_model_pipeline = Pipeline(steps=[['scaler',StandardScaler()],['linear_regressor',LinearRegression()]])
rf_model_pipeline = Pipeline(steps=[['scaler',StandardScaler()],['rf_regressor', RandomForestRegressor(random_state = 1, n_jobs = 10)]])
xgb_model_pipeline = Pipeline(steps=[['scaler',StandardScaler()],['xgb_regressor',xgb.XGBRegressor(random_state=1, n_jobs = 16)]])
et_model_pipeline = Pipeline(steps=[['scaler',StandardScaler()],['et_regressor',ExtraTreesRegressor (random_state = 1, n_jobs = 16)]])


# In[5]:


models_dict = {"linear_regressor": lr_model_pipeline, "xgb_regressor":xgb_model_pipeline,
               "rf_regressor":rf_model_pipeline}


# ### Prepare data for modelling

# In[6]:


Xfull, Yfull, data_time_columns, index_2019 = prepare_x_y_data(input_csv)


# ### Cut off data post-Covid

# In[45]:

Xfull= Xfull[0:index_2019] # (previously hardcoded to 2643750)
Yfull= Yfull[0:index_2019]
data_time_columns = data_time_columns[0:index_2019]


# ### Choose which month_num and weekday_num option to include

# In[46]:

# Note that in the latest version wher NM integrated new sensors and census data we no longer add the
# weekday (Monday, Tuesday, ....) or month (month_1, month_2) variables, so the only thing to do here is to
# remove the 'day' column that has the string representionat of the day of week (not sure where this came from)
Xfull.drop(['day'], axis=1, inplace = True)

# If using the dummy variables
# Xfull.drop(['Cos_month_num', 'Sin_month_num', 'Cos_weekday_num', 'Sin_weekday_num'], axis=1)

# If using the cyclical variables
#Xfull.drop(['Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday',
#       'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7',
#       'month_8', 'month_9', 'month_10', 'month_11', 'month_12'], axis=1, inplace = True)


# ### Remove year

# In[47]:


del Xfull['year']

# ### Run model with cross validation

# In[ ]:

print("Running models with explanatory variables: ", Xfull.columns)

# Dataframe to store the scores for all the models
error_metric_scores = pd.DataFrame()
# Check the required directories exist
os.makedirs("Results/CV/ComparingModels", exist_ok=True)

for model_name, model_pipeline in models_dict.items():
    print(model_name)
    # Use cross_validate to return the error scores associated with this model and this data
    start = time()
    model_output = cross_validate(model_pipeline, Xfull, Yfull, cv=cv_parameters, scoring=error_metrics, error_score="raise")

    end = time()
    print('Ran in {} minutes'.format(round((end - start)/60),2))
    
    # Formulate the different error scores into a dataframe
    error_metrics_df =pd.DataFrame({'mae': round(abs(model_output['test_neg_mean_absolute_error'].mean()),2), 
                  'mape': round(abs(model_output['test_neg_mean_absolute_percentage_error'].mean()),2),
                  'r2': round(abs(model_output['test_r2'].mean()),2), 
                  'rmse': round(abs(model_output['test_neg_root_mean_squared_error'].mean()),2)},
                 index =[model_name])
        
    # Add evaluation metric scores for this model to the dataframe containing the metrics for each model
    error_metric_scores = pd.concat([error_metric_scores, error_metrics_df])
    # Save error scores for this distance to file
    error_metrics_df.to_csv('Results/CV/ComparingModels/{}_{}m_error_metric_scores_outlierremovaleachsensor.csv'.format(model_name,buffer_size_m),index=False)    

# Save dataframes of error metrics for each buffer distance 
error_metric_scores.to_csv('Results/CV/ComparingModels/comparingmodels_error_metric_scores_outlierremovaleachsensor.csv')   


# ### Print table showing error metrics associated with each model

# In[ ]:





error_metric_scores.to_csv('Results/CV/error_metric_scores_new2.csv')

# In[ ]:


# df= error_metric_scores.copy()
# df = df.reindex(['linear_regressor', 'rf_regressor', 'xgb_regressor'])

