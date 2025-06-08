# /home/siisi/super/siisi/scratch/Dockerfile

# Use the official Odoo image as the base
FROM odoo:latest

# Switch to root to bypass permission issues
USER root

# Install psycopg2 and other dependencies without upgrading pip
RUN pip3 install psycopg2 qifparse "pypdf>=3.1.0" --break-system-packages

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Switch back to Odoo user for security
USER odoo
