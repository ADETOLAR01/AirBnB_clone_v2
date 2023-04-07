from fabric.api import *
from datetime import datetime

env.hosts = ['<54.210.83.3>']
env.user = '<156689-web-01>'
env.key_filename = '<~/.ssh/your_ssh_key_file>'

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Get the current time and date
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the name of the archive
        archive_name = "web_static_" + timestamp + ".tgz"

        # Compress the web_static folder into a tgz archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path if it has been correctly generated
        return "versions/{}".format(archive_name)

    except:
        # Return None if there was an error generating the archive
        return None
