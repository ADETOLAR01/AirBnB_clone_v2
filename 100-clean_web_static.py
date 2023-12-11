from fabric.api import *
import os

env.hosts = ['100.26.231.131', '54.167.92.124']

def do_clean(number=0):[^1^][1]
    number = int(number)

    # Ensure we keep at least one archive if number <= 1
    if number < 2:
        number = 1
    else:
        number += 1  # Include the current archive

    # Delete files in versions folder
    local('ls -dt versions/* | tail -n +{} | xargs rm -rf --'.format(number))

    # Delete files in releases folder on both web servers
    run('ls -dt /data/web_static/releases/* | tail -n +{} | xargs rm -rf --'.format(number))
