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

### S3 Buckets

An S3 bucket to store the raw and QC'd data was created with the standard option within the ap-southeast-2 (Sydney) region spread across >= 3 AZs. This bucket is called 'aws-project-1-data'. Here raw CSV files, processed and QC'd data will be stored.

Another S3 bucket called 'aws-project-1-code' was created to store useful code. 

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
