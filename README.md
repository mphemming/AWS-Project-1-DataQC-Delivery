# AWS Project 1: Data QC and Delivery

## Description

This is a repository that will contained code used to process and quality control ocean profiles stored in a private S3 bucket, before releasing to a public S3 bucket for access. 
Eventually, Plots will be created and shared via AWS Simple Email Service (SES) to those who wish to receive. Also, plans to store participant information using AWS Relational Database Service (RDS) which can
securely be accessed. 

Project progress can be tracked here: https://github.com/users/mphemming/projects/2/views/1
Some code used here will be based on the code available here: https://github.com/mphemming/lambda-fishsoop-moana-qc1/tree/main/fishoop-moana-qc1/ops_qc

## Project information

The below sections will contain notes and information useful to replicate the project process.

### IAM user

MFA was enabled for the root user as recommended, and an IAM user 'Michael_developer' with console access and full admin rights was created. This IAM user will be used to work on this project.
The password for this IAM user is stored in Michael's Dashlane account. 

### Regions

I am working within the ap-southeast-2 (Sydney) region. 

### S3 Buckets

An S3 bucket to store the raw and QC'd data was created with the standard option within the ap-southeast-2 (Sydney) region spread across >= 3 AZs. This bucket is called 'aws-project-1-data'. Here raw CSV files, processed and QC'd data will be stored.

Another S3 bucket called 'aws-project-1-code' was created to store useful code. The S3 buckket 'aws-project-1-data-participation' was also created to store participant infromation CSV files.  

## Lambda

### Python Dependencies

The following Python packages are used:

* libnetcdf==0.0.1
* xarray==2024.3.0
* numpy==1.26.4
* netcdf4==1.6.5
* h5py==3.11.0
* boto3==1.34.93

(TO BE UPDATED AS I GO ALONG, also the dependencies folder and zip)

I downloaded the files after searching for the specific package here: https://pypi.org/. 
I then zipped the 'dependencies' folder and named the archive 'dependencies.zip' and uploaded it to the 'aws-project-1-data' S3 bucket.

I used the following command in AWS CloudShell to create the Lambda layer:

```
aws lambda publish-layer-version --layer-name aws-project-1-layer --description "The Lambda Python layer including dependencies required to perform QC and data delivery" --content S3Bucket=aws-project-1-data,S3Key=dependencies.zip --compatible-runtimes python3.12
```

To check that the layer was created, you can use:
```
aws lambda list-layers
```

### Lambda Function notes

For a Lambda function to work, the script needs to contain modules (functions) which can be called. For example, in the TestPackages.py script there is a module called 'lambda_header'.

To upload a script that you want to run within the lambda function, you click on 'upload from' when in the 'code' section. The button is on the righthandside. Then you can copy the URL for code stored in the Amazon S3 location. The code has to be zipped for this to work. 

To get the Lambda function to run the code, you have to scroll down and select 'edit runtime settings'. Here in the 'Handler' cell, you type the script name followed by the module name required, with a dot separating them. For example, to run the module 'Lambda_handler' in 'TestPackages.py', you would write 'TestPackages.lambda_handler' in this 'Handler' cell. 

### Python testing

I test python code locally using the AWS-Project-1-DataQC-Delivery Anaconda environment (see AWS-Project-1-DataQC-Delivery.yml file).


## Participant Information Database

Participant information (e.g. vessel name, Port) is received in an aggregated CSV files exported from JotForm. When the CSV file in an S3 bucket is updated, a trigger will run a lambda function to convert the information into a DynamoDB table (database). Why DynamoDB? it's easy to manage (serverless), can automatically be updated with new columns in future as it is noSQL, it has automated backups, and it's spread across multiple availability zones by default. 

The below steps were taken:

* Store example CSV in S3 bucket 'aws-project-1-data-participation'
* Create a DynamoDB table called 'participant-information' with the following settings: 'user_id' as the partition key (set as a number), no sort key was used, default settings (provisioned)
* Setup Point-in-time recovery (PITR) found in the 'backups' section (didn't do this for this example)
* Setup the permissions so that only the 'Michael_developer' IAM user can read/write into the table. First create an IAM policy in the console. Navigate to 'policies' on the left and click on 'create policy'. Then click on 'json' and copy the code below with the correct Amazon Resource Number (ARN) that can be found in the infromation section for the DynamoDB table. I saved the policy as 'participant-information-dynamoDB'. Then navigate to the 'users' section in the IAM console, find the user 'Michael_developer', click 'add permissions' and then 'attach policies directly' to add the newly-created policy. Then use 'access-analyzer' to test that only 'Michael_developer' can read/write into the table. I created a new 'external access analysis' called 'CheckDynamoDBpermissions'. The policy json code was also copied into the 'Resource-based policy for table' section to ensure that the policy is attached as I was still getting errors. 
* Encryption: All user data stored in Amazon DynamoDB is fully encrypted at rest. No need to do anything. 
* Deletion protection: make sure to turn this on, which can be done in the 'additonal settings' tab.
* I created a script called 'CSV2Dynamo.py' that successfully transfered rows in the 'ParticipationJotForm.CSV' to the DynamoDB table 'participant-information'.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:Query",
                "dynamodb:Scan"
            ],
            "Resource": "arn:aws:dynamodb:region:account-id:table/YourTableName"
        }
    ]
}
```


**Notes:**

Partition key
The partition key is part of the table's primary key. It is a hash value that is used to retrieve items from your table and allocate data across hosts for scalability and availability.

Sort key - optional
You can use a sort key as the second part of a table's primary key. The sort key allows you to sort or search among all items sharing the same partition key.

For extra security, check VPC settings to ensure table cannot be accessed via the web. Depends on how the VPC network and subnets are setup I guess. 

To put items into DynamoDB table, you are required to use AWS access key ID and the associated secret access key. These are different to the IAM user and password used for login to the AWS console. To create the access key ID and secret access key, you can do so by navigating to the IAM console, clicking on the IAM user account and creating them. 

It is important that you respect the data type of the DynamoDB table columns. I have used 'user_id' for the partition key, which is a number, so in the json file you have to specify 'N' (see code example in repo). The other columns are strings, so 'S'.  
