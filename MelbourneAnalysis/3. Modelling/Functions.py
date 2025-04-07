import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, mean_squared_error,r2_score
import time as thetime
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold
from time import time
from sklearn.model_selection import cross_validate
import datashader as ds
from datashader.mpl_ext import dsshow
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
try:
    from eli5.sklearn import PermutationImportance
except:
    pass
import branca.colormap as cm
import folium
from PIL import Image
import io

def prepare_x_y_data(input_csv):
    # Read in formatted data
    data = pd.read_csv(input_csv, index_col = False)
    data = data.fillna(0)

    # Drop unneeded (mostly string) columns
    data = drop_unneeded_columns(data)
    
    # Get rid of columns in which none of the sensors have a value
    for column in data.columns:
        if np.nanmax(data[column]) ==0:
            del data[column]

    # Filter columns using the regex pattern in function input
    regex_pattern = 'buildings$|street_inf$|landmarks$'
    data = data[data.columns.drop(list(data.filter(regex=regex_pattern)))].copy()
    
    ### Add a random variable (to compare performance of other variables against)
    rng = np.random.RandomState(seed=42)
    data['random'] = np.random.random(size=len(data))
    data["random_cat"] = rng.randint(3, size=data.shape[0])

    # We need the index of the last row for 2019 (need this later)
    index_2019 = data.index[pd.to_datetime(data['datetime']) >= '2020-01-01'][0]

    ## Prepare data for modelling 
    ### Split into predictor/predictand variables
    Xfull = data.drop(['hourly_counts'], axis =1)
    Yfull = data['hourly_counts'].values
       
    ### Store the (non Sin/Cos) time columns and then remove them (Need them later to segment the results by hour of the day)
    data_time_columns = Xfull[['day_of_month_num', 'time', 'weekday_num', 'time_of_day', 'datetime']]
    Xfull = Xfull.drop(['day_of_month_num', 'time', 'weekday_num', 'time_of_day','datetime', 'month_num'],axis=1)

    return Xfull, Yfull, data_time_columns, index_2019


# Code from: https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib/53865762#53865762
def using_datashader(ax, x, y, normalisation):
    df = pd.DataFrame(dict(x=x, y=y))
    dsartist = dsshow(df,ds.Point("x", "y"),ds.count(), vmin=0.1, vmax=100,norm=normalisation,aspect="auto",ax=ax)
    cbar = plt.colorbar(dsartist, ax=ax)
    cbar.ax.tick_params(labelsize=10) 

# Add hour of week variable
def label_hour_of_week (row):                                
    return "w{}_h{}".format(int(row['Weekday']), int(row['Hour']) )

def run_model_with_cv(model,model_name, metrics, cv, X_data, Y_data, regex_name, regex_pattern):
    print("Running {} model, variables include {}".format(model_name,  regex_name))

    # Get list of all features
    feature_list = list(X_data.columns)
        
    # Perform cross validation, time how long it takes
    start = time()
    print("running cross_validate")
    model_output = cross_validate(model, X_data, Y_data, cv=cv, scoring=metrics ,return_estimator=True, error_score="raise")
    print("ran cross_validate")    
    end = time()
    
    #  Create a dataframe containng scores for each performance metric
    df =pd.DataFrame({'mae': round(abs(model_output['test_neg_mean_absolute_error'].mean()),2), 
                      'map': round(abs(model_output['test_neg_mean_absolute_percentage_error'].mean()),2),
                      'r2': round(abs(model_output['test_r2'].mean()),2), 
                      'rmse': round(abs(model_output['test_neg_root_mean_squared_error'].mean()),2)},
                     index =["{}_{}".format(model_name, regex_name)])
    
    # Get the estimators 
    estimators = model_output['estimator']
    
    print('Ran in {} minutes'.format(round((end - start)/60),2))
    return [estimators, df, feature_list]   

