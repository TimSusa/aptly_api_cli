#!/bin/bash -e

# Restart aptly server if it is not running
$HOME/bin/aptly-check-port-running.sh

# If no argument is given, spit out help
if [ -z "$1" ]; then
   echo "This script should be used along with jenkins versioning plugin and it will add a package to the local repo, snapshot the repo and publish it to s3."
   echo "Usage: $(basename $0) <PATH_TO> <DEB_PACKAGE_PREFIX> <REPO_PREFIX>"
   echo "For example: $(basename $0) ../ cluster-manager unstable"
else


PATH_TO=$1
DEB_PACKAGE_PREFIX=$2
REPO_PREFIX=$3

echo "Uploading File ${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_amd64.deb to internal repo"
aptly-cli --file_upload ${REPO_PREFIX}-uploads ${PATH_TO}${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_amd64.deb

echo "Adding File to internal repo ${REPO_PREFIX}-repo"
aptly-cli --repo_add_package_from_upload ${REPO_PREFIX}-repo ${REPO_PREFIX}-uploads ${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_amd64.deb

echo "Creating a snapshot from internal repo ${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_snapshot"
aptly-cli --snapshot_create_from_local_repo ${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_snapshot ${REPO_PREFIX}-repo

echo "Publish snapshot to ${REPO_PREFIX}-eu-west-1"
aptly-cli --publish_switch "${REPO_PREFIX}-eu-west-1" "${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_snapshot" "precise" "main" 0

echo "Publish snapshot to ${REPO_PREFIX}-us-east-1"
aptly-cli --publish_switch "${REPO_PREFIX}-us-east-1" "${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}_snapshot" "precise" "main" 0

echo "Cleaning up... "
echo "Remove local package, because it is not needed anymore"
rm ${PATH_TO}${DEB_PACKAGE_PREFIX}_${CUSTOM_PACKAGE_VERSION}*

echo "Delete old snapshots"
aptly-cli --clean_last_snapshots "${DEB_PACKAGE_PREFIX}" 100 "${REPO_PREFIX}"

echo "Delete old packages"
aptly-cli --clean_last_packages "${REPO_PREFIX}-repo" "${DEB_PACKAGE_PREFIX}" 100
fi
