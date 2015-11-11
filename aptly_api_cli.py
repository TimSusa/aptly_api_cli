#! /usr/bin/env python

"""
This is the corresponding client
for the REST API. Call it like:
$ python client.py -h
"""

import os
# if 'REST_API_TESTING' not in os.environ:
#     os.environ['REST_API_TESTING'] = '1'
# if 'REST_API_DEBUG' not in os.environ:
#     os.environ['REST_API_DEBUG'] = '1'

from aptly_cli.cli.cli import main

if __name__ == '__main__':
    main()
