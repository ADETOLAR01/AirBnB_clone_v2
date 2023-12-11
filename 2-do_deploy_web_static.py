from fabric.api import env, put, run
from os.path import exists

# define hosts
env.hosts = ['100.26.231.131', '54.167.92.124']

def do_deploy(archive_path):[^1^][1]
    # check if archive_path exists
    if not exists(archive_path):
        return False

    try:
        # upload the archive to the /tmp/ directory of the web server[^2^][2]
        put(archive_path, "/tmp/")
        
        # define variables
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        releases_path = "/data/web_static/releases"
        tmp_path = "/tmp/" + file_name
        current_path = releases_path + "/" + no_ext
        
        # uncompress the archive to the folder on the web server[^3^][3]
        run("mkdir -p " + current_path)
        run("tar -xzf " + tmp_path + " -C " + current_path)[^4^][4][^5^][5]
        
        # delete the archive from the web server[^6^][6]
        run("rm " + tmp_path)
        
        # move files
        run("mv " + current_path + "/web_static/* " + current_path)
        
        # delete the symbolic link /data/web_static/current from the web server[^7^][7]
        run("rm -rf /data/web_static/current")[^8^][8][^9^][9]
        
        # create a new the symbolic link /data/web_static/current on the web server[^7^][7]
        run("ln -s " + current_path + " /data/web_static/current")
        
        return True
    except:
        return False
