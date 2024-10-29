import os

import subprocess

import time

from pathlib import Path



# Get current time

now = time.time()



# Directory where packages are installed

site_packages_dir = Path(subprocess.check_output(['python3', '-m', 'site', '--user-site']).strip().decode())



# List packages modified in the last 24 hours

recent_packages = []

for pkg in site_packages_dir.iterdir():

    if pkg.is_dir() and (now - pkg.stat().st_mtime) < 86400:  # 86400 seconds in 24 hours

        recent_packages.append(pkg.name.split('-')[0])  # Extract package name without version



# Get specific versions for recent packages

output = subprocess.check_output(['pip', 'freeze']).decode()

with open('recent_requirements.txt', 'w') as req_file:

    for line in output.splitlines():

        if any(pkg in line for pkg in recent_packages):

            req_file.write(f"{line}\n")



print("recent_requirements.txt created with packages installed in the last 24 hours.")


