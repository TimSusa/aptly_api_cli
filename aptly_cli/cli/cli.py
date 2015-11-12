#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The CLI with option parser
"""

import sys
from optparse import OptionParser

from aptly_cli.api.api import AptlyApiRequests


def main():
    """
    Main entry point for cli.
    """
    obj = AptlyApiRequests()
    parser = _get_parser_opts()
    (opts, args) = parser.parse_args()
    _execute_opts(obj, opts, args)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)


def _get_parser_opts():
    """ _get_parser_opts
    Create parser, options and return object.
    """
    parser = OptionParser()

    parser.add_option('--repo_list',
                      action='store_true',
                      help='List all local repos')

    parser.add_option('--repo_create',
                      nargs=1,
                      help='Create local repo',
                      metavar='REPO_NAME [COMMENT] [DISTRIBUTION] [COMPONENT]')

    parser.add_option('--repo_show_packages',
                      nargs=1,
                      help='Shows packages from repo',
                      metavar='REPO_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]')

    parser.add_option('--repo_show',
                      nargs=1,
                      help='Show basic repo-information',
                      metavar='REPO_NAME')

    parser.add_option('--repo_edit',
                      nargs=1,
                      help='Edit repo-information',
                      metavar='REPO_NAME COMMENT DISTRIBUTION COMPONENT')

    parser.add_option('--repo_delete',
                      nargs=1,
                      help='Delete repository',
                      metavar='REPO_NAME')

    parser.add_option('--repo_add_packages_by_key',
                      nargs=2,
                      help='Add packages to local repo by key',
                      metavar='REPO_NAME PACKAGE_REFS')

    parser.add_option('--repo_delete_packages_by_key',
                      nargs=2,
                      help='Delete packages from repository by key',
                      metavar='REPO_NAME PACKAGE_REFS')

    parser.add_option('--file_list_dirs',
                      action='store_true',
                      help='Lists all upload-directories')

    parser.add_option('--file_upload',
                      nargs=2,
                      help='Upload file to local upload-directory',
                      metavar='UPLOAD_DIR FILE')

    parser.add_option('--repo_add_package_from_upload',
                      nargs=3,
                      help='Add package from upload folder to local repo',
                      metavar='REPO_NAME UPLOAD_DIR PACKAGE_NAME')

    parser.add_option('--file_list',
                      action='store_true',
                      help='List uploaded files')

    parser.add_option('--file_delete_dir',
                      nargs=1,
                      help='Delete upload directory',
                      metavar='UPLOAD_DIR')

    parser.add_option('--file_delete',
                      nargs=2,
                      help='Delete a file in upload directory',
                      metavar='UPLOAD_DIR FILE')

    parser.add_option('--snapshot_create_from_local_repo',
                      nargs=2,
                      help='Create snapshot from local repo',
                      metavar='SNAPSHOT_NAME REPO_NAME [DESCRIPTION]')

    parser.add_option('--snapshot_create_by_pack_refs',
                      nargs=3,
                      help='Create snapshot by package references',
                      metavar='SNAPSHOT_NAME SOURCE_SNAPSHOTS PACKAGE_REF_LIST [DESCRIPTION]')

    parser.add_option('--snapshot_show',
                      nargs=1,
                      help='Show basic information about snapshot',
                      metavar='SNAPSHOT_NAME')

    parser.add_option('--snapshot_show_packages',
                      nargs=1,
                      help='Show all packages the snapshot is containing or optionally search for one.',
                      metavar='SNAPSHOT_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]')

    parser.add_option('--snapshot_update',
                      nargs=2,
                      help='Rename snapshot and optionally change description',
                      metavar='OLD_SNAPSHOT_NAME NEW_SNAPSHOT_NAME [DESCRIPTION]')

    parser.add_option('--snapshot_list',
                      action='store_true',
                      help='Lists all available snapshots',
                      metavar='[SORT_BY_NAME_OR_TIME]')

    parser.add_option('--snapshot_diff',
                      nargs=2,
                      help='List differences of two snapshots',
                      metavar='LEFT_SNAPSHOT_NAME RIGHT_SNAPSHOT_NAME')

    parser.add_option('--snapshot_delete',
                      nargs=1,
                      help='Delete snapshot by name. Optionally force deletion.',
                      metavar='SNAPSHOT_NAME [FORCE_DELETION]')

    parser.add_option('--publish_list',
                      action='store_true',
                      help='List all available repositories to publish to')

    parser.add_option('--publish',
                      nargs=4,
                      help='Publish snapshot or repository to storage',
                      metavar='PREFIX SOURCES_KIND SOURCES_LIST DISTRIBUTION_LIST [COMPONENT] [LABEL] [ORIGIN] [FORCE_OVERWRITE] [ARCHITECTURES_LIST]')

    parser.add_option('--publish_drop',
                      nargs=2,
                      help='Drop published repo content',
                      metavar='PREFIX DISTRIBUTION [FORCE_REMOVAL]')

    parser.add_option('--publish_switch',
                      nargs=3,
                      help='Switching snapshots to published repo with minimal server down time.',
                      metavar='PREFIX SOURCES_LIST DISTRIBUTION [COMPONENT] [FORCE_OVERWRITE]')

    parser.add_option('--get_version',
                      action='store_true',
                      help='Returns aptly version')

    parser.add_option('--package_show_by_key',
                      nargs=1,
                      help='Show packages by key',
                      metavar='PACKAGE_KEY')
    return parser


def _execute_opts(obj, opts, args):
    """ _execute_opts
    Execute functions due to options and arguments.
    """
    class Data:
        """
        Create dat object and use it as argument.
        """
        def __init__(self):
            pass

    if opts.repo_list:
        obj.repo_list()

    if opts.repo_create:
        if len(args) >= 3:
            Data.comment = args[0]
            Data.default_distribution = args[1]
            Data.default_component = args[2]
            obj.repo_create(opts.repo_create, Data)
        else:
            obj.repo_create(opts.repo_create)

    if opts.repo_show_packages:
        if len(args) >= 3:
            obj.repo_show_packages(
                opts.repo_show_packages, args[0], args[1], args[2])
        else:
            obj.repo_show_packages(opts.repo_show_packages)

    if opts.repo_show:
        obj.repo_show(opts.repo_show)

    if opts.repo_edit:
        if len(args) >= 3:
            Data.comment = args[0]
            Data.default_distribution = args[1]
            Data.default_component = args[2]
            obj.repo_edit(opts.repo_edit, Data)
        else:
            print 'Wrong usage!'

    if opts.repo_delete:
        obj.repo_delete(opts.repo_delete)

    if opts.file_list_dirs:
        obj.file_list_directories()

    if opts.file_upload:
        obj.file_upload(opts.file_upload[0], opts.file_upload[1])

    if opts.repo_add_package_from_upload:
        o = opts.repo_add_package_from_upload
        obj.repo_add_package_from_upload(o[0], o[1], o[2])

    if opts.repo_add_packages_by_key:
        print 'repo_add_packages_by_key'
        o = opts.repo_add_packages_by_key
        key_list = o[1].split(', ')
        obj.repo_add_packages_by_key(o[0], key_list)

    if opts.repo_delete_packages_by_key:
        print 'repo_delete_packages_by_key'
        o = opts.repo_delete_packages_by_key
        key_list = o[1].split(', ')
        obj.repo_delete_packages_by_key(o[0], key_list)

    if opts.file_list:
        obj.file_list()

    if opts.file_delete_dir:
        obj.file_delete_directory(opts.file_delete_dir)

    if opts.file_delete:
        obj.file_delete(opts.file_delete[0], opts.file_delete[1])

    if opts.snapshot_create_from_local_repo:
        o = opts.snapshot_create_from_local_repo
        if len(args) >= 1:
            obj.snapshot_create_from_local_repo(o[0], o[1], args[0])
        else:
            obj.snapshot_create_from_local_repo(o[0], o[1])

    if opts.snapshot_create_by_pack_refs:
        o = opts.snapshot_create_by_pack_refs
        l = o[2].split(', ')
        if len(args) >= 1:
            obj.snapshot_create_from_package_refs(
                o[0], o[1].split(', '), l, args[0])
        else:
            obj.snapshot_create_from_package_refs(o[0], o[1].split(', '), l)

    if opts.snapshot_show_packages:
        o = opts.snapshot_show_packages
        if len(args) >= 3:
            obj.snapshot_show_packages(o, args[0], args[1], args[2])
        else:
            obj.snapshot_show_packages(o)

    if opts.snapshot_update:
        o = opts.snapshot_update
        if len(args) >= 1:
            obj.snapshot_update(o[0], o[1], args[0])

    if opts.snapshot_list:
        if len(args) >= 1:
            obj.snapshot_list(args[0])
        else:
            obj.snapshot_list()

    if opts.snapshot_diff:
        obj.snapshot_diff(opts.snapshot_diff[0], opts.snapshot_diff[1])

    if opts.snapshot_delete:
        if len(args) >= 1:
            print args[0]
            obj.snapshot_delete(opts.snapshot_delete, args[0])
        else:
            obj.snapshot_delete(opts.snapshot_delete)

    if opts.publish_list:
        obj.publish_list()

    if opts.publish:
        o = opts.publish
        if len(args) >= 5:
            obj.publish(
                o[0], o[1], o[2], o[3], args[0], args[1], args[2], args[3], args[4])
        else:
            obj.publish(o[0], o[1], o[2], o[3])

    if opts.publish_switch:
        o = opts.publish_switch
        if len(args) >= 2:
            obj.publish_switch(o[0], o[1], o[2], args[0], args[1])
        else:
            obj.publish_switch(o[0], o[1], o[2])

    if opts.publish_drop:
        o = opts.publish_drop
        if len(args) >= 1:
            obj.publish_drop(o[0], o[1], args[0])
        else:
            obj.publish_drop(o[0], o[1])

    if opts.package_show_by_key:
        obj.package_show_by_key(opts.package_show_by_key)

    if opts.get_version:
        obj.get_version()

if __name__ == "__main__":
    sys.exit(main())
