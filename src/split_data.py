import os
import yaml
import pandas as pd
import numpy as np
import argparse
from get_data import read_computing
from sklearn.model_selection import train_test_split #this sub-fuction is used to split the data
from pkgutil import get_data

#Step2:
def split_and_save(config_path):
    config = read_computing(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    split_ratio = config["split_data"]["test_size"]
    random_state = config["base"]["random_state"]
    df = pd.read_csv(raw_data_path, sep=",") #converting raw data to data frames
    print(df)
    train, test = train_test_split(df, test_size=split_ratio, random_state=random_state)
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")

#Step1:
if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="computing.yaml")
    parsed_args=args.parse_args()
    split_and_save(config_path=parsed_args.config)