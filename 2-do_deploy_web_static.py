#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import env, put, run
from os
env.hosts = ['100.26.239.74', '54.89.96.221']


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_folder = archive_filename.split('.')[0]

        # Uncompress the archive to the folder
        run(f'mkdir -p /data/web_static/releases/{archive_folder}')
        run(f'tar -xzf /tmp/{archive_filename} -C /data/web_static/releases/{archive_folder}')
        
        # Delete the archive from the web server
        run(f'rm /tmp/{archive_filename}')

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run(f'ln -s /data/web_static/releases/{archive_folder} /data/web_static/current')

        return True
    except:
        return False
