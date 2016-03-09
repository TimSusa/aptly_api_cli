#!/bin/bash

# Decide, if the staging snapshot should also be published to production

res=$(aptly-cli --diff_both_last_snapshots_mirrors)

if [ "${res}" == "EMPTY"  ]; then
		echo "New snapshot has no new packages. No need to release to production!"
	    exit 0
else
	echo "New packages were found..."
	/var/lib/jenkins/bin/publish-3rdParty-production.sh
fi

aptly-cli --clean_mirrored_snapshots
