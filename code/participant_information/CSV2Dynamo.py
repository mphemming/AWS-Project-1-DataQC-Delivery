# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:58:06 2024

@author: mphem
"""

# This script is for testing the code locally on Michael's laptop

# %% ---------------------------------------------------
# import packages

import csv
import json
import boto3
import codecs

# %% ---------------------------------------------------
# functions

def csv_to_json(csv_file):
    json_list = []
    with open(csv_file, 'r', encoding='utf-8-sig') as file:  # Use 'utf-8-sig' to automatically handle BOM
        reader = csv.DictReader(file)
        for index, row in enumerate(reader, start=1):
            # Initialize the JSON row
            json_row = {}
            for key, value in row.items():
                # Determine data type for each attribute
                data_type = 'N' if key == 'user_id' else 'S'
                # Convert each value to string to avoid 'Invalid type' error
                json_row[key.strip('\ufeff')] = {data_type: str(value)}  # Strip BOM from key
            # Add 'user_id' column with row number
            json_row['user_id'] = {'N': str(index)}
            json_list.append(json_row)
    return json_list

def get_csv_from_s3(bucket_name, csv_key):
    s3 = boto3.client('s3')
    temp_file = (r'C:\Users\mphem\OneDrive - UNSW\Work\AWS\AWS_project_1_DataQC' + 
                r'Delivery\AWS-Project-1-DataQC-Delivery\data\temp_csv_file.csv')  
                # Use a temporary file to store the CSV
    s3.download_file(bucket_name, csv_key, temp_file)
    return temp_file

def write_to_dynamodb(table_name, json_list, aws_access_key_id, aws_secret_access_key, aws_region):
    dynamodb = boto3.client('dynamodb', 
                            region_name=aws_region,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    for item in json_list:
        item_attributes = {key: value for key, value in item.items()}  # Copy item as is
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item_attributes
        )

# %% ---------------------------------------------------
# get CSV information and write to DynamoDB table

def main():
    bucket_name = 'aws-project-1-data-participation'
    csv_key = 'ParticipationJotForm.csv'
    temp_csv_file = get_csv_from_s3(bucket_name, csv_key)
    json_list = csv_to_json(temp_csv_file)
    table_name = 'participant-information'
    aws_access_key_id = 'add_access_key'
    aws_secret_access_key = 'add_secret_access_key'
    # aws_session_token = 'your_session_token'  # if using temporary credentials
    aws_region = 'ap-southeast-2'  # Sydney
    write_to_dynamodb(table_name, json_list, aws_access_key_id, aws_secret_access_key, aws_region)


if __name__ == "__main__":
    main()

