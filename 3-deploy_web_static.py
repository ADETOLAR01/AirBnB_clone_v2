#!/usr/bin/env python3
"""Fabric script to distribute archive to web servers"""

import os.path
from fabric.api import env, put, run
from fabric.operations import sudo


env.hosts = ['<54.210.83.3>', '52.205.77.18']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory on server
        put(archive_path, '/tmp/')

        # Get archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_filename)[0]

        # Create directory to uncompress archive
        run('sudo mkdir -p /data/web_static/releases/{}/'
            .format(archive_basename))

        # Uncompress archive into directory
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_basename))

        # Delete archive from server
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Move contents of web_static to archive directory
        run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'
            .format(archive_basename, archive_basename))

        # Remove web_static directory
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_basename))

        # Delete symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create new symbolic link
        run('sudo ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(archive_basename))

        return True

    except Exception:
        return False
