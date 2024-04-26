# AWS Project 1: Data QC and Delivery

## Description

This is a repository that will contained code used to process and quality control ocean profiles stored in a private S3 bucket, before releasing to a public S3 bucket for access. 
Eventually, Plots will be created and shared via AWS Simple Email Service (SES) to those who wish to receive. Also, plans to store participant information using AWS Relational Database Service (RDS) which can
securely be accessed. 

Project progress can be tracked here: https://github.com/users/mphemming/projects/2/views/1

## Project information

The below sections will contain notes and information useful to replicate the project process.

### IAM user

MFA was enabled for the root user as recommended, and an IAM user 'Michael_developer' with console access and full admin rights was created. This IAM user will be used to work on this project.
The password for this IAM user is stored in Michael's Dashlane account. 

### S3 Buckets

An S3 bucket to store the raw and QC'd data was created. This bucket is called 'aws-project-1-data'. 
