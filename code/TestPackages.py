# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:51:20 2024

@author: mphem
"""

import boto3
import json
import subprocess

def lambda_handler(event, context):
    # Run conda list command to get installed packages
    # Note: You might need to find an alternative way to retrieve package information
    #       since subprocess.Popen is not allowed in Lambda
    # conda_process = subprocess.Popen(['conda', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # conda_output, _ = conda_process.communicate()
    # installed_packages = conda_output.decode('utf-8').split('\n')

    # Dummy package versions for testing
    installed_packages = [
        'libnetcdf 4.8.1',
        'xarray 0.19.0',
        'numpy 1.22.0',
        'netcdf4 1.5.7',
        'h5py 3.3.0',
        'boto3 1.21.24'
    ]

    # Extract package versions
    libnetcdf_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('libnetcdf ')), None)
    xarray_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('xarray ')), None)
    numpy_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('numpy ')), None)
    netcdf4_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('netcdf4 ')), None)
    h5py_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('h5py ')), None)
    boto3_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('boto3 ')), None)

    # Package versions dictionary
    package_versions = {
        'libnetcdf': libnetcdf_version,
        'xarray': xarray_version,
        'numpy': numpy_version,
        'netcdf4': netcdf4_version,
        'h5py': h5py_version,
        'boto3': boto3_version
    }

    # Upload package versions to S3 bucket
    s3 = boto3.client('s3')
    bucket_name = 'aws-project-1-data'
    key = 'python_packages.json'
    s3.put_object(Body=json.dumps(package_versions), Bucket=bucket_name, Key=key)

    return {
        'statusCode': 200,
        'body': json.dumps('Package versions uploaded to S3 bucket successfully.')
    }