def run_model_with_cv_and_predict_new(model,model_name, metrics, cv, X_data, Y_data, buffer_size_m):
    print("Running {} model, buffer size is {}".format(model_name,  buffer_size_m))

    # Get list of all features
    feature_list = list(X_data.columns)
        
    # Perform cross validation, time how long it takes
    start = time()
    print("running cross_validate")
    model_output = cross_validate(model, X_data, Y_data, cv=cv, scoring=metrics ,return_estimator=True, error_score="raise")
    print("ran cross_validate")    
    
    print("running cross_val_predict")
    predictions = cross_val_predict(model, X_data,Y_data,cv=cv)
    print("ran cross_val_predict")   
    end = time()
    
    #  Create a dataframe containng scores for each performance metric
    df =pd.DataFrame({'mae': round(abs(model_output['test_neg_mean_absolute_error'].mean()),2), 
                      'map': round(abs(model_output['test_neg_mean_absolute_percentage_error'].mean()),2),
                      'r2': round(abs(model_output['test_r2'].mean()),2), 
                      'rmse': round(abs(model_output['test_neg_root_mean_squared_error'].mean()),2)},
                     index =["{}_{}".format(buffer_size_m, regex_name)])
    
    # Get the estimators 
    estimators = model_output['estimator']
    
    print('Ran in {} minutes'.format(round((end - start)/60),2))
    return [estimators, df, feature_list, predictions]   

def run_model_with_cv_and_predict(model,model_name, metrics, cv, X_data, Y_data, regex_name, regex_pattern, buffer_size_m):
    print("Running {} model, variables include {}".format(model_name,  regex_name))

    # Get list of all features
    feature_list = list(X_data.columns)
        
    # Perform cross validation, time how long it takes
    start = time()
    print("running cross_validate")
    model_output = cross_validate(model, X_data, Y_data, cv=cv, scoring=metrics ,return_estimator=True, error_score="raise")
    print("ran cross_validate")    
    
    print("running cross_val_predict")
    predictions = cross_val_predict(model, X_data,Y_data,cv=cv)
    print("ran cross_val_predict")   
    end = time()
    
    #  Create a dataframe containng scores for each performance metric
    df =pd.DataFrame({'mae': round(abs(model_output['test_neg_mean_absolute_error'].mean()),2), 
                      'map': round(abs(model_output['test_neg_mean_absolute_percentage_error'].mean()),2),
                      'r2': round(abs(model_output['test_r2'].mean()),2), 
                      'rmse': round(abs(model_output['test_neg_root_mean_squared_error'].mean()),2)},
                     index =["{}_{}".format(buffer_size_m, regex_name)])
    
    # Get the estimators 
    estimators = model_output['estimator']
    
    print('Ran in {} minutes'.format(round((end - start)/60),2))
    return [estimators, df, feature_list, predictions]   

def label_hours (row):
    if row['time'] >6 and row['time'] <= 9:
        return 'morning rush hour'
    elif row['time'] >9 and row['time'] <= 12 :
        return 'morning'
    elif row['time'] >12 and row['time'] <= 15 :
        return 'afternoon'
    elif row['time'] >15 and row['time'] <= 18 :
        return 'afternoon rush hour'    
    elif row['time'] >18 and row['time'] <= 23 :
        return 'evening'    
    elif row['time'] == 23  or row['time'] <= 6 :
        return 'nighttime' 

def select_n_floors(row):
    year = row['datetime'].year
    if year>2020:
        return row.avg_n_floors_2020
    else:
        return row['avg_n_floors_{}'.format(year)]

def select_buildings (row):
    year = row['datetime'].year
    # Add the correct buildings data according to year
    # Building data only up to 2019, so for dates after this, use 2019 data
    if year > 2020:
        return row.buildings_2020
    else:
        return row['buildings_{}'.format(year)]
    
