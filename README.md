# 🏢 Siisi Odoo Deployment

A **containerized Odoo®** setup leveraging Docker and Docker Compose for rapid development, configuration management, and production-ready deployment. Includes PostgreSQL database, custom addons, secure secrets handling, and Odoo configuration templating.

![Platform Demo](static/assets/images/sydicate.jpg)

---

## 🚀 Project Highlights

* 📦 **Odoo Application** built from the official `odoo:latest` image
* 🐘 **PostgreSQL** database with health checks and persistent volumes
* 🔒 **Docker Secrets** for PostgreSQL password management
* 🔄 **Custom Addons** support via `/mnt/custom-addons`
* 🛠️ **Configuration** via `config/odoo.conf` and environment variables
* 📂 **Persistent Storage** for Odoo data and database
* 🌐 **Bridged Network** for inter-container communication

---

## 📁 Repository Structure

```plaintext
siisi/
├── .gitignore             # Exclude logs, venv, certs, config, and data
├── .gitattributes         # Binary path attributes for config and data
├── Dockerfile             # Custom Odoo Docker build (installs psycopg2, qifparse, pypdf)
├── docker-compose.yml     # Compose file defining db and siisi services
├── config/
│   └── odoo.conf          # Odoo server configuration file
├── custom-addons/         # Your custom Odoo addons here
├── odoo_pg_pass           # Docker secret file with DB password
└── logs/
    └── siisi/logs/        # Host path for Odoo logs
```

---

## ⚙️ Prerequisites

* **Docker** ≥ 20.10
* **Docker Compose** ≥ 1.29
* **Linux** or macOS host (permission handling tested on Linux)

---

## 🔧 Setup & Deployment

1. **Clone the Repository**

   ```bash
   git clone https://github.com/isaacaisha/siisi.git
   cd siisi/siisi
   ```

2. **Place Secret**

   * Create file `odoo_pg_pass` at project root containing only the PostgreSQL password.
   * Ensure file permissions restrict access: `chmod 600 odoo_pg_pass`

3. **Build & Start**

   ```bash
   docker-compose up -d --build
   ```

4. **Verify Containers**

   ```bash
   docker-compose ps
   ```

   * `siisi-db` status should be "healthy"
   * `siisi` (Odoo) should be "running" on port 8069

5. **Access Odoo**
   Open in browser: [http://localhost:8069](http://localhost:8069)

---

## 🔒 Secrets & Configuration

* **Database Secret**: via Docker secret `postgresql_password` (file: `odoo_pg_pass`)
* **Odoo Config**: `config/odoo.conf`:

  ```ini
  [options]
  addons_path = /mnt/custom-addons,/usr/lib/python3/site-packages/odoo/addons
  db_host = db
  db_port = 5432
  db_user = odoo
  db_password = <secret from Docker secret>
  admin_passwd = siisi321
  proxy_mode = True
  xmlrpc_port = 8069
  http_interface = 0.0.0.0
  data_dir = /var/lib/odoo
  logfile = /var/log/siisi/siisi/logs/odoo.log
  ```
* **Environment Variables** set in `docker-compose.yml`:

  * `POSTGRES_PASSWORD_FILE=/run/secrets/postgresql_password`
  * `ADDONS_PATH` override for custom addons

---

## 📂 Persistent Storage

| Volume          | Container Path                    | Purpose                      |
| --------------- | --------------------------------- | ---------------------------- |
| `siisi-db-data` | `/var/lib/postgresql/data/pgdata` | PostgreSQL database files    |
| `siisi-data`    | `/var/lib/odoo`                   | Odoo filestore (attachments) |
| `./logs`        | `/var/log/siisi/siisi/logs`       | Odoo log files on host       |

---

## 🌐 Networking

* **Network**: `siisi-network` (bridge) connects `db` and `siisi` services.
* **Ports**: Host port `8069` → Container port `8069` (Odoo web UI)

---

## 📝 .gitignore & .gitattributes

* Excludes Python caches, logs, venv, and config secrets.
* Marks binary directories to prevent Git diff noise.

---

## 🪶 Maintenance Tips

* **Database Backup**:

  ```bash
  docker exec siisi-db pg_dump -U odoo postgres > backup.sql
  ```
* **Restore**:

  ```bash
  cat backup.sql | docker exec -i siisi-db psql -U odoo -d postgres
  ```
* **Logs**:

  ```bash
  tail -f logs/siisi/logs/odoo.log
  ```

---

## 🤝 Contributing

1. Fork the repo
2. Add or update custom addons under `custom-addons/`
3. Submit a PR with clear description

---

## 📜 License

MIT License © 2025 Isaac Aïsha

---

*Happy Odoo-ing!*
