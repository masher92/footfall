# Predicting Pedestrian Footfall: <br /> Location Data Analysis of Melbourne, Australia

## Table of Contents
* [Downloading data](#downloading-data)
* [Preparing data](#preparing-data)
* [Analysing data](#analysing-data)
* [Modelling](#modelling)

<a name="downloading-data"></a>
## Downloading data

Footfall data is downloaded by selecting 'Export --> CSV' from: 
* https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-Monthly-counts-per-hour/b2ak-trbp 

Weather data is downloaded from: https://www.timeanddate.com/weather/australia/melbourne/historic. 

Data on other features is downloaded from: https://data.melbourne.vic.gov.au/. Including data on:
* [Lighting](https://data.melbourne.vic.gov.au/City-Council/Feature-Lighting-including-light-type-wattage-and-/4j42-79hg)
* [Landmarks](https://data.melbourne.vic.gov.au/People/Landmarks-and-places-of-interest-including-schools/j5vt-ppat)
* [Street furniture](https://data.melbourne.vic.gov.au/widgets/8fgn-5q6t?mobile_redirect=true)
* [Buildings](https://data.melbourne.vic.gov.au/Property/Buildings-with-name-age-size-accessibility-and-bic/pmhb-s6pn)
* [Bike share dock locations](https://data.melbourne.vic.gov.au/w/vrwc-rwgm/spy9-nmud?cur=l0YdZo6QE_m&from=88D7wUgzKYw)

Other possible interesting sources of data to include: social indicators (affluence of area?); tree canopies (green space?; live music venues; Super Sunday bike count;
Metro Train Stations with Accessibility Information (landmarks only has Railway Station', 'Transport Terminal', 'Marina', 'Bridge' under transport sub-themes - mero stations might feature in transport terminal but would need to check); playgrouns? Cafe, restaurant, bistro seats; Bar, tavern, pub patron capacity; taxi ranks; public toilets; bus stop locations.

<a name="preparing-data"></a>
## Preparing data

This directory contains two scripts which clean and reformat the footfall and feature data, and save cleaned versions to the Cleaned_data directory:
* CleaningData-Footfall.ipynb 
* CleaningData-OtherFeatures.ipynb

And one script which scrapes the weather data from the Melbourne historic weather website, cleans the data, and saves yearly weather csvs to the Cleaned_data directory:
* ScrapingWeatherData.ipynb

The outputs from this are:
* bikes_clean.csv - columns: station_id, capacity, latitude, longitude
* buildings_clean.csv - year, n_floors, building_type, access_type, access_rating, latitude, longitude
* landmarks_clean.csv - theme, subtheme, featurename, latitude, longitude
* lights_clean.csv - , latitude, longitude
* street_inf_clean.csv - lamptype_lupvalue, lamp-rating_w, latitude, longitude
* weather_data_{year}.csv - datetime (hourly), Temp,	Humidity,	Pressure,	Rain, (binary 1 or 0),	WindSpeed

<a name="analysing-data"></a>
## Analysing data

<a name="modelling"></a>
## Modelling
