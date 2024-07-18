#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import env, put, run, local
from os.path import exists
env.hosts = ['100.26.239.74', '54.89.96.221']


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        # Get the file name without extension
        file_name = archive_path.split('/')[1].split('.')[0]
        # Create the directory where the archive will be uncompressed
        run('mkdir -p /data/web_static/releases/{}'.format(file_name))
        # Uncompress the archive to the folder on the web server
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.format(file_name, file_name))
        # Delete the archive from the web server
        run('rm /tmp/{}.tgz'.format(file_name))
        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')
        # Create a new the symbolic link /data/web_static/current on the web server
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(file_name))
        return True
    except:
        return False
