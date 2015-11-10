# aptly-api-cli
Why do we need another aptly cli interface?
- Because aptly-api-cli has a lot of more features build in.

# Description
Implementation that fullfils the following documentation http://www.aptly.info/doc/api/

# Installation

# Features

# Command Line Options

### -h, --help
Show this help message and exit

### --repo_list
List all local repos

### --repo_create=REPO_NAME [COMMENT] [DISTRIBUTION] [COMPONENT]
Create local repo

###   --repo_show_packages=REPO_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]
Shows packages from repo

###  --repo_show=REPO_NAME
Show basic repo-information

###   --repo_edit=REPO_NAME COMMENT DISTRIBUTION COMPONENT
Edit repo-information

###   --repo_delete=REPO_NAME
Delete repository

###  --repo_add_packages_by_key=REPO_NAME PACKAGE_REFS
Add packages to local repo by key

###  --repo_delete_packages_by_key=REPO_NAME PACKAGE_REFS
Delete packages from repository by key

### --file_list_dirs
Lists all upload-directories

### --file_upload=UPLOAD_DIR FILE
Upload file to local upload-directory

### --repo_add_package_from_upload=REPO_NAME UPLOAD_DIR PACKAGE_NAME
Add package from upload folder to local repo

### --file_list
List uploaded files

### --file_delete_dir=UPLOAD_DIR
Delete upload directory

### --file_delete=UPLOAD_DIR FILE
Delete a file in upload directory

### --snapshot_create_from_local_repo=SNAPSHOT_NAME REPO_NAME [DESCRIPTION]
Create snapshot from local repo

### --snapshot_create_by_pack_refs=SNAPSHOT_NAME SOURCE_SNAPSHOTS PACKAGE_REF_LIST [DESCRIPTION]
Create snapshot by package references

### --snapshot_show=SNAPSHOT_NAME
Show basic information about snapshot

### --snapshot_show_packages=SNAPSHOT_NAME [PACKAGE_TO_SEARCH] [WITH_DEPS] [FORMAT]
Show all packages the snapshot is containing or optionally search for one.

### --snapshot_update=OLD_SNAPSHOT_NAME NEW_SNAPSHOT_NAME [DESCRIPTION]
Rename snapshot and optionally change description

### --snapshot_list
Lists all available snapshots

### --snapshot_diff=LEFT_SNAPSHOT_NAME RIGHT_SNAPSHOT_NAME
List differences of two snapshots

### --snapshot_delete=SNAPSHOT_NAME [FORCE_DELETION]
Delete snapshot by name. Optionally force deletion.

### --publish_list
List all available repositories to publish to

### --publish=PREFIX SOURCES_KIND SOURCES_LIST DISTRIBUTION_LIST [COMPONENT] [LABEL] [ORIGIN] [FORCE_OVERWRITE] [ARCHITECTURES_LIST]
Publish snapshot or repository to storage

### --publish_drop=PREFIX DISTRIBUTION [FORCE_REMOVAL]
Drop published repo content

### --publish_switch=PREFIX SOURCES_LIST DISTRIBUTION [COMPONENT] [FORCE_OVERWRITE]
Switching snapshots to published repo with minimal server down time.

### --get_version
Returns aptly version

### --package_show_by_key=PACKAGE_KEY
Show packages by key
