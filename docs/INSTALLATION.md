# 🚀 Installation Guide

## Prerequisites

- Python 3.8+ 
- Node.js 18+ (for web interface)
- Git 2.30+

## Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/takawasi/sca-cognitive-architecture.git
cd sca-cognitive-architecture
```

### 2. Setup Python Environment
```bash
python -m venv sca-env
source sca-env/bin/activate  # On Windows: sca-env\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize Components
```bash
# Start MCP servers
python examples/basic-usage/start_sca_servers.py

# Launch web interface
cd website
python -m http.server 8000
```

### 4. Verify Installation
Open http://localhost:8000 in your browser.

## Advanced Installation

### Production Deployment

#### VPS Setup
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx postgresql

# Setup PostgreSQL
sudo -u postgres createdb sca_production
sudo -u postgres createuser sca_user --createdb
```

#### SSL Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

#### Service Configuration
```bash
# Copy systemd service
sudo cp scripts/sca-system.service /etc/systemd/system/
sudo systemctl enable sca-system
sudo systemctl start sca-system
```

### Docker Installation

```bash
# Build container
docker build -t sca-system .

# Run with docker-compose
docker-compose up -d
```

## Configuration

### Environment Variables
```bash
export SCA_ENV=production
export SCA_DATABASE_URL=postgresql://user:pass@localhost/sca_db
export SCA_SECRET_KEY=your-secret-key
```

### MCP Server Configuration
Edit `config/mcp_servers.json`:
```json
{
  "servers": {
    "context_mapper": {
      "command": "python",
      "args": ["servers/context_mapper_server.py"],
      "env": {}
    }
  }
}
```

## Troubleshooting

### Common Issues

**MCP servers not connecting**
```bash
# Check server status
python scripts/health_check.py

# View logs
tail -f logs/sca_system.log
```

**Permission errors**
```bash
# Fix file permissions
chmod +x scripts/*.sh
sudo chown -R $USER:$USER .
```

**Database connection issues**
```bash
# Test database connection
python scripts/test_db_connection.py

# Reset database
python scripts/reset_database.py
```

For additional support, see [FAQ](FAQ.md) or open an [issue](https://github.com/takawasi/sca-cognitive-architecture/issues).