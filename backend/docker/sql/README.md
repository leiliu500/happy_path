# Happy Path Docker Database Setup

This documentation covers the Docker-based PostgreSQL database setup for the Happy Path application, including development and production environments.

## Overview

The Happy Path project uses PostgreSQL as its primary database, containerized with Docker for consistent development and deployment environments. The setup includes:

- **Development Environment**: Optimized for local development with detailed logging and debugging features
- **Production Environment**: Optimized for performance and reliability
- **Automated Management**: Python script for easy database operations

## Directory Structure

```
backend/
├── docker/
│   └── sql/
│       ├── Dockerfile                  # Shared PostgreSQL Docker image
│       ├── docker-compose.dev.yml      # Development environment
│       ├── docker-compose.yml          # Production environment
│       └── README.md                   # This file
├── run_dev.py                          # Development environment manager
└── sql/                                # Database schemas and setup scripts
    ├── setup.sql
    └── schemas/
        └── *.sql
```

## Prerequisites

### Required Software

1. **Docker Desktop**: Download and install from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. **Python 3.7+**: For running the development manager script
3. **Git**: For cloning and managing the repository

### System Requirements

- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 2GB free space for Docker images and data
- **OS**: macOS, Windows, or Linux

## Quick Start

### 1. Start Development Database

```bash
# Navigate to the backend directory
cd backend

# Start the development database
python run_dev.py start
```

### 2. Check Status

```bash
python run_dev.py status
```

### 3. Connect to Database

```bash
python run_dev.py connect
```

## Development Environment

### Configuration

The development environment (`docker-compose.dev.yml`) includes:

- **Database**: `happy_path_dev`
- **Port**: `5433` (to avoid conflicts with local PostgreSQL)
- **User**: `happy_path_user`
- **Password**: `happy_path_dev_password`
- **Features**:
  - Detailed SQL logging
  - Volume persistence
  - Health checks
  - Auto-restart

### Database Connection Details

```
Host: localhost
Port: 5433
Database: happy_path_dev
Username: happy_path_user
Password: happy_path_dev_password
```

### Connection String

```
postgresql://happy_path_user:happy_path_dev_password@localhost:5433/happy_path_dev
```

## Production Environment

### Configuration

The production environment (`docker-compose.yml`) includes:

- **Database**: `happy_path`
- **Port**: `5432`
- **User**: `happy_path_user`
- **Password**: Set via `POSTGRES_PASSWORD` environment variable
- **Features**:
  - Performance-optimized settings
  - Backup volume mounting
  - Production-grade health checks

### Starting Production Environment

```bash
cd backend/docker/sql

# Set password via environment variable
export POSTGRES_PASSWORD=your_secure_password

# Start production database
docker compose up -d
```

## Development Manager Script (`run_dev.py`)

The `run_dev.py` script provides a comprehensive interface for managing the development database environment.

### Available Commands

#### Start Database
```bash
python run_dev.py start
```
- Checks Docker installation and daemon status
- Starts the PostgreSQL container
- Waits for database to be ready
- Confirms successful startup

#### Stop Database
```bash
python run_dev.py stop
```
- Gracefully stops the PostgreSQL container
- Preserves data volumes

#### Restart Database
```bash
python run_dev.py restart
```
- Stops and starts the database
- Useful for applying configuration changes

#### Check Status
```bash
python run_dev.py status
```
- Shows Docker installation status
- Displays container status
- Shows connection information

#### View Logs
```bash
# View recent logs
python run_dev.py logs

# Follow logs in real-time
python run_dev.py logs --follow
```

#### Connect to Database
```bash
python run_dev.py connect
```
- Opens interactive `psql` session
- Direct access to development database
- Use `\q` to exit

#### Reset Database
```bash
python run_dev.py reset
```
- **⚠️ DESTRUCTIVE OPERATION**
- Removes all data and volumes
- Requires confirmation
- Useful for clean slate development

### Script Features

- **Docker Validation**: Checks Docker installation and daemon status
- **Health Monitoring**: Waits for database readiness
- **Error Handling**: Provides clear error messages and troubleshooting hints
- **Safety Checks**: Confirmation required for destructive operations
- **Cross-Platform**: Works on macOS, Windows, and Linux

## Database Schema Management

### Automatic Initialization

The Docker setup automatically runs SQL scripts during container initialization:

1. **Primary Setup**: `sql/setup.sql`
2. **Schema Scripts**: All files in `sql/schemas/`

### Manual Schema Updates

For development, you can manually run SQL scripts:

```bash
# Connect to database
python run_dev.py connect

# Run SQL commands
\i /docker-entrypoint-initdb.d/sql_scripts/schemas/your_schema.sql
```

### Schema Reload

To reload all schemas from scratch:

```bash
# Reset database (destroys data)
python run_dev.py reset

# Start fresh database with all schemas
python run_dev.py start
```

## Troubleshooting

### Common Issues

