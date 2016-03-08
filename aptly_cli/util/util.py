#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Util
Instance
"""

import re
# import json
# import sys
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
        nr_o = self._atoi(nr_of_leftover)
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
        prefix_list = ['cloudera', 'erlang', 'mongodb', 'mongodb2', 'nginx', 'puppetmaster',
                       'rabbitmq', 'redis', 'saltstack2014.7', 'saltstack2015.5', 'saltstack', 'git']
        snaplist = self.api.snapshot_list()
        results = []
        result = ""
        # print "go into loop..."
        for x in prefix_list:
            # print "sort out for prefix..."
            # print x
            res_list = self._sort_out_last_n_snap(snaplist, x, 2)
            if len(res_list) >= 2:
                # print "Diff..."
                res = self.api.snapshot_diff(res_list[0], res_list[1])
                if not res:
                    results.append("EMPTY")
                else:
                    results.append(res)
                    # print "Found..."
                    # print res
                    break
            else:
                results.append("EMPTY")
                # print "Nothing to diff..."

        # print results
        result = ""
        for y in results:
            if y == "EMPTY":
                result = "EMPTY"
            else:
                result = y
                break

        print result
