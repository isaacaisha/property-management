# Docker Compose commands eg.:

#  Check the Odoo Version
docker-compose exec manager_local odoo --version

# Start only the manager_local service
docker-compose up -d manager_local

# Stop only the manager_local service
docker-compose stop manager_local

# Restart only the manager_local service
docker-compose restart manager_local

# View logs for the manager_local service (follow mode)
docker-compose logs -f manager_local

# Alternatively, view logs for a container by its Docker name
docker logs gestion-web-local

# If databases already exist but have ownership issues, drop and recreate them
docker exec -it odoo-db-local psql -U odoo -d postgres -c "DROP DATABASE manager_local;"
docker exec -it odoo-db-local psql -U odoo -d postgres -c "CREATE DATABASE manager_local OWNER odoo;"

# Connect to PostgreSQL
docker exec -it odoo-db-local psql -U odoo -d postgres

# Run an interactive shell in the manager_local container
docker-compose exec manager_local /bin/bash

# Run an Odoo command inside the manager_local container (for example, to update a module)
docker-compose exec manager_local odoo -d manager_local -u copro_manager --stop-after-init
# To update every installed module in your database
docker-compose exec manager_local odoo -d manager_local -i base --stop-after-init
docker-compose exec manager_local odoo -d manager_local -u all --stop-after-init
docker-compose exec odoo16_local odoo -d odoo16_local -i base --stop-after-init
docker-compose exec odoo16_local odoo -d odoo16_local -u all --stop-after-init

# Remove a specific Docker volume (if not in use)
docker volume rm gestion-web-data-local

# List Docker networks
docker network ls

# Stop & Remove the Stuck Container
docker stop odoo-db-local
docker rm odoo-db-local
# Remove the Volume & Network
docker volume rm dev_odoo-db-data-local
docker network rm dev_odoo-network-local

docker network create dev_odoo-network-local
docker-compose up -d --build manager_local
docker-compose up -d --force-recreate manager_local

# Connect to the database
docker-compose exec db psql -U odoo -d manager_local

# Create Module using scaffold method
docker-compose exec manager_local odoo scaffold copro_manager /mnt/custom-addons/

# Create all Odoo Modules for 'manager_local' Database
docker-compose down && docker-compose up -d manager_local
docker-compose run --rm manager_local -d manager_local -i base --stop-after-init

# Stop and remove existing containers, networks, and volumes
docker-compose down --volumes --remove-orphans
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
# Remove All Images
docker rmi -f $(docker images -aq)
# Remove Docker System Data (Optional)
docker system prune -a --volumes -f

# Optionally prune unused volumes and networks
docker volume prune -f
docker network prune -f
docker system prune -a --volumes

# Start containers in detached mode
docker-compose up -d

# (In a separate terminal) Update Odoo modules in the container
docker-compose exec manager_local odoo -c /etc/odoo/odoo.conf -u all --stop-after-init