def doubleMADsfromMedian(y, thresh=3.5):
    # Calculate the upper and lower limits
    m = np.median(y) # The median
    abs_dev = np.abs(y - m) # The absolute difference between each y and the median
    # The upper and lower limits are the median of the difference
    # of each data point from the median of the data
    left_mad = np.median(abs_dev[y <= m]) # The left limit (median of lower half)
    right_mad = np.median(abs_dev[y >= m]) # The right limit (median of upper half)
    
    # Now create an array where each value has left_mad if it is in the lower half of the data,
    # or right_mad if it is in the upper half
    y_mad = left_mad * np.ones(len(y)) # Initially every value is 'left_mad'
    y_mad[y > m] = right_mad # Now larger values are right_mad

    # Calculate the z scores for each element
    modified_z_score = 0.6745 * abs_dev / y_mad
    modified_z_score[y == m] = 0
    
    # Return boolean list showing whether each y is an outlier
    return modified_z_score > thresh   


def remove_outliers(sensors):
    # Make a list of true/false for whether the footfall is an outlier
    no_outliers = pd.DataFrame(doubleMADsfromMedian(sensors['hourly_counts']))
    no_outliers.columns = ['outlier'] # Rename the column to 'outlier'

    # Join to the original footfall data to the list of outliers, then select a few useful columns
    join = pd.concat([sensors, no_outliers], axis = 1)
    join = pd.DataFrame(join, columns = ['datetime', 'sensor_id','outlier', 'hourly_counts'])

    # Count the total outlier footfall (a reviewer wanted this)
    total_outlier_footfall = join[join['outlier'] == True]['hourly_counts'].sum()

    # Choose just the outliers
    outliers = join[join['outlier'] == True]
    outliers_list = list(outliers['datetime']) # A list of the days that are outliers

    # Now remove all outliers from the original data
    sensors_without_outliers = sensors.loc[~sensors.index.isin(outliers.index)]
    sensors_without_outliers = sensors_without_outliers.reset_index(drop = True)

    # Check that the lengths all make sense
    assert(len(sensors_without_outliers) == len(sensors)-len(outliers_list))

    #print(f"I found {len(outliers_list)} outliers from {len(join)} days in total. Removing them leaves us with {len(sensors_without_outliers)} events")
    #print(f"{round(len(outliers_list)/len(join) *100,1)}% outliers removed")
    pct = round(len(outliers_list)/len(join) *100,1)     
    return sensors_without_outliers, outliers, pct, total_outlier_footfall

def convert_df_variables_to_dummy(df, variables):
    for variable in variables:
        dummies_this_variable = pd.get_dummies(df[variable], drop_first = True)
        if variable == 'day_of_month':
            dummies_this_variable=dummies_this_variable.add_prefix('d_')
        elif variable == 'time':
            dummies_this_variable=dummies_this_variable.add_prefix('h_')
        df = pd.concat([df,dummies_this_variable], axis=1)
        df=df.drop([variable], axis=1)
    return df

def join_features_to_sensors (features_df, sensors):
    # Reformat
    features_df.reset_index(inplace = True)
    features_df.rename(columns={'index':'sensor_id'}, inplace = True)
    features_df["sensor_id"] = features_df["sensor_id"].astype(int)
    # Join features data to sensor data
    sensors_with_features = sensors.merge(features_df, on='sensor_id', how='left')
    # Set datetime to proper datetime
    sensors_with_features['datetime'] = pd.to_datetime(sensors_with_features['datetime'])
    return sensors_with_features

def perform_linear_regression(df):
    
    # The predictor variables
    Xfull = df.drop(['hourly_counts'], axis =1)

    # The variable to be predicted
    Yfull = df['hourly_counts'].values

    # Split data into training and test sets
    X_train, X_test, Y_train, Y_test = \
    train_test_split(Xfull, Yfull, test_size=0.6666, random_state=123)
    
    #### Standardize both training and testing data
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    #### Fit model
    model = LinearRegression()
    model.fit(X_train, Y_train)

    ### Print results
    print('Training score: ', model.score(X_train, Y_train))
    print('Test score: ', model.score(X_test, Y_test))
    print('CV score: ', (cross_val_score(model, X_train, Y_train)).mean())

    # Make predictions on the testing data
    predictions = model.predict(X_test)
    residuals = pd.DataFrame({'Predictions':predictions,'RealValues': Y_test})
    residuals['residuals'] = residuals.RealValues - residuals.Predictions
    
    # Not sure what this does
    (mean_squared_error(Y_test, predictions))**0.5

    # Collect the model coefficients in a dataframe
    df_coef = pd.DataFrame(model.coef_, index=X_train.columns,
                           columns=['coefficients'])
    # calculate the absolute values of the coefficients to gauge influence (show importance of predictor variables)
    df_coef['coef_abs'] = df_coef.coefficients.abs()

    # Plot the magnitude of the coefficients and... 
