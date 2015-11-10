#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
#from requests.exceptions import RequestException
# for cli option parsing:
from optparse import OptionParser

from aptly_api.aptly_api_requests import AptlyApiRequests

def _get_parser_options():
    parser = OptionParser()
    # non argument option
    parser.add_option('--repo_list',
                      action='store_true',
                      help='List all local repos')

    parser.add_option('--repo_create',
                      nargs=1,
                      help='Create local repo', metavar='REPO_NAME [COMMENT] [DISTRIBUTION] [COMPONENT]')

    parser.add_option('--repo_show_packages',
                      nargs=1,
                      help='Shows packages from repo', metavar='REPO_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]')

    parser.add_option('--repo_show',
                      nargs=1,
                      help='Show basic repo-information', metavar='REPO_NAME')

    parser.add_option('--repo_edit',
                      nargs=1,
                      help='Edit repo-information', metavar='REPO_NAME COMMENT DISTRIBUTION COMPONENT')

    parser.add_option('--repo_delete',
                      nargs=1,
                      help='Delete repository', metavar='REPO_NAME')

    parser.add_option('--repo_add_packages_by_key',
                      nargs=2,
                      help='Add packages to local repo by key', metavar='REPO_NAME PACKAGE_REFS')

    parser.add_option('--repo_delete_packages_by_key',
                      nargs=2,
                      help='Delete packages from repository by key', metavar='REPO_NAME PACKAGE_REFS')

    parser.add_option('--file_list_dirs',
                      action='store_true',
                      help='Lists all upload-directories')

    parser.add_option('--file_upload',
                      nargs=2,
                      help='Upload file to local upload-directory', metavar='UPLOAD_DIR FILE')

    parser.add_option('--repo_add_package_from_upload',
                      nargs=3,
                      help='Add package from upload folder to local repo', metavar='REPO_NAME UPLOAD_DIR PACKAGE_NAME')

    parser.add_option('--file_list',
                      action='store_true',
                      help='List uploaded files')

    parser.add_option('--file_delete_dir',
                      nargs=1,
                      help='Delete upload directory', metavar='UPLOAD_DIR')

    parser.add_option('--file_delete',
                      nargs=2,
                      help='Delete a file in upload directory', metavar='UPLOAD_DIR FILE')

    parser.add_option('--snapshot_create_from_local_repo',
                      nargs=2,
                      help='Create snapshot from local repo', metavar='SNAPSHOT_NAME REPO_NAME [DESCRIPTION]')

    parser.add_option('--snapshot_create_by_pack_refs',
                      nargs=3,
                      help='Create snapshot by package references (Please use %20 for spaces for one package reference)',
                      metavar='SNAPSHOT_NAME SOURCE_SNAPSHOTS PACKAGE_REF_LIST [DESCRIPTION]')

    parser.add_option('--snapshot_show',
                      nargs=1,
                      help='Show basic information about snapshot', metavar='SNAPSHOT_NAME')

    parser.add_option('--snapshot_show_packages',
                      nargs=1,
                      help='Show all packages the snapshot is containing or optionally search for one.', metavar='SNAPSHOT_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]')

    parser.add_option('--snapshot_update',
                      nargs=2,
                      help='Rename snapshot and optionally change description', metavar='OLD_SNAPSHOT_NAME NEW_SNAPSHOT_NAME [DESCRIPTION]')

    parser.add_option('--snapshot_list',
                      action='store_true',
                      help='Lists all available snapshots', metavar='[SORT_BY_NAME_OR_TIME]')

    parser.add_option('--snapshot_diff',
                      nargs=2,
                      help='List differences of two snapshots', metavar='LEFT_SNAPSHOT_NAME RIGHT_SNAPSHOT_NAME')

    parser.add_option('--snapshot_delete',
                      nargs=1,
                      help='Delete snapshot by name. Optionally force deletion.', metavar='SNAPSHOT_NAME [FORCE_DELETION]')

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


