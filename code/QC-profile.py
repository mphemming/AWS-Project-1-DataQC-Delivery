# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:30:04 2024

@author: mphem
"""

import tempfile
import os
import boto3
import pandas as pd

def _read_mangopare_csv(self):
        """
        Opens a mangopare csv file in pandas, formats the data, converts to xarray
        """
        self.logger.error("In readers: _read_mangopare_csv")
        try:
            self.start_line = self._calc_header_rows(default_skiprows=self.skip_rows)
            
            # Get the bucket name and object key from the event dictionary
            s3_event = self.event['Records'][0]['s3']
            bucket_name = s3_event['bucket']['name']
            object_key = s3_event['object']['key']
            
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                local_csv_path = os.path.join(temp_dir, "temp.csv")
                
                # Download the S3 object to the local temporary file
                s3_client = boto3.client('s3')
                s3_client.download_file(bucket_name, object_key, local_csv_path)
                
                # Log the filename before reading
                self.logger.info("Reading CSV file: %s", local_csv_path)
                
                # Read the local CSV file using pandas
                self.df = pd.read_csv(
                    local_csv_path,
                    skiprows=self.start_line,
                    on_bad_lines='error',
                    float_precision="round_trip",
                )
        except Exception as exc:
            self.logger.error(
                "Could not read csv file {} due to {}".format(self.filename, exc)
            )
            raise type(exc)(f"Could not read csv file due to: {exc}")