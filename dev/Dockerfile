# /home/siisi/property-management/dev/Dockerfile

# Use the official Odoo image as the base
FROM odoo:latest

# Switch to root to bypass permission issues
USER root

# bring in distro package
RUN apt-get update && apt-get install -y python3-packaging

# then pip-install your other deps
RUN pip3 install psycopg2 qifparse "pypdf>=3.1.0" --break-system-packages

# Switch back to Odoo user for security
USER odoo
