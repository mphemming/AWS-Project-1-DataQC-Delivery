
# This code was copied into the Lambda function to run, based on 'CSVDynamo.py' code. 


# %% ---------------------------------------------------
# import packages

import csv
import json
import boto3
import codecs
import logging

# %% ---------------------------------------------------
# functions

def csv_to_json(csv_content):
    json_list = []
    csv_reader = csv.DictReader(csv_content.splitlines())
    for index, row in enumerate(csv_reader, start=1):
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
        
        
def write_to_dynamodb(table_name, json_list):
    dynamodb = boto3.client('dynamodb')
    for item in json_list:
        item_attributes = {key: value for key, value in item.items()}  # Copy item as is
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item_attributes
        )
        
# %% ---------------------------------------------------
# function called in AWS Lambda (use 'CSV2DynamoLambda.lambda_handler')

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'aws-project-1-data-participation'
    csv_key = 'ParticipationJotForm.csv'
    response = s3.get_object(Bucket=bucket_name, Key=csv_key)
    csv_file = response['Body'].read().decode('utf-8')  # Read and decode the content of the StreamingBody object

    json_list = csv_to_json(csv_file)
    
    print("JSON List:", json.dumps(json_list, indent=2))
    
    table_name = 'participant-information'
    write_to_dynamodb(table_name, json_list)

    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully written to DynamoDB')
    }

