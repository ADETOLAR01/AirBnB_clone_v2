#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives"""

from fabric.api import env, run, local
from datetime import datetime
import os

env.hosts = ['<54.210.83.3>', '52.205.77.18']
env.user = 'ubuntu'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    if int(number) <= 1:
        number = 1
    else:
        number = int(number)

    archives = sorted(os.listdir('versions'))
    to_delete = archives[:-number]
    if len(to_delete) > 0:
        for archive in to_delete:
            path = os.path.join('versions', archive)
            local('rm {}'.format(path))

    releases = sorted(run('ls /data/web_static/releases').split())
    to_delete = releases[:-number]
    if len(to_delete) > 0:
        for release in to_delete:
            path = '/data/web_static/releases/{}'.format(release)
            run('sudo rm -rf {}'.format(path))