#     fig, axs = plt.subplots(nrows=1, ncols=2, figsize = (16,5))
#     axs[0].scatter(residuals['Predictions'], Y_test, s=30, c='r', marker='+', zorder=10)
#     axs[0].plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], c='k', lw=2)
#     axs[0].set_xlabel("Predicted Values - $\hat{y}$")
#     axs[0].set_ylabel("Actual Values MEDV - y")
#     df_coef['coefficients'].sort_values(ascending = False)[:30].plot(kind='barh', ax= axs[1]);
    
    return df_coef, residuals

def create_formatted_df(sensors,features_near_sensors,feature_subtypes_near_sensors, public_holidays, weather, use_subtypes = False):
    # Create month as number not string
    sensors['datetime'] =pd.to_datetime(sensors['datetime'])
    # Keep only data from 2011 onwards
    sensors= sensors[sensors['year']>2010]
    
    #########################################
    # Add data on features within a 100m radius of each sensor
    #########################################   
    if use_subtypes == False:
        # Join features data to sensor data
        sensors_with_features = join_features_to_sensors(features_near_sensors, sensors)

        # Add buildings (correctly for the year the data relates to)
        sensors_with_features['buildings'] = sensors_with_features.apply (lambda row: select_buildings(row), axis=1)
        sensors_with_features= sensors_with_features.drop(['buildings_2010', 'buildings_2011','buildings_2012', 'buildings_2013',
                                                          'buildings_2014','buildings_2015','buildings_2016','buildings_2017',
                                                          'buildings_2018', 'buildings_2019', 'buildings_2020'], axis =1)
    
    else:
        #########################################
        # Add data on subtypes of features within a 100m radius of each sensor
        #########################################
        # Join features data to sensor data
        sensors_with_features = join_features_to_sensors(feature_subtypes_near_sensors, sensors)

        # Create a dataframe containing just the building subttypes for the year that this row refers to
        sensors_with_subfeatures_filtered_buildings = pd.DataFrame(None)
        # For each year, get the data for just that year
        for year in range(2011,2022+1):    
            this_year = sensors_with_features[sensors_with_features['year'] == year]
            # Get just the building columns for this year
            buildings_this_yr = this_year.filter(like='{}'.format(year))
            # Drop all the building columns from the row (and the bikes) 
            this_year = this_year[this_year.columns.drop(list(this_year.filter(regex='bikes|buildings')))]
            # Join the row without any buildings, back to this row 
            this_year = pd.concat([this_year, buildings_this_yr], axis=1)
            this_year.columns = this_year.columns.str.replace(r'_{}'.format(year), '')
            # Join to dataframe which will store data for all years eventually
            sensors_with_subfeatures_filtered_buildings = sensors_with_subfeatures_filtered_buildings.append(this_year)
        sensors_with_features = sensors_with_subfeatures_filtered_buildings.copy()
    
    # Add dummy variables for calendar variables
    sensors_with_features=convert_df_variables_to_dummy(sensors_with_features, ['day', 'month', 'year', 'time'])
    
    # Add in weather data
    weather['datetime'] = pd.to_datetime(weather['datetime'])
    sensors_with_features = sensors_with_features.merge(weather, on='datetime', how='left')
    
    ## Add holidays data
    # Convert date to datetime
    public_holidays['datetime'] = pd.to_datetime(public_holidays['Date'])
    # Rename column to indicate it relates to public holidays, and set values to 1
    public_holidays.rename(columns={'Holiday Name':'public_holiday'}, inplace=True)
    public_holidays['public_holiday'] = 1
    # Drop date column 
    public_holidays = public_holidays.drop(['Date'], axis=1)
    # Join to sensors data
    sensors_with_features = sensors_with_features.merge(public_holidays,how='left', on='datetime')
    # Replace NAs with 0s
    sensors_with_features['public_holiday'] = sensors_with_features['public_holiday'].fillna(0)
    
    # Drop unneeded columns
    sensors_with_features=sensors_with_features.drop(['Latitude', 'Longitude', 'location', 'datetime','mdate'], axis=1)
    
    # Replace NaNs with 0s
    sensors_with_features= sensors_with_features.fillna(0)
    
    return sensors_with_features

