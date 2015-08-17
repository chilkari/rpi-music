#!/usr/bin/python

"""
Script to pull down samples from Amazon S3 to the /samples directory
inside the sampler.

First version is super primitive. There is no 'sync' peresay. Simply 
removes any existing 'samples' directory and redownloads the lot.
"""

import os
import shutil
import yaml
from boto.s3.connection import S3Connection

with open('amazon_credentials.yaml', 'r') as f:
    creds = yaml.load(f)

# Remove existing 'samples' subdirectory
if os.path.exists("samples"):
    print "Existing samples directory. Removing..."
    shutil.rmtree("samples", ignore_errors=True)

print "Creating new empty samples directory..."
os.makedirs('samples')

print 'connecting...'
conn = S3Connection(creds['access_key_id'], creds['secret_access_key'])
print 'connected. Getting bucket...'
bucket = conn.get_bucket('chilkari-raspberry-pi-music')
print 'have bucket. listing keys...'
for key in bucket.get_all_keys(prefix='samples/', delimiter='/'):
    if key.name == 'samples/':
        continue
    print "creating directory {}".format(key.name)
    os.makedirs(key.name)
    os.makedirs(key.name + '/samples')

print 'refetching full list of all keys'
for key in bucket.get_all_keys(prefix='samples/'):
    if key.name.endswith('/'):
        continue
    print "downloading {}".format(key.name)
    res = key.get_contents_to_filename(key.name)
