import pandas as pd
import numpy as np

def select_buildings (row):
    # Add the correct buildings data according to year
    # Building data only up to 2019, so for dates after this, use 2019 data
    if row.year > 2020:
        return row.buildings_2019
    else:
        return row['buildings_{}'.format(row.year)]
    
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

    # Choose just the outliers
    outliers = join[join['outlier'] == True]
    outliers_list = list(outliers['datetime']) # A list of the days that are outliers

    # Now remove all outliers from the original data
    df = sensors.loc[~sensors.index.isin(outliers.index)]
    df = df.reset_index(drop = True)

    # Check that the lengths all make sense
    assert(len(df) == len(sensors)-len(outliers_list))

    print("I found {} outliers from {} days in total. Removing them leaves us with {} events".format(\
        len(outliers_list), len(join), len(df) ) )

    return df

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

    return sensors_with_features