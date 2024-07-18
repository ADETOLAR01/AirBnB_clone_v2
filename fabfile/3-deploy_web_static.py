# fabfile/3-deploy_web_static.py


from fabric import task
from fabric.connection import Connection
from datetime import datetime
from os.path import exists, isdir
import os

env_hosts = ['100.26.239.74', '54.89.96.221']
env_user = 'ubuntu'
env_key = '~/.ssh/id_rsa'


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            os.makedirs("versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local_command = "tar -cvzf {} web_static".format(file_name)
        os.system(local_command)
        return file_name
    except Exception as e:
        print(f"Error: {e}")
        return None


def do_deploy(c, archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = os.path.basename(archive_path)
        no_ext = os.path.splitext(file_n)[0]
        path = "/data/web_static/releases/"
        c.put(archive_path, '/tmp/')
        c.run(f'mkdir -p {path}{no_ext}/')
        c.run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        c.run(f'rm /tmp/{file_n}')
        c.run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        c.run(f'rm -rf {path}{no_ext}/web_static')
        c.run('rm -rf /data/web_static/current')
        c.run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@task
def deploy(c):
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(c, archive_path)


@task
def deploy_all(c):
    for host in env_hosts:
        connection = Connection(host=host, user=env_user, connect_kwargs={"key_filename": env_key})
        deploy(connection)