# This is based on analysis of how the score changes when the feature is not available
# Thus we need to chose the accuracy score to use
def find_permutation_importance(model, Xfull, Yfull, n_iter):
    # instantiate permuter object
    permuter = PermutationImportance(model, scoring='neg_mean_absolute_error', cv='prefit', n_iter=n_iter)
    permuter.fit(Xfull.values, Yfull)
    # Create a dataframe containing the mean results (and std)
    pi_meanvalues_df = pd.DataFrame({'feature':Xfull.columns,
                  'importance':permuter.feature_importances_,
                  'Feature_importance_std': permuter.feature_importances_std_}).sort_values('importance', ascending = True)
    # Get the raw results for each permutation, and store as a dataframe
    pi_raw_results = permuter.results_  
    raw_importances = pd.DataFrame({'feature_list':list(Xfull.columns)})
    for num,results in enumerate(permuter.results_):
        raw_importances[num] = results
    raw_importances =raw_importances.sort_values(by=0, ascending=False)
    raw_importances.reset_index(drop = True, inplace=True)
    
    # Get just the features that scored more highly than a random feature
    return pi_meanvalues_df, raw_importances

def find_gini_importance(Xfull, model):
    # Get numerical feature importances
    rf_importances = list(model.feature_importances_)
    rf_feature_importances = pd.DataFrame({'feature': Xfull.columns,'importance':rf_importances})      
    rf_feature_importances= rf_feature_importances.sort_values(by = 'importance', ascending = True)
    # Get just the features that scored more highly than a random feature
    rf_feature_importances_overrandom = rf_feature_importances[rf_feature_importances['importance']>rf_feature_importances.query("feature=='random'")["importance"].values[0]]
    return rf_feature_importances


def plot_compare_importances(axs,gini_importances, perm_importances, log_scale = False, above_random_cat = False):
    
    if above_random_cat == 'random_num':
        gini_importances = gini_importances[gini_importances['importance']>gini_importances.query("feature=='random'")["importance"].values[0]]
        perm_importances = perm_importances[perm_importances['importance']>perm_importances.query("feature=='random'")["importance"].values[0]]
    elif above_random_cat == 'random_cat':
        gini_importances = gini_importances[gini_importances['importance']>gini_importances.query("feature=='random_cat'")["importance"].values[0]]
        perm_importances = perm_importances[perm_importances['importance']>perm_importances.query("feature=='random_cat'")["importance"].values[0]]
        
    axs[0].barh(range(len(gini_importances['importance'])), gini_importances["importance"])
    axs[0].set_yticks(range(len(gini_importances["feature"])))
    _ = axs[0].set_yticklabels(np.array(gini_importances["feature"]))
    axs[0].set_title('Gini importance')
    if log_scale == True:
        axs[0].set_xscale('log')

    axs[1].barh(range(len(perm_importances['importance'])),
             perm_importances['importance'],
             xerr=perm_importances['Feature_importance_std'])
    axs[1].set_yticks(range(len(perm_importances['importance'])))
    _ = axs[1].set_yticklabels(perm_importances['feature'])  
    axs[1].set_title('Permutation importance')
    if log_scale == True:
        axs[1].set_xscale('log')

