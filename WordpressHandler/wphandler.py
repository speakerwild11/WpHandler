import os
import time
import subprocess
import atexit

#call :wsl "cd /var/www/html; printf \'ExpiresActive On\nExpiresDefault A1\nHeader append Cache-Control must-revalidate\' >> .htaccess"


def do_proc(command):
    subprocess.call(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)

def install_wp():
    do_proc("wp_install.bat")
    do_proc("wsl --shutdown")
    print("Wordpress successfully installed with the settings in wphandler.conf, and backed up.")

def restore_wp_backup():
    do_proc("wsl --unregister Debian")
    do_proc(f"wsl --import Debian {os.getcwd()} wordpress_instance")
    do_proc("wsl --shutdown")
    print("Wordpress instance has been restored.")

# Pass a command to WSL (aka our debian instance hosting Wordpress)
def wsl(command):
    do_proc(f"<nul set /p =\"{command}\"|wsl -d Debian")

def install_plugin(slug):
    wsl(f"wp plugin install {slug} --path=/var/www/html --activate --allow-root")

def uninstall_plugin(slug):
    wsl(f"wp plugin uninstall {slug} --path=/var/www/html --allow-root")

def start_wp_instance():
    if os.path.isfile(f"{os.getcwd()}\\wordpress_instance"):
        print("Restoring Wordpress instance...")
        restore_wp_backup()
    else:
        print("No Wordpress backup found! Reinstalling Wordpress...")
        install_wp()