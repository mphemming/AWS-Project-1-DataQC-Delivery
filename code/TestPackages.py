# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:51:20 2024

@author: mphem
"""

import subprocess
import boto3

# Run conda list command to get installed packages
conda_process = subprocess.Popen(['conda', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
conda_output, _ = conda_process.communicate()

# Decode the byte string output and split it into lines
installed_packages = conda_output.decode('utf-8').split('\n')

# Filter out the package versions of xarray and numpy
libnetcdf_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('libnetcdf ')), None)
xarray_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('xarray ')), None)
numpy_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('numpy ')), None)
netcdf4_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('netcdf4 ')), None)
h5py_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('h5py ')), None)
boto3_version = next((pkg.split()[1] for pkg in installed_packages if pkg.startswith('boto3 ')), None)

# Define the file name to save the output
output_file = 'python_packages.txt'

# Write the package versions to a local file
with open(output_file, 'w') as file:
    file.write(f"libnetcdf version: {libnetcdf_version}\n")
    file.write(f"xarray version: {xarray_version}\n")
    file.write(f"numpy version: {numpy_version}\n")
    file.write(f"netcdf4 version: {netcdf4_version}\n")
    file.write(f"h5py version: {h5py_version}\n")
    file.write(f"boto3 version: {boto3_version}\n")

print(f"Package versions saved to '{output_file}'.")

# Upload the file to S3
s3 = boto3.client('s3')
bucket_name = 'aws-project-1-data'
key = 'python_packages.txt'
s3.upload_file(output_file, bucket_name, key)

print(f"File uploaded to S3 bucket: {bucket_name}, with key: {key}.")

