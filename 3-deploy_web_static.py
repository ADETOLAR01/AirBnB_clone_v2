from fabric.api import *
import os

env.hosts = ['100.26.231.131', '54.167.92.124']

def do_pack():[^1^][1]
    local("mkdir -p versions")
    archive_path = local("tar -cvzf versions/web_static_$(date '+%Y%m%d%H%M%S').tgz web_static")
    return archive_path

def do_deploy(archive_path):[^2^][2]
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        server_path = "/data/web_static/releases/" + file_name[:-4]
        run("mkdir -p {}".format(server_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, server_path))[^3^][3]
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(server_path, server_path))
        run("rm -rf {}/web_static".format(server_path))[^4^][4]
        run("rm -rf /data/web_static/current")[^5^][5]
        run("ln -s {} /data/web_static/current".format(server_path))
        return True
    except:
        return False

def deploy():[^6^][6]
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