def prepend(list, str):
    # Using format()
    str += '{0}'
    list = [str.format(i) for i in list]
    return(list)

def MAPE(Y_actual,Y_Predicted):
    try:
        mape = np.mean(np.abs((Y_actual - Y_Predicted)/Y_actual))*100
    except:
        mape = np.nan
    return mape

def find_hourly_errors_on_date(special_dates_data, special_date, ylim = None):
    ### Aggregate data by hour (sum or mean)(and remove unneeded columns)
    # Find the sum each hour (across all sensors)
    special_date_hourly_values =special_dates_data.groupby(['Hour']).sum() #mean()
    # Remove extra columns
    special_date_hourly_values.drop(['Weekday', 'sensor_id', 'AbsolouteError', 'Error'], axis=1, inplace=True)

    ### Add error metrics
    special_date_hourly_values['AbsolouteError'] = abs(special_date_hourly_values['Real_vals']-special_date_hourly_values['Predictions'])
    special_date_hourly_values['Error'] = special_date_hourly_values['Real_vals']-special_date_hourly_values['Predictions']
    special_date_hourly_values['Percentage_Increase'] = ((special_date_hourly_values['Real_vals'] - special_date_hourly_values['Predictions']) / abs(special_date_hourly_values['Predictions'])) * 100
    special_date_hourly_values['Mape']  = special_date_hourly_values.apply(lambda x: MAPE(x['Real_vals'], x['Predictions']), axis=1)

    ### Plot the trajectory of the real values and the errors throughout the day
    fig, ax = plt.subplots(figsize = (9,8), sharex = True)
    ax2 = ax.twinx()
    fig = special_date_hourly_values['Predictions'].plot(ax=ax, color='darkred', linewidth=4, legend =False)
    fig = special_date_hourly_values['Real_vals'].plot(ax=ax, color='black', linewidth=4, legend =False)
    fig = special_date_hourly_values['Percentage_Increase'].plot(ax=ax2, color='purple', linewidth=4, legend =False)
    if ylim != None:
        ax2.set_ylim(ylim)

    colors_leg = ['darkred', 'black', 'purple']
    texts = ['Predictions', 'Real values','% Increase'] 
    patches = [ mpatches.Patch(color=colors_leg[i], label="{:s}".format(texts[i]) ) for i in range(len(texts)) ]    

    ax.set_xticks(range(0,len(special_date_hourly_values.index)))
    ax.set_xticklabels(special_date_hourly_values.index, size=15)
    ax.tick_params(axis='both', which='major', labelsize=15, pad=15)
    ax2.tick_params(axis='both', which='major', labelsize=15)
    ax.set_xlabel('Hour', fontsize = 21, labelpad=15)
    ax.set_ylabel ('Count',fontsize=21, labelpad=15)
    ax2.set_ylabel('Percentage Increase in Count', fontsize=21, rotation=270, labelpad=15)

    # ax.set_title(special_date)
    ax.tick_params(axis='x', rotation=90)
    plt.legend(handles=patches, bbox_to_anchor=(0.52, 1.08), loc='center', ncol=3, prop={'size': 20});
    plt.savefig('Results/EvaluateEvents/{}_lines.png'.format(special_date), bbox_inches='tight')
    plt.close() 

