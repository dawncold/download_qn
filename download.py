# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function, division
import os
import sys
import requests
import qiniu

if not os.path.exists('.config'):
    print('can not find config file on {}'.format(os.getcwd()))
    sys.exit(-1)

with open('.config') as f:
    lines = f.readlines()
config = {}
for line in lines:
    if not line.strip():
        continue
    k, v = line.split('=')
    config[k] = v


q = qiniu.Auth(config['AK'], config['SK'])

bucket = qiniu.BucketManager(q)

bucket_names, resp = bucket.buckets()

if resp.status_code != 200:
    print(resp.status_code)
    print(resp.text_body)
    sys.exit(-1)

bucket_name = bucket_names[0]

result = bucket.list(bucket_name)

bucket_data = result[0]
resp = result[2]

if resp.status_code != 200:
    print(resp.text_body)

bucket_keys = []
for item in bucket_data['items']:
    bucket_keys.append(item['key'])


for bucket_key in bucket_keys:
    url = '{}/{}'.format(config['DOMAIN'], bucket_key)
    rsp = None
    try:
        rsp = requests.get(url)
        rsp.raise_for_status()
    except requests.HTTPError:
        print('error: {}'.format(url))
    else:
        with open(bucket_key, mode='wb+') as f:
            f.write(rsp.content)
