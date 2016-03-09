#!/bin/bash

nc -z localhost 9003
#pgrep aptly
lastRes=$(echo $?)
test $lastRes -gt 0 && printf "Aptly server not running, at specified port. So it will be started now..\n" && sudo start -n aptly &
sleep 5
exit 0
