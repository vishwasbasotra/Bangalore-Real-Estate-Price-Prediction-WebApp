# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 05:56:10 2020

@author: Vishwas Basotra
"""

# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)
import tensorflow as tf

# importing the dataset
dataset = pd.read_csv('dataset\Bengaluru_House_Data.csv')
print(dataset.head(10))
print(dataset.shape)

# Data preprocessing
## getting the count of area type in the dataset
print(dataset.groupby('area_type')['area_type'].agg('count'))

## droping unnecessary columns
dataset.drop(['area_type','society','availability'], axis='columns', inplace=True)
print(dataset.shape)

## data cleaning
print(dataset.isnull().sum())
dataset.dropna(inplace=True)
print(dataset.shape)

### data engineering
print(dataset['size'].unique())
dataset['bhk'] = dataset['size'].apply(lambda x: x.split(' ')[0])
dataset.drop('size',axis=1, inplace=True)

### rearranging the columns
dataset = dataset[['location','bhk','total_sqft','bath','balcony','price']]  

### exploring 'total_sqft' column
print(dataset['total_sqft'].unique())

#### defining a function to check whether the value is float or not
def is_float(x):
    try:
        float(x)
    except :
        return False
    return True

print(dataset[~dataset['total_sqft'].apply(is_float)].head(10))

#### defining a function to convert the range of column values to a single value
def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None
#### testing the function
print(convert_sqft_to_num('290'))
print(convert_sqft_to_num('2100 - 2850'))
print(convert_sqft_to_num('4.46Sq. Meter'))

#### applying this function to the dataset
dataset['total_sqft'] = dataset['total_sqft'].apply(convert_sqft_to_num)
print(dataset['total_sqft'].head(10))
print(dataset.loc[30])

## feature engineering
print(dataset.head(10))

### creating new colomn 'price_per_sqft' as we know
### in real estate market, price per sqft matters alot. 
dataset['price_per_sqft'] = dataset['price']*100000/dataset['total_sqft']
print(dataset['price_per_sqft'])

### exploring 'location' column
print(len(dataset['location'].unique()))

dataset['location'] = dataset['location'].apply(lambda x: x.strip())

location_stats = dataset.groupby('location')['location'].agg('count').sort_values(ascending=False)
print(location_stats[0:10])

#### creating 'location_stats' to get the location with total count or occurance 
#### occurance, and 'location_stats_less_than_10' to get the location with <= 10 
#### occurance
print(len(location_stats[location_stats <= 10]))
location_stats_less_than_10 = location_stats[location_stats <= 10]
print(location_stats_less_than_10)

#### redefining the 'location' column as 'other' value where location count
#### is <= 10
dataset['location'] = dataset['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
print(dataset['location'].head(10))
print(len(dataset['location'].unique()))
























