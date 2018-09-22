#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:57:27 2018

@author: saramelvin
"""
import pandas as pd
import pickle as pkl 

def read_in_sample():
    data_all = pd.read_csv("AIS_LA_SD_Jan_1_to_15_2016_Filtered_by_Proximity.csv") 
    data_true_pos = pd.read_csv("Example_COLREGs_Interactions_UTM11.csv")

    data_sample = data_all.head()
    
    return data_sample, data_true_pos

if __name__ == "__main__":
    sample_data, pos_sample = sample_input = read_in_sample()
    pkl.dump(sample_data, open("sample_data.p","wb"))
    pkl.dump(pos_sample, open("pos_sample.p","wb"))
