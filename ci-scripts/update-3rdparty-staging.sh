#!/bin/bash -e

# This script starts the update chain beginning from staging.

# If no argument is given, spit out help
if [ -z "$1" ]; then
  echo "What does this script do?"
  echo "All 3rdParty mirrors will get updated and snapshots will be created."
  echo "Afterwards the snapshots will be merged with that of jenkins local 3rdParty repo and published to s3."
  echo "Usage: $(basename $0) <LIST_OF_3RD_PARTY_PACAKGE_NAMES>"
  echo "For example: $(basename $0) cloudera saltstack mongodb puppetmaster"
else

PACKAGES=()
for ARG in "$@"
do
	# hack, because of nginx repo issue
	if [ "${ARG}" != "nginx"  ]; then
		echo "Updating mirror ${ARG}"
		aptly mirror update ${ARG}-mirror
	fi

	echo "Create snapshot ${ARG}_${CUSTOM_PACKAGE_VERSION}_snapshot from mirror ${ARG}-mirror"
	aptly snapshot create ${ARG}_${CUSTOM_PACKAGE_VERSION}_snapshot from mirror ${ARG}-mirror

	PACKAGES+=(${ARG})
done

# Create a joined string of all mirrored snapshot names
PACKAGES=( "${PACKAGES[@]/%/_${CUSTOM_PACKAGE_VERSION}_snapshot}" )
bar=$(printf " %s" "${PACKAGES[@]}")
bar=${bar:1}

echo "mirrored snapshots.."
echo  $bar

# snapshot local repo
echo "Create snapshto from local repo 3rdparty-repo"
aptly snapshot create 3rdparty-repo_${CUSTOM_PACKAGE_VERSION}_snapshot from repo 3rdparty-repo

# merge all snapshots
echo "Merge all snapshots together to 3rdparty-s3-repo_${CUSTOM_PACKAGE_VERSION}_snapshot"
aptly snapshot merge 3rdparty-s3-repo_${CUSTOM_PACKAGE_VERSION}_snapshot 3rdparty-repo_${CUSTOM_PACKAGE_VERSION}_snapshot $bar

# publish snapshots
echo "Publish snapshots to s3:3rdparty-staging:"
aptly publish switch precise s3:3rdparty-staging-eu-west-1: 3rdparty-s3-repo_${CUSTOM_PACKAGE_VERSION}_snapshot

# old repo
aptly publish switch precise s3:3rdparty-staging: 3rdparty-s3-repo_${CUSTOM_PACKAGE_VERSION}_snapshot
# create dependency graph
echo "Create dependency graph"
aptly graph

echo "Cleanup Database"
# clean up database
aptly db cleanup

fi