def main():
    ara = AptlyApiRequests()

    parser = _get_parser_options()
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if options.repo_list:
        ara.repo_list()

    if options.repo_create:
        if len(args) >= 3:
            data.comment=args[0]
            data.default_distribution=args[1]
            data.default_component=args[2]
            ara.repo_create(options.repo_create, data)
        else:
            ara.repo_create(options.repo_create)

    if options.repo_show_packages:
        if len(args) >= 3:
            ara.repo_show_packages(options.repo_show_packages, args[0], args[1], args[2])
        else:
            ara.repo_show_packages(options.repo_show_packages)

    if options.repo_show:
        ara.repo_show(options.repo_show)

    if options.repo_edit:
        if len(args) >= 3:
            data.comment=args[0]
            data.default_distribution=args[1]
            data.default_component=args[2]
            ara.repo_edit(options.repo_edit, data)
        else:
            print 'Wrong usage!'

    if options.repo_delete:
        ara.repo_delete(options.repo_delete)

    if options.file_list_dirs:
        ara.file_list_directories()

    if options.file_upload:
        ara.file_upload(options.file_upload[0], options.file_upload[1])

    if options.repo_add_package_from_upload:
        ara.repo_add_package_from_upload(options.repo_add_package_from_upload[0], options.repo_add_package_from_upload[1], options.repo_add_package_from_upload[2])

    if options.repo_add_packages_by_key:
        print 'repo_add_packages_by_key'
        o = options.repo_add_packages_by_key
        key_list = o[1].split(', ')
        ara.repo_add_packages_by_key(o[0], key_list)

    if options.repo_delete_packages_by_key:
        print 'repo_delete_packages_by_key'
        o = options.repo_delete_packages_by_key
        key_list = o[1].split(', ')
        ara.repo_delete_packages_by_key(o[0], key_list)

    if options.file_list:
        ara.file_list()

    if options.file_delete_dir:
        ara.file_delete_directory(options.file_delete_dir)

    if options.file_delete:
        ara.file_delete(options.file_delete[0], options.file_delete[1])

    if options.snapshot_create_from_local_repo:
        if len(args) >= 1:
            ara.snapshot_create_from_local_repo(options.snapshot_create_from_local_repo[0], options.snapshot_create_from_local_repo[1], args[0])
        else:
            ara.snapshot_create_from_local_repo(options.snapshot_create_from_local_repo[0], options.snapshot_create_from_local_repo[1])

    if options.snapshot_create_by_pack_refs:
        o = options.snapshot_create_by_pack_refs
        l = o[2].split(', ')
        if len(args) >= 1:
            ara.snapshot_create_from_package_refs(o[0], o[1].split(', '), l, args[0])
        else:
            ara.snapshot_create_from_package_refs(o[0], o[1].split(', '), l)


    if options.snapshot_show_packages:
        if len(args) >= 3:
            ara.snapshot_show_packages(options.snapshot_show_packages, args[0], args[1], args[2])
        else:
            ara.snapshot_show_packages(options.snapshot_show_packages)

    if options.snapshot_update:
        if len(args) >= 1:
            ara.snapshot_update(options.snapshot_update[0], options.snapshot_update[1], args[0])

    if options.snapshot_list:
        if len(args) >= 1:
            ara.snapshot_list(args[0])
        else:
            ara.snapshot_list()

    if options.snapshot_diff:
        ara.snapshot_diff(options.snapshot_diff[0], options.snapshot_diff[1])

    if options.snapshot_delete:
        if len(args) >= 1:
            print args[0]
            ara.snapshot_delete(options.snapshot_delete, args[0])
        else:
            ara.snapshot_delete(options.snapshot_delete)

    if options.publish_list:
        ara.publish_list()

    if options.publish:
        if len(args) >= 5:
            ara.publish(options.publish[0], options.publish[1], options.publish[2], options.publish[3], args[0], args[1], args[2], args[3], args[4])
        else:
            ara.publish(options.publish[0], options.publish[1], options.publish[2], options.publish[3])

    if options.publish_switch:
        if len(args) >= 2:
            ara.publish_switch(options.publish_switch[0], options.publish_switch[1], options.publish_switch[2], args[0], args[1])
        else:
            ara.publish_switch(options.publish_switch[0], options.publish_switch[1], options.publish_switch[2])

    if options.publish_drop:
        if len(args) >= 1:
            ara.publish_drop(options.publish_drop[0], options.publish_drop[1], args[0])
        else:
            ara.publish_drop(options.publish_drop[0], options.publish_drop[1])

    if options.package_show_by_key:
        ara.package_show_by_key(options.package_show_by_key)

    if options.get_version:
        ara.get_version()

if __name__ == "__main__":
    sys.exit(main())

