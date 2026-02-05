help:
	@echo "Available commands:"
	@echo "  make build        - Build Docker images"
	@echo "  make build-no-cache        - Build Docker images without cache"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make restart      - Restart all services"
	@echo "  make logs         - Show logs (all services)"
	@echo "  make logs-webapp  - Show webapp logs only"
	@echo "  make logs-db      - Show MongoDB logs only"
	@echo "  make logs-follow  - Follow logs in real-time"
	@echo "  make db-backup    - Backup MongoDB data"
	@echo "  make db-restore   - Restore MongoDB data"
	@echo "  make init-admin    - Initialize admin user"
	@echo "  make init-mock    - Initialize mock data"
	"

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose build

# Build without cache
build-no-cache:
	@echo "Building Docker images (no cache)..."
	docker-compose build --no-cache

# Start services
up:
	@echo "Starting services..."
	docker-compose up -d
	@echo "Services started!"
	@echo "   Web:     http://localhost:8080"
	@echo "   MongoDB: localhost:27017"

# Stop services
down:
	@echo "⏹️  Stopping services..."
	docker-compose down

# Restart services
restart: down up

# Restart specific service
restart-webapp:
	@echo "Restarting webapp..."
	docker-compose restart webapp

restart-db:
	@echo "Restarting MongoDB..."
	docker-compose restart mongodb

# Show logs
logs:
	docker-compose logs --tail=100

# Follow logs
logs-follow:
	docker-compose logs -f

# Show webapp logs only
logs-webapp:
	docker-compose logs --tail=100 webapp

# Show MongoDB logs only
logs-db:
	docker-compose logs --tail=100 mongodb

# Follow webapp logs
logs-webapp-follow:
	docker-compose logs -f webapp

# Detailed status
db-backup:
	@echo "Backing up MongoDB..."
	@mkdir -p backups
	docker exec iotdb_mongodb mongodump --db=iotdb --out=/tmp/backup
	docker cp iotdb_mongodb:/tmp/backup ./backups/backup-$(shell date +%Y%m%d-%H%M%S)
	@echo "Backup completed in ./backups/"

# Restore MongoDB (use: make db-restore BACKUP=backups/backup-20260205-120000)
db-restore:
	@if [ -z "$(BACKUP)" ]; then \
		echo "Error: Please specify BACKUP path"; \
		echo "Usage: make db-restore BACKUP=backups/backup-20260205-120000"; \
		exit 1; \
	fi
	@echo "Restoring MongoDB from $(BACKUP)..."
	docker cp $(BACKUP) iotdb_mongodb:/tmp/restore
	docker exec iotdb_mongodb mongorestore --db=iotdb /tmp/restore/iotdb
	@echo "Restore completed!"


# Initialize admin user
init-admin:
	@echo "Creating admin user..."
	docker exec -it iotdb_webapp python scripts/init-admin

#init mock data
init-mock:
	@echo "Initializing mock data..."
	docker exec -it iotdb_webapp python scripts/init-mock-data

# Rebuild and restart
rebuild: clean build up
	@echo "Rebuild completed!"

# Production deployment
deploy: clean build-no-cache up
	@echo "Deployed to production!"
%:
	@echo "❌ Unknown target: $@"
