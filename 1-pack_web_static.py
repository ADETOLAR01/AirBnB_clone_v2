from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Path to the generated archive if successful, None otherwise.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive filename (web_static_<year><month><day><hour><minute><second>.tgz)
        now = datetime.utcnow()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Create the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the generated archive
        return os.path.join("versions", archive_name)
    except Exception as e:
        # Return None if an exception occurs
        return None
