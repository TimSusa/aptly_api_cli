#!/bin/bash -e

# Called by decide-for-release.sh

# cut out snapshotname
LAST_SNAP=$(aptly-cli --get_last_snapshots "3rdparty-s3-repo" 1 "3rdparty-staging_snapshot")
echo "This is the new snapshot: ${LAST_SNAP}"

# publish snapshots
echo "Publish to ${LAST_SNAP} to 3rdparty-eu-west-1"
aptly-cli --publish_switch "3rdparty-eu-west-1" "${LAST_SNAP}" "precise" "main" 0
echo "Publish to ${LAST_SNAP} to 3rdparty-us-east-1"
aptly-cli --publish_switch "3rdparty-us-east-1" "${LAST_SNAP}" "precise" "main" 0
