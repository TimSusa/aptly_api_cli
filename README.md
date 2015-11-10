# UNDER CONSTRUCTION!

# aptly-api-cli
### Why do we need another aptly cli interface?
- Because aptly-api-cli has a lot of more features build in.
- aptly-api-cli is made accessible to the python community


# Description
This python command line interface, executes calls to the Aptly server remotely, without blocking the Aptly database.
All functionality from here http://www.aptly.info/doc/api/ is extended by even more useful features, like clean out last N
snapshots or packages, etc. pp

# Installation

# Command Line Options

## Help
Show this help message and exit
```
-h, --help
```
## Local Repos Api
Local repositories management via REST API.

### List 
List all local repos
```
--repo_list
```

### Create
Create empty local repository with specified parameters. COMMENT,  DISTRIBUTION (e.g.: precise) and COMPONENT (e.g.: main) are optional.

--repo_create=REPO_NAME [COMMENT] [DISTRIBUTION] [COMPONENT]

### Show
Show basic information about a local repository.

--repo_show=REPO_NAME

### Show Package
Show all packages from a local repository. PACKAGE_TO_SEARCH (Name of the Package to search for), WITH_DEPS (e.g.: 0 or zero), FORMAT (e.g.: compact or detail) are optional.

--repo_show_packages=REPO_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]

### Edit
Edit information of a local repository.  

--repo_edit=REPO_NAME COMMENT DISTRIBUTION COMPONENT


### Delete repository
--repo_delete=REPO_NAME

###  Add packages to local repo by key
--repo_add_packages_by_key=REPO_NAME PACKAGE_REFS

###  Delete packages from repository by key
--repo_delete_packages_by_key=REPO_NAME PACKAGE_REFS


### Lists all upload-directories
--file_list_dirs


### Upload file to local upload-directory 
--file_upload=UPLOAD_DIR FILE

### Add package from upload folder to local repo
--repo_add_package_from_upload=REPO_NAME UPLOAD_DIR PACKAGE_NAME

### List uploaded files
--file_list


### Delete upload directory
--file_delete_dir=UPLOAD_DIR


### Delete a file in upload directory
 --file_delete=UPLOAD_DIR FILE

### Create snapshot from local repo
--snapshot_create_from_local_repo=SNAPSHOT_NAME REPO_NAME [DESCRIPTION]


### Create snapshot by package references
--snapshot_create_by_pack_refs=SNAPSHOT_NAME SOURCE_SNAPSHOTS PACKAGE_REF_LIST [DESCRIPTION]


### Show basic information about snapshot
--snapshot_show=SNAPSHOT_NAME


### Show all packages the snapshot is containing or optionally search for one.
--snapshot_show_packages=SNAPSHOT_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]


### Rename snapshot and optionally change description
--snapshot_update=OLD_SNAPSHOT_NAME NEW_SNAPSHOT_NAME [DESCRIPTION]


### Lists all available snapshots
--snapshot_list


### List differences of two snapshots
--snapshot_diff=LEFT_SNAPSHOT_NAME RIGHT_SNAPSHOT_NAME

### Delete snapshot by name. Optionally force deletion.
--snapshot_delete=SNAPSHOT_NAME [FORCE_DELETION]


### List all available repositories to publish to
--publish_list


### Publish snapshot or repository to storage
--publish=PREFIX SOURCES_KIND SOURCES_LIST DISTRIBUTION_LIST [COMPONENT] [LABEL] [ORIGIN] [FORCE_OVERWRITE] [ARCHITECTURES_LIST]


### Drop published repo content
--publish_drop=PREFIX DISTRIBUTION [FORCE_REMOVAL]


### Switching snapshots to published repo with minimal server down time.
--publish_switch=PREFIX SOURCES_LIST DISTRIBUTION [COMPONENT] [FORCE_OVERWRITE]


### Returns aptly version
--get_version


### Show packages by key
--package_show_by_key=PACKAGE_KEY