def find_sensorly_errors_on_date(special_dates_data, special_date, melbourne_sensors):
    
    ### Aggregate data by hour (sum or mean)(and remove unneeded columns)
    # Find the sum each hour (across all sensors)
    special_date_sensorly_values =special_dates_data.groupby(['sensor_id']).sum()
    # Remove extra columns
    special_date_sensorly_values.drop(['Weekday', 'Percentage_Increase', 'AbsolouteError', 'Error', 'Hour'], axis=1, inplace=True)
    
    ### Add error metrics
    special_date_sensorly_values['AbsolouteError'] = abs(special_date_sensorly_values['Real_vals']-special_date_sensorly_values['Predictions'])
    special_date_sensorly_values['Error'] = special_date_sensorly_values['Real_vals']-special_date_sensorly_values['Predictions']
    special_date_sensorly_values['Percentage_Increase'] = ((special_date_sensorly_values['Real_vals'] - special_date_sensorly_values['Predictions']) / abs(special_date_sensorly_values['Predictions'])) * 100
    
    ### Join back with sensor geographic data
    special_date_sensorly_values = pd.merge(special_date_sensorly_values, melbourne_sensors[['Latitude', 'Longitude', 'sensor_id']], on='sensor_id', how='left')
    special_date_sensorly_values.head()
    
    ### Plot spatially the percentage increase error
    error_metric = 'Percentage_Increase'
    linear = cm.linear.viridis.scale(special_date_sensorly_values[error_metric].min(),special_date_sensorly_values[error_metric].max()).to_step(7)

    # Plot
    f = folium.Figure(width=500, height=400)
    melbourne_map = folium.Map(location= [melbourne_sensors.Latitude.mean() - 0.005,
                               melbourne_sensors.Longitude.mean()- 0.042], tiles="openstreetmap",
                                 zoom_start=14, min_zoom = 13).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(melbourne_map)
    for _, row in special_date_sensorly_values.iterrows():
        folium.CircleMarker([row.Latitude, row.Longitude],
                          popup=row.sensor_id,
                          radius=8,  fill=True, fill_opacity = 1,
                          color = linear(row[error_metric]), fill_color = linear(row[error_metric]),
                          ).add_to(melbourne_map)

    # Add legend
    folium.TileLayer('cartodbpositron').add_to(melbourne_map)
    linear.caption = "Percentage Increase"
    svg_style = '<style>svg#legend {background-color: white;}</style>'
    melbourne_map.get_root().header.add_child(folium.Element(svg_style))
    linear.add_to(melbourne_map)
    
    # Save
    img_data = melbourne_map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save('Results/EvaluateEvents/{}_spatial.png'.format(special_date))
    
    # Crop
    pilImage = Image.open('Results/EvaluateEvents/{}_spatial.png'.format(special_date))
    w, h = pilImage.size
    # im = im.crop((left, top, right, bottom))
    pilImage.crop((870, 5, w+25, h-230)).save('Results/EvaluateEvents/{}_spatial.png'.format(special_date))    
    linear.add_to(melbourne_map)
      
    # For display in Jupyter
    f = folium.Figure(width=200, height=400)
    melbourne_map = folium.Map(location= [melbourne_sensors.Latitude.mean(),
                               melbourne_sensors.Longitude.mean()], tiles="openstreetmap",
                                 zoom_start=13, min_zoom = 13).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(melbourne_map)
    for _, row in special_date_sensorly_values.iterrows():
        folium.CircleMarker([row.Latitude, row.Longitude],
                          popup=row.sensor_id,
                          radius=8,  fill=True, fill_opacity = 1,
                          color = linear(row[error_metric]), fill_color = linear(row[error_metric]),
                          ).add_to(melbourne_map)
    folium.TileLayer('cartodbpositron').add_to(melbourne_map)
    linear.caption = "Percentage Increase"
    svg_style = '<style>svg#legend {background-color: white;}</style>'
    melbourne_map.get_root().header.add_child(folium.Element(svg_style))
    linear.add_to(melbourne_map)    
        
    #display(melbourne_map)

def drop_unneeded_columns(data):
    """
    Drop columns that are not needed for modelling
    :param data: A dataframe containing sensors hourly counts
    :return: The dataframe without the unneeded columns
    """
    return data.drop([
        'sensor_id', 'sensor_name', 'Name', 'installation_date', 'status', 'note', 'Note', 'Location_Type', 'Status'
    ], axis=1) # don't want this included

def buffer_sizes():
    """
    Get the buffer sizes we want to experiment with (so that this isn't hard coded all over the place)
    :return:
    """
    return [50, 100, 200, 400, 500, 600, 1000]