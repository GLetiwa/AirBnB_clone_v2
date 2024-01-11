#!/usr/bin/python3
"""Fabric script to create and deploy web_static to web servers"""

from fabric.api import local, env
from os.path import exists
from datetime import datetime
from fabric.api import run
from fabric.api import put


env.hosts = ['100.26.151.199', '52.91.156.173']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """Generates a .tgz archive from web_static folder"""

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create the archive filename using the current timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    # Create the .tgz archive
    result = local("tar -czvf versions/{} web_static".format(archive_name))

    # Check if the archive has been correctly generated
    if result.succeeded:
        archive_path = "versions/{}".format(archive_name)
        print("web_static packed: {}".format(archive_path))
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """Deploys an archive to the web servers"""

    # Check if the archive_path exists
    if not exists(archive_path):
        return False

    # Extract filename without extension
    archive_name = archive_path.split('/')[-1]
    folder_name = archive_name.split('.')[0]

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Create the folder /data/web_static/releases/<archive_name without extension>
        run("mkdir -p /data/web_static/releases/{}".format(folder_name))

        # Uncompress the archive to /data/web_static/releases/<archive_name without extension>
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(archive_name, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Delete the symbolic link /data/web_static/current
        run("rm -f /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

def deploy():
    """Creates and deploys web_static to web servers"""

    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call the do_deploy(archive_path) function
    return do_deploy(archive_path)

if __name__ == "__main__":
    # Use this script to deploy on servers: xx-web-01 and xx-web-02
    deploy()
