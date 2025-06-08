# Commands for Odoo

<!-- Installation -->
sudo apt update
sudo apt upgrade -y
sudo apt install -y docker.io docker-compose

<!-- Docker -->
docker --version
docker-compose --version

sudo systemctl restart docker
sudo systemctl status docker

<!-- Start Odoo -->
docker-compose down
docker-compose up -d
<!-- Stop Odoo Docker -->
docker-compose down

<!-- Check if all containers are running -->
docker ps

<!-- Check logs -->
docker-compose logs -f db      # PostgreSQL logs
docker-compose logs -f manager_prod  # Odoo latest logs

<!-- Run Odoo into Docker bash -->
docker exec -it odoo-web-1 odoo -i base -r odoo -w odoo

# Stop and remove containers, networks, and volumes
docker-compose down --remove-orphans --volumes
# Remove any lingering Docker resources
docker system prune -a --volumes
# Remove the old network (if it exists)
docker network rm manager_prod-network

# Create a fresh network
docker network create manager_prod-network

<!-- Grant permissions to the PostgreSQL user -->
docker exec -it manager_prod psql -U odoo -d postgres -c "ALTER USER odoo WITH SUPERUSER;"
# Check if the odoo user has the correct privileges
docker exec -it manager_prod psql -U odoo -d postgres -c "\du odoo"
# Apply the changes
docker-compose restart manager_prod
# Check if the odoo17 Database Exists
docker exec -it manager_prod psql -U odoo -d postgres -c "\l"
# If databases already exist but have ownership issues, drop and recreate them
docker exec -it manager_prod psql -U odoo -d postgres -c "DROP DATABASE odoo16;"
docker exec -it manager_prod psql -U odoo -d postgres -c "CREATE DATABASE odoo16 OWNER odoo;"
docker exec -it manager_prod psql -U odoo -d postgres -c "DROP DATABASE manager_prod;"
docker exec -it manager_prod psql -U odoo -d postgres -c "CREATE DATABASE manager_prod OWNER odoo;"

# Connect to PostgreSQL
docker exec -it manager_prod psql -U odoo -d postgres
# Run these SQL commands inside PostgreSQL:
GRANT ALL PRIVILEGES ON DATABASE odoo16 TO odoo;
GRANT ALL PRIVILEGES ON DATABASE manager_prod TO odoo;
# Make the user the owner of the databases (critical for Odoo)
ALTER DATABASE odoo16 OWNER TO odoo;
ALTER DATABASE manager_prod OWNER TO odoo;
# Exit PostgreSQL
\q

# Delete Old Database Volumes
docker volume rm manager_prod-db-data odoo16-web-data manager_prod-web-data 
# First start ONLY the PostgreSQL container
docker-compose up -d db
# Wait 20 seconds for PostgreSQL to initialize
sleep 20
# Start Odoo containers (they'll auto-create databases)
docker-compose up -d odoo16 manager_prod

echo "odoo" > odoo_pg_pass

docker-compose logs nginx-proxy
docker-compose logs nginx-letsencrypt

# Run an Odoo command inside the manager_prod container (for example, to update a module)
docker-compose exec manager_prod odoo -d manager_prod -u copro_manager --stop-after-init
docker-compose exec manager_prod odoo -d manager_prod -i base --stop-after-init
docker-compose down manager_prod
docker-compose up -d manager_prod


python3 manage.py collectstatic
sudo systemctl daemon-reload
sudo systemctl restart manager_prod.service
sudo systemctl status manager_prod.service

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

python3 manage.py makemigrations
python3 manage.py migrate

sudo journalctl -u manager_prod.service -f
python3 manage.py runserver 0.0.0.0:8011

# CONNECT POSTGRES
sudo -i -u postgres
sudo nano /var/lib/pgsql/data/postgresql.conf

# systemd
sudo nano /etc/systemd/system/manager_prod.service

# nginx
sudo nano /etc/nginx/sites-available/manager_prod.conf

# CREATE SSL CERTIFICATE
sudo dnf install certbot python3-certbot-nginx
sudo certbot --nginx

# link the configuration to enable it
sudo ln -s /etc/nginx/sites-available/manager_prod /etc/nginx/sites-enabled/

sudo certbot certificates
sudo certbot --nginx -d property-manager.siisi.online -d www.property-manager.siisi.online

sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

sudo systemctl enable certbot.timer
sudo certbot renew --dry-run

# kill all port runing
sudo lsof -t -iTCP:8001 -sTCP:LISTEN | xargs sudo kill

# Find Your Computer's Local IP Address
ifconfig | grep inet


docker-compose down --volumes --remove-orphans
docker system prune -a --volumes 
docker-compose down
docker-compose up -d --build
docker-compose exec manager_prod odoo -d manager_prod -i base --stop-after-init
