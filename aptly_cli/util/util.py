#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Util
Instance
"""

import re
# import json
# import sys
from os.path import expanduser, exists
from aptly_cli.api.api import AptlyApiRequests


class Util(object):

    """ Util
    Instance
    """

    def __init__(self):
        """
        Desc
        """
        self.api = AptlyApiRequests()

    @staticmethod
    def _atoi(text):
        """ _atoi
        Desc
        """
        return int(text) if text.isdigit() else text

    def _natural_keys(self, text):
        """ _natural_keys
        Desc
        """
        return [self._atoi(c) for c in re.split('(\\d+)', text)]

    def _sort_out_last_n_snap(self, snaplist, prefix, nr_of_leftover, postfix=None):
        """ _sort_out_last_n_snap
        Input:
        snaplist - List of all Snapshots
        n - Number of items to let over
        Output:
        Returns array of sorted items.
        """
        snapstaginglist = []
        for x in snaplist:
            if prefix in x[u'Name']:
                if postfix is None:
                    # end of string contains
                    snapstaginglist.append(x[u'Name'])
                else:
                    if postfix in x[u'Name']:
                        snapstaginglist.append(x[u'Name'])

        slen = len(snapstaginglist)
        # sort array and print last entry
        snapstaginglist.sort(key=self._natural_keys)
        # print snapstaginglist
        ret = []
        nr_o = int(nr_of_leftover)
        if slen > (nr_o - 1):
            for a in snapstaginglist[-nr_o:]:
                ret.append(a)
        else:
            ret = snapstaginglist

        return ret

    def get_last_snapshots(self, prefix, nr_of_vers, postfix=None):
        """ get_last_snapshots
        Desc
        """
        snaplist = self.api.snapshot_list()
        if postfix is None:
            res = self._sort_out_last_n_snap(snaplist, prefix, nr_of_vers)
        else:
            res = self._sort_out_last_n_snap(snaplist, prefix, nr_of_vers, postfix)

        return res

    def diff_both_last_snapshots_mirrors(self):
        """ diff_both_last_snapshots_mirrors
        DEsc
        """
        local_cfg = self.api.get_config_from_file()
        prefix_list = local_cfg['prefixes_mirrors'].split(', ')

        snaplist = self.api.snapshot_list()
        results = []
        result = ""

        for x in prefix_list:
            res_list = self._sort_out_last_n_snap(snaplist, x, 2)
            if len(res_list) >= 2:
                res = self.api.snapshot_diff(res_list[0], res_list[1])
                if not res:
                    results.append("EMPTY")
                else:
                    results.append(res)
                    break
            else:
                results.append("EMPTY")

        # print results
        result = ""
        for y in results:
            if y == "EMPTY":
                result = "EMPTY"
            else:
                result = y
                break

        print result

    @staticmethod
    def create_init_file():
        """ create_init_file
        """
        home = expanduser("~")
        name = home + '/aptly-cli.conf'

        print "Look for already existing file..."

        if not exists(name):
            print 'Create_init_file'
            try:
                conf = open(name, 'a')   # Trying to create a new file if it does not exist
                conf.write('[general]\nbasic_url=http://localhost\nport=:9003\n')
                conf.close()

            except:
                print('Something went wrong! Can\'t tell what?')

        else:
            print "File already exists! Stop action"
            print name
