#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
#from requests.exceptions import RequestException


class AptlyApiRequests(object):

    """
    Instances of this class will be able to talk

    to the Aptly REST API remotely.
    """

    def __init__(self):
        """
        Pass url and port to the constructor
        to initialize instance.
        """
        basic_url = 'http://localhost'
        port = ':9003'
        url = basic_url + port

        # self values
        self.cfg = {
            # Routes
            'route_snap': url + '/api/snapshots/',
            'route_repo': url + '/api/repos/',
            'route_file': url + '/api/files/',
            'route_pack': url + '/api/packages/',
            'route_pub': url + '/api/publish/',
            'route_graph': url + '/api/graph/',
            'route_vers': url + '/api/version/',

            # Number of packages to have left
            'save_last_pkg': 10,

            # Number of snapshots to have left
            'save_last_snap': 3
        }

        self.headers = {'content-type': 'application/json'}

    def _wrap_and_join(self, x):
        return '"{0}"'.format('", "'.join(x))


    def _out(self, x):
        for y in x:
            print y

    ###################
    # LOCAL REPOS API #
    ###################
    def repo_create(self, repo_name, data=None):
        """
        POST /api/repos
        Create empty local repository with specified parameters ( see also aptly repo create).

        JSON body params:
        Name: required, [string] - local repository name
        Comment: [string] - text describing local repository, for the user
        DefaultDistribution: [string] - default distribution when publishing from this local repo
        DefaultComponent: [string] - default component when publishing from this local repo

        HTTP Errors:
        Code  Description
        400 repository with such name already exists
        curl -X POST -H 'Content-Type: application/json' --data '{"Name": "aptly-repo"}' http://localhost:8080/api/repos
        """

        if data is None:
            post_data = {
                'Name': repo_name
            }
        else:
            post_data = {
                'Name': repo_name,
                'Comment': data.comment,
                'DefaultDistribution': data.default_distribution,
                'DefaultComponent': data.default_component
            }

        r = requests.post(self.cfg['route_repo'][:-1],
                          data=json.dumps(post_data),
                          headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data


    def repo_show(self, repo_name):
        """
        SHOW
        GET /api/repos/:name
        Returns basic information about local repository.

        HTTP Errors:
        Code  Description
        404 repository with such name doesn’t exist

        Response:
        Name:  [string]  local repository name
        Comment: [string]  text describing local repository, for the user
        DefaultDistribution: [string]  default distribution when publishing from this local repo
        DefaultComponent:  [string]  default component when publishing from this local repo

        Example:
        $ curl http://localhost:8080/api/repos/aptly-repo
        """
        r = requests.get(
            self.cfg['route_repo'] + repo_name, headers=self.headers)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def repo_show_packages(self, repo_name, package_to_search=None, withDeps = 0, format='compact'):
        """
        SHOW PACKAGES/SEARCH
        GET /api/repos/:name/packages
        List all packages in local repository or perform search on repository contents and return result.

        Query params:
        q - package query, if missing - return all packages
        withDeps - set to 1 to include dependencies when evaluating package query
        format - result format, compact by default ( self, only package keys), details to return full information about each package ( self, might be slow on large repos)

        Example:
        $ curl http://localhost:8080/api/repos/aptly-repo/packages
        """

        if package_to_search is None:
            param = {
                'withDeps': withDeps,
                'format': format
            }
        else:
            param = {
                'q': package_to_search,
                'withDeps': withDeps,
                'format': format
            }
        url =  self.cfg['route_repo'] + repo_name + '/packages'

        r = requests.get( url, params=param, headers=self.headers)
#       raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data

    def repo_edit(self, repo_name, data = None):
        """
        EDIT
        PUT /api/repos/:name
        Update local repository meta information.

        JSON body params:
        Comment: [string]  text describing local repository, for the user
        DefaultDistribution: [string]  default distribution when publishing from this local repo
        DefaultComponent:  [string]  default component when publishing from this local repo

        HTTP Errors:
        Code  Description
        404 repository with such name doesn’t exist
        Response is the same as for GET /api/repos/:name API.

        Example:
        $ curl -X PUT -H 'Content-Type: application/json' --data '{"DefaultDistribution": "trusty"}' http://localhost:8080/api/repos/local1
        """

        if data is None:
            data = {}
        else:
            data = {
                'Comment': data.comment,
                'DefaultDistribution': data.default_distribution,
                'DefaultComponent': data.default_component
            }

        r = requests.put(self.cfg['route_repo'] + repo_name,
                         data=json.dumps(data),
                         headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def repo_list(self):
        """
        LIST
        GET /api/repos
        Show list of currently available local repositories. Each repository is returned as in “show” API.

        Example:
        $ curl http://localhost:8080/api/repos
        """
        r = requests.get(self.cfg['route_repo'], headers=self.headers)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data

    def repo_delete(self, repo_name):
        """
        DELETE
        DELETE /api/repos/:name
        Delete local repository.
        Local repository can’t be deleted if it is published. If local repository has snapshots, aptly would refuse to delete it by default, but that can be overridden with force flag.

        Query params:
        force when value is set to 1, delete local repository even if it has snapshots

        HTTP Errors:
        Code  Description
        404 repository with such name doesn’t exist
        409 repository can’t be dropped ( self, reason in the message)
        """
        r = requests.delete(self.cfg['route_repo'] + repo_name,
                            headers=self.headers)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data

    def repo_add_package_from_upload(self, repo_name, dir_name, file_name = None, params = None):
        """
        ADD PACKAGES FROM UPLOADED FILE/DIRECTORY
        POST /api/repos/:name/file/:dir
        POST /api/repos/:name/file/:dir/:file
        Import packages from files ( uploaded using File Upload API) to the local repository. If directory specified, aptly would discover package files automatically.
        Adding same package to local repository is not an error.
        By default aptly would try to remove every successfully processed file and directory :dir ( if it becomes empty after import).

        Query params:
        noRemove - when value is set to 1, don’t remove any files
        forceReplace - when value is set to 1, remove packages conflicting with package being added ( in local repository)

        HTTP Errors:
        404 repository with such name doesn’t exist

        Response:
        FailedFiles [][string]  list of files that failed to be processed
        Report  object  operation report ( self, see below)

        Report structure:
        Warnings - [][string]  list of warnings
        Added -[][string]  list of messages related to packages being added

        Example ( file upload, add package to repo):
        $ curl -X POST -F file=@aptly_0.9~dev+217+ge5d646c_i386.deb http://localhost:8080/api/files/aptly-0.9
        """
        if file_name is None:
            url = self.cfg['route_repo'] + repo_name + '/file/' + dir_name
        else:
            url = self.cfg['route_repo'] + repo_name + '/file/' + dir_name + '/' + file_name

        if params is not None:
            query_param = {
                'noRemove': param.no_remove,
                'forceReplace': param.force_replace
            }
        else:
            query_param = {
                'noRemove': 0,
                'forceReplace': 0
            }

        r = requests.post(url,
                          params=query_param,
                          headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def repo_add_packages_by_key(self, repo_name, package_key_list):
        """
        ADD PACKAGES BY KEY
        POST /api/repos/:name/packages
        Add packages to local repository by package keys.
        Any package could be added, it should be part of aptly database ( it could come from any mirror, snapshot, other local repository). This API combined with package list ( search) APIs allows to implement importing, copying, moving packages around.
        API verifies that packages actually exist in aptly database and checks constraint that conflicting packages can’t be part of the same local repository.

        JSON body params:
        PackageRefs [][string]  list of package references ( package keys)

        HTTP Errors:
        Code  Description
        400 added package conflicts with already exists in repository
        404 repository with such name doesn’t exist
        404 package with specified key doesn’t exist
        Response is the same as for GET /api/repos/:name API.

        Example
        $ curl -X POST -H 'Content-Type: application/json' --data '{"PackageRefs": ["Psource pyspi 0.6.1-1.4 f8f1daa806004e89","Pi386 libboost-program-options-dev 1.49.0.1 918d2f433384e378"]}' http://localhost:8080/api/repos/repo2/packages
        """
        if len(package_key_list) <= 0:
            print 'No packages were given... aborting'
            return

        url = self.cfg['route_repo'] + repo_name + '/packages'
        param = {
            'PackageRefs': package_key_list
        }
        r = requests.post(url, data=json.dumps(param), headers=self.headers)
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def repo_delete_packages_by_key(self, repo_name, package_key_list):
        """
        DELETE PACKAGES BY KEY
        DELETE /api/repos/:name/packages
        Remove packages from local repository by package keys.
        Any package could be removed from local repository. List package references in local repository could be retrieved with GET /repos/:name/packages.

        JSON body params:
        PackageRefs [][string]  list of package references ( package keys)

        HTTP Errors:
        404 repository with such name doesn’t exist
        Response is the same as for GET /api/repos/:name API.

        Example:
        $ curl -X DELETE -H 'Content-Type: application/json' --data '{"PackageRefs": ["Pi386 libboost-program-options-dev 1.49.0.1 918d2f433384e378"]}' http://localhost:8080/api/repos/repo2/packages
        """
        url = self.cfg['route_repo'] + repo_name + '/packages'
        data = {
            'PackageRefs': package_key_list
        }
        r = requests.delete(url, data=json.dumps(data), headers=self.headers)
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data



    ###################
    # FILE UPLOAD API #
    ###################

    def file_list_directories(self):
        """
        LIST DIRECTORIES
        GET /api/files
        List all directories.
        Response: list of directory names.

        Example:
        $ curl http://localhost:8080/api/files
        """
        r = requests.get(self.cfg['route_file'] , headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)

    def file_upload(self, dir_name, file):
        """
        UPLOAD FILE
        POST /api/files/:dir
        Parameter :dir is upload directory name. Directory would be created if it doesn’t exist.
        Any number of files can be uploaded in one call, aptly would preserve filenames. No check is performed if existing uploaded would be overwritten.
        Response: list of uploaded files as :dir/:file.

        Example:
        $ curl -X POST -F file=@aptly_0.9~dev+217+ge5d646c_i386.deb http://localhost:8080/api/files/aptly-0.9
        """

        f = {
            'file': open(file,'rb')
        }

        r = requests.post(self.cfg['route_file'] + dir_name,
                          files=f)

        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def file_list(self, dir_name = None):
        """
        LIST FILES IN DIRECTORY
        GET /api/files/:dir
        Returns list of files in directory.
        Response: list of filenames.

        HTTP Errors:
        404 - directory doesn’t exist

        Example:
        $ curl http://localhost:8080/api/files/aptly-0.9
        """
        if dir_name is None:
            dir_name = ''

        r = requests.get(self.cfg['route_file'] + dir_name , headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data


    def file_delete_directory(self, dir_name):
        """
        DELETE DIRECTORY
        DELETE /api/files/:dir
        Deletes all files in upload directory and directory itself.

        Example:
        $ curl -X DELETE http://localhost:8080/api/files/aptly-0.9
        """
        r = requests.delete(self.cfg['route_file'] + dir_name, headers=self.headers)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data

    def file_delete(self, dir_name, file_name):
        """
        DELETE FILE IN DIRECTORY
        DELETE /api/files/:dir/:file
        Delete single file in directory.

        Example:
        $ curl -X DELETE http://localhost:8080/api/files/aptly-0.9/aptly_0.9~dev+217+ge5d646c_i386.deb
        """
        r = requests.delete(self.cfg['route_file'] + dir_name + '/' + file_name, headers=self.headers)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        print json.dumps(resp_data)
        return resp_data

    ################
    # SNAPSHOT API #
    ################

    def snapshot_list(self, sort = 'time'):
        """
        LIST
        GET /api/snapshots
        Return list of all snapshots created in the system.

        Query params:
        sort  snapshot order, defaults to name, set to time to display in creation order

        Example:
        $ curl -v http://localhost:8080/api/snapshots
        """
        params = {
            'sort': sort
        }
        r = requests.get(self.cfg['route_snap'], headers=self.headers, params=params)
#        r.raise_for_status()
        resp_data = json.loads(r.content)
        self._out(resp_data)
        return resp_data


    def snapshot_create_from_local_repo(self, snapshot_name, repo_name, description = None):
        """
        CREATE SNAPSHOT FROM LOCAL REPO
        POST /api/repos/:name/snapshots
        Create snapshot of current local repository :name contents as new snapshot with name :snapname.

        JSON body params:
        Name -  [string], required  snapshot name
        Description - [string]  free-format description how snapshot has been created

        HTTP Errors:
        Code  Description
        400 snapshot with name Name already exists
        404 local repo with name :name doesn’t exist

        Example:
        $ curl -X POST -H 'Content-Type: application/json' --data '{"Name":"snap9"}' http://localhost:8080/api/repos/local-repo/snapshots
        """
        url = self.cfg['route_repo'] + repo_name + '/snapshots'
        if description is None:
            description = 'Description for '+ snapshot_name

        data = {
            'Name': snapshot_name,
            'Description': description
        }

        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def snapshot_create_from_package_refs(self, snapshot_name, source_snapshot_list, package_refs_list, description = None):
        """
        CREATE SNAPSHOT FROM PACKAGE REFS
        POST /api/snapshots
        Create snapshot from list of package references.
        This API creates snapshot out of any list of package references. Package references could be obtained from other snapshots, local repos or mirrors.

        Name - [string], required  snapshot name
        Description - [string]  free-format description how snapshot has been created
        SourceSnapshots - [][string]  list of source snapshot names (only for tracking purposes)
        PackageRefs - [][string]  list of package keys which would be contents of the repository
        Sending request without SourceSnapshots and PackageRefs would create empty snapshot.

        HTTP Errors:
        400 snapshot with name Name already exists, package conflict
        404 source snapshot doesn’t exist, package doesn’t exist

        Example:
        $ curl -X POST -H 'Content-Type: application/json' --data '{"Name":"empty"}' http://localhost:8080/api/snapshots
        $ curl -X POST -H 'Content-Type: application/json' --data '{"Name":"snap10", "SourceSnapshots": ["snap9"], "Description": "Custom", "PackageRefs": ["Psource pyspi 0.6.1-1.3 3a8b37cbd9a3559e"]}'  http://localhost:8080/api/snapshots
        """
        url = self.cfg['route_snap'][:-1]
        if description is None:
            description = 'Description for '+ snapshot_name

        print snapshot_name
        print description
        print source_snapshot_list
        print package_refs_list
        data = {
            'Name': snapshot_name,
            'Description': description,
            'SourceSnapshots': source_snapshot_list,
            'PackageRefs': package_refs_list
        }

        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        # r.raise_for_status()
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data



    def snapshot_update(self, old_snapshot_name, new_snapshot_name, description = None):
        """
        UPDATE
        PUT /api/snapshots/:name
        Update snapshot’s description or name.

        JSON body params:
        Name - [string]  new snapshot name
        Description - [string]  free-format description how snapshot has been created

        HTTP Errors:
        404 snapshot with such name doesn’t exist
        409 rename is not possible: name already used by another snapshot

        Example:
        $ curl -X PUT -H 'Content-Type: application/json' --data '{"Name": "snap-wheezy"}' http://localhost:8080/api/snapshots/snap1
        """
        url = self.cfg['route_snap'] + old_snapshot_name
        if description is None:
            description = 'Description for ' + new_snapshot_name

        data = {
            'Name': new_snapshot_name,
            'Description': description
        }

        r = requests.put(url, data=json.dumps(data), headers=self.headers)
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data


    def snapshot_show(self, snapshot_name):
        """
        SHOW
        GET /api/snapshots/:name
        Get information about snapshot by name.

        HTTP Errors:
        Code  Description
        404 snapshot with such name doesn’t exist

        Example:
        $ curl http://localhost:8080/api/snapshots/snap1
        """
        url = self.cfg['route_snap'] + snapshot_name
        r = requests.get(url, headers=self.headers)
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def snapshot_delete(self, snapshot_name, force = '0'):
        """
        DELETE
        DELETE /api/snapshots/:name
        Delete snapshot. Snapshot can’t be deleted if it is published. aptly would refuse to delete snapshot if it has been used as source to create other snapshots, but that could be overridden with force parameter.

        Query params:
        force -  when value is set to 1, delete snapshot even if it has been used as source snapshot

        HTTP Errors:
        404 snapshot with such name doesn’t exist
        409 snapshot can’t be dropped (reason in the message)

        Example:
        $ curl -X DELETE http://localhost:8080/api/snapshots/snap-wheezy
        $ curl -X DELETE 'http://localhost:8080/api/snapshots/snap-wheezy?force=1'
        """
        url = self.cfg['route_snap'] + snapshot_name
        if force == '1':
            print 'Forcing removal of snapshot'

        param = {
            'force': force
        }

        r = requests.delete(url, params=param, headers=self.headers)
        print r.url
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data


    def snapshot_show_packages(self, snapshot_name, package_to_search = None, withDeps = 0, format = 'compact'):
        """
        SHOW PACKAGES/SEARCH
        GET /api/snapshots/:name/packages
        List all packages in snapshot or perform search on snapshot contents and return result.

        Query params:
        q - package query, if missing - return all packages
        withDeps - set to 1 to include dependencies when evaluating package query
        format - result format, compact by default ( only package keys), details to return full information about each package ( might be slow on large snapshots)

        Example:
        $ curl http://localhost:8080/api/snapshots/snap2/packages
        $ curl  http://localhost:8080/api/snapshots/snap2/packages?q='Name%20( ~%20matlab)'
        """
        url = self.cfg['route_snap'] + snapshot_name + '/packages'

        if package_to_search is None:
            param = {
                'withDeps': withDeps,
                'format': format
            }
        else:
            param = {
                'q': package_to_search,
                'withDeps': withDeps,
                'format': format
            }

        r = requests.get(url, params=param, headers=self.headers)
        resp_data = json.loads(r.content)
        print resp_data
        return resp_data

    def snapshot_diff(self, snapshot_left, snapshot_right):
        """
        DIFFERENCE BETWEEN SNAPSHOTS
        GET /api/snapshots/:name/diff/:withSnapshot
        Calculate difference between two snapshots :name (left) and :withSnapshot (right).
        Response is a list of elements:

        Left - package reference present only in left snapshot
        Right - package reference present only in right snapshot

        If two snapshots are identical, response would be empty list.
        null -  package reference right -  snapshot has package missing in left
        package reference -  null -  left snapshot has package missing in right
        package reference - package reference snapshots have different packages

        Example:
        $ curl http://localhost:8080/api/snapshots/snap2/diff/snap3
        """
        url = self.cfg['route_snap'] + snapshot_left + '/diff/' + snapshot_right
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp


    ###############
    # PUBLISH API #
    ###############

    def publish_list(self):
        """
        LIST
        GET /api/publish
        List published repositories.

        Example:
        $ curl http://localhost:8080/api/publish
        """
        url = self.cfg['route_pub']
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp

    def publish(self, prefix, sources_kind, sources_list, distribution_name, component=None, label = None, origin = None, force_overwrite = None, architectures_list = None):
        """
        PUBLISH SNAPSHOT/LOCAL REPO
        POST /api/publish/:prefix
        Publish local repository or snapshot under specified prefix. Storage might be passed in prefix as well, e.g. s3:packages/. To supply empty prefix, just remove last part (POST /api/publish)

        JSON body params:
        SourceKind - [string], required  source kind: local for local repositories and snapshot for snapshots
        Sources -[]Source, required  list of Component/Name objects, Name is either local repository or snpashot name
        Distribution - [string]  distribution name, if missing aptly would try to guess from sources
        Label [string] - value of Label: field in published repository stanza
        Origin  [string] - value of Origin: field in published repository stanza
        ForceOverwrite - bool  when publishing, overwrite files in pool/ directory without notice
        Architectures - [][string]  override list of published architectures

        Notes on Sources field:
        when publishing single component repository, Component may be omitted, it would be guessed from source or set to default value main
        for multiple component published repository, Component would be guessed from source if not set
        GPG signing would happen in aptly server, using local to server gpg binary, keyrings.
        It’s not possible to configure publishing endpoints via API, they should be set in configuration and require aptly server restart.

        HTTP errors:
        400 prefix/distribution is already used by another published repository
        404 source snapshot/repo hasn’t been found

        Example:
        $ curl -X POST -H 'Content-Type: application/json' --data '{"SourceKind": "local", "Sources": [{"Name": "local-repo"}], "Architectures": ["i386", "amd64"], "Distribution": "wheezy"}' http://localhost:8080/api/publish
        $ curl -X POST -H 'Content-Type: application/json' --data '{"SourceKind": "local", "Sources": [{"Name": "0XktRe6qMFp4b8C", "Component": "contrib"}, {"Name": "EqmoTZiVx8MGN65", "Component": "non-free"}], "Architectures": ["i386", "amd64"], "Distribution": "wheezy"}' http://localhost:8080/api/publish/debian_testing/
        """
        url = self.cfg['route_pub'] + prefix

        if component is None:
            print 'WARNING: Component was not given... setting to main'
            component = 'main'


        # Prepare list of sources
        sources = []
        comp_list = component.split()
        list = sources_list.split()
        if len(comp_list) != len(list):
            print "ERROR: sources list and components list should have same length"
            return

        for x in list:
            for y in comp_list:
                row = {
                    'Name': x,
                    'Component': y
                }
        sources.append(row)

        dat = {}
        if label is None:
            if origin is None:
                if force_overwrite is None:
                    if architectures_list is None:
                        print 'simple publish'
                        dat = {
                            'SourceKind': sources_kind,
                            'Sources': sources,
                            'Distribution': distribution_name
                        }
        else:
            print 'fancy publish'
            if int(force_overwrite) <= 0:
                fo = False
            else:
                fo = True
            print fo
            dat = {
                'SourceKind': sources_kind,
                'Sources': sources,
                'Distribution': distribution_name,
                'Architectures': architectures_list.split(),
                'Label': label,
                'Origin': origin,
                'ForceOverwrite': fo
            }

        print dat
        r = requests.post(url, data=json.dumps(dat), headers=self.headers)
        print r.url
        resp = json.loads(r.content)
        print resp
        return resp

    def publish_switch(self, prefix, snapshot_list, distribution, component = None, force_overwrite = 0):
        """
        UPDATE PUBLISHED LOCAL REPO/SWITCH PUBLISHED SNAPSHOT
        PUT /api/publish/:prefix/:distribution
        API action depends on published repository contents:
        if local repository has been published, published repository would be updated to match local repository contents
        if snapshots have been been published, it is possible to switch each component to new snapshot

        JSON body params:
        Snapshots - []Source  only when updating published snapshots, list of objects Component/Name
        ForceOverwrite - bool  when publishing, overwrite files in pool/ directory without notice

        Example:
        $ curl -X PUT -H 'Content-Type: application/json' --data '{"Snapshots": [{"Component": "main", "Name": "8KNOnIC7q900L5v"}]}' http://localhost:8080/api/publish//wheezy
        """
        if prefix is None:
            prefix = ''

        if int(force_overwrite) <= 0:
            fo = False
        else:
            fo = True


        url = self.cfg['route_pub'] + prefix + '/' + distribution

        snap_list_obj = []
        for x in snapshot_list.split():
            if component is not None:
                snap_obj = {
                    'Component': component,
                    'Name': x
                }
            else:
                snap_obj = {
                    'Name': x
                }
            snap_list_obj.append(snap_obj)
        print snap_list_obj
        data = {
            'Snapshots': snap_list_obj,
            'ForceOverwrite': fo
        }
        r = requests.put(url, data=json.dumps(data), headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp


    def publish_drop(self, prefix, distribution, force = 0):
        """
        DROP PUBLISHED REPOSITORY
        DELETE /api/publish/:prefix/:distribution
        Delete published repository, clean up files in published directory.

        Query params:
        force -  force published repository removal even if component cleanup fails
        Usually ?force=1 isn’t required, but if due to some corruption component cleanup fails, ?force=1 could be used to drop published repository. This might leave some published repository files left under public/ directory.

        Example:
        $ curl -X DELETE http://localhost:8080/api/publish//wheezy
        """

        url = self.cfg['route_pub'] + prefix + '/' + distribution

        param = {
            'force': force
        }

        r = requests.delete(url, params=param, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp


    ###############
    # PACKAGE API #
    ###############

    def package_show_by_key(self, package_key):
        """
        SHOW
        GET /api/packages/:key
        Show information about package by package key.
        Package keys could be obtained from various GET .../packages APIs.

        Response:
        Key - [sitring]  package key (unique package identifier)
        ShortKey - [string]  short package key (should be unique in one package list: snapshot, mirror, local repository)
        FilesHash - [string]  hash of package files
        Package Stanza Fields - [string]  all package stanza fields, e.g. Package, Architecture, …

        HTTP Errors:
        Code  Description
        404 package with such key doesn’t exist

        Example:
        $ curl http://localhost:8080/api/packages/'Pi386%20libboost-program-options-dev%201.49.0.1%20918d2f433384e378'
        Hint: %20 is url-encoded space.
        """
        url = self.cfg['route_pack'] + package_key
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp

    #############
    # GRAPH API #
    #############

    def graph(self, file_ext = '.png'):
        """
        GET /api/graph.:ext
        Generate graph of aptly objects ( same as in aptly graph command).
        :ext specifies desired file extension, e.g. .png, .svg.

        Example:
        open url http://localhost:8080/api/graph.svg in browser (hint: aptly database should be non-empty)
        """
        url = self.cfg['route_graph'][:-1] + file_ext
        print url
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp

    ###############
    # VERSION API #
    ###############

    def get_version(self):
        """
        GET /api/version
        Return current aptly version.

        Example:
        $ curl http://localhost:8080/api/version
        """
        url = self.cfg['route_vers']
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        print resp
        return resp