#### Docker Not Running
```
✗ Docker daemon is not running. Please start Docker Desktop.
```
**Solution**: Start Docker Desktop application

#### Port Conflicts
```
Error: Port 5433 is already in use
```
**Solutions**:
1. Stop conflicting service: `lsof -ti:5433 | xargs kill`
2. Change port in `docker-compose.dev.yml`

#### Permission Issues
```
Error: Permission denied
```
**Solutions**:
1. Check Docker Desktop permissions
2. Run with appropriate user permissions
3. Verify file permissions in `docker/sql/` directory

#### Container Won't Start
```
✗ Database failed to become ready within timeout
```
**Solutions**:
1. Check logs: `python run_dev.py logs`
2. Verify Docker resources (memory/CPU)
3. Check SQL script syntax in initialization files

#### Connection Refused
```
psql: connection to server at "localhost" (127.0.0.1), port 5433 failed
```
**Solutions**:
1. Verify container is running: `python run_dev.py status`
2. Check port mapping in docker-compose file
3. Ensure firewall allows port 5433

### Advanced Troubleshooting

#### Direct Docker Commands

```bash
# Check container status
docker ps -a | grep happy_path

# View container logs
docker logs happy_path_postgres_dev

# Execute commands in container
docker exec -it happy_path_postgres_dev bash

# Inspect container configuration
docker inspect happy_path_postgres_dev
```

#### Database Diagnostics

```bash
# Connect and run diagnostics
python run_dev.py connect

-- Check database size
SELECT pg_size_pretty(pg_database_size('happy_path_dev'));

-- List all tables
\dt

-- Check connections
SELECT * FROM pg_stat_activity;
```

## Performance Optimization

### Development Environment

The development environment prioritizes debugging over performance:

- Detailed SQL statement logging
- Generous connection limits
- Extended timeouts for debugging

### Production Environment

The production environment is optimized for performance:

- **Memory Settings**: 512MB shared buffers, 1GB effective cache
- **Connection Pooling**: 200 max connections
- **WAL Settings**: Optimized write-ahead logging
- **Statistics**: Enhanced query planning statistics

### Custom Optimization

To customize performance settings, modify the `command` section in docker-compose files:

```yaml
command: >
  postgres 
  -c max_connections=300
  -c shared_buffers=1GB
  -c effective_cache_size=2GB
```

## Backup and Recovery

### Development Backups

```bash
# Create backup
docker exec happy_path_postgres_dev pg_dump -U happy_path_user happy_path_dev > backup.sql

# Restore backup
python run_dev.py reset
python run_dev.py start
cat backup.sql | docker exec -i happy_path_postgres_dev psql -U happy_path_user -d happy_path_dev
```

### Production Backups

```bash
# Automated backup script
docker exec happy_path_postgres pg_dump -U happy_path_user happy_path > /var/lib/postgresql/backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

## Security Considerations

### Development Security

- Default passwords for convenience
- Trust authentication method
- Detailed logging (may contain sensitive data)

### Production Security

- Environment variable passwords
- Restricted network access
- Minimal logging
- Regular security updates

### Best Practices

1. **Passwords**: Use strong, unique passwords in production
2. **Networks**: Isolate database networks
3. **Updates**: Regularly update PostgreSQL image
4. **Monitoring**: Implement security monitoring
5. **Backups**: Encrypt backup files

## Integration with Application

### Python Connection

```python
import psycopg2

# Development connection
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="happy_path_dev",
    user="happy_path_user",
    password="happy_path_dev_password"
)
```

### Environment Variables

```bash
# Development
export DATABASE_URL="postgresql://happy_path_user:happy_path_dev_password@localhost:5433/happy_path_dev"

# Production
export DATABASE_URL="postgresql://happy_path_user:${POSTGRES_PASSWORD}@localhost:5432/happy_path"
```

## Monitoring and Logging

### Log Locations

- **Development**: Container logs via `docker logs` or `python run_dev.py logs`
- **Production**: Backup volume `/var/lib/postgresql/backups`

### Health Checks

Both environments include health checks that verify:
- PostgreSQL process is running
- Database accepts connections
- User authentication works

### Monitoring Commands

```bash
# Container resource usage
docker stats happy_path_postgres_dev

# Database activity
python run_dev.py connect
SELECT * FROM pg_stat_activity;
```

## Support and Resources

### Official Documentation

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Common PostgreSQL Commands

```sql
-- List databases
\l

-- List tables
\dt

-- Describe table
\d table_name

-- Show running queries
SELECT * FROM pg_stat_activity;

-- Database size
SELECT pg_size_pretty(pg_database_size(current_database()));
```

### Getting Help

1. Check logs: `python run_dev.py logs`
2. Verify status: `python run_dev.py status`
3. Review this documentation
4. Check PostgreSQL and Docker documentation
5. Contact the development team

---

**Note**: This setup is designed for development convenience and production reliability. Always follow your organization's security and deployment guidelines when using in production environments.
