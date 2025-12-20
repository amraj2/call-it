# Temporal Workflow Orchestration Platform

A scalable Temporal server setup with Flask frontend for running and managing workflows.

## Features

- 🚀 **Temporal Server** - Workflow orchestration engine
- 🔧 **Scalable Architecture** - Organized workflow and activity structure
- 🌐 **Flask Web Interface** - User-friendly web UI for running workflows
- 📊 **Temporal UI** - Built-in monitoring and workflow visualization
- 🐳 **Docker Compose** - Easy deployment with containerized services

## Quick Start

### Option 1: Start Everything at Once (Recommended)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start all services:**
   ```bash
   ./start_all.sh
   ```

   This will start:
   - Temporal server (Docker)
   - Temporal worker
   - Flask app

3. **Access the services:**
   - Flask App: http://localhost:8000
   - Temporal UI: http://localhost:8088

4. **Stop all services:**
   ```bash
   ./stop_all.sh
   ```

### Option 2: Start Services Manually

1. **Start the Temporal server:**
   ```bash
   docker-compose up -d
   ```
   Or use the helper script:
   ```bash
   ./start.sh
   ```

2. **Start the Temporal worker** (in a separate terminal):
   ```bash
   python3 temporal_worker.py
   ```
   Or use the helper script:
   ```bash
   ./run_worker.sh
   ```

3. **Start the Flask app** (in another terminal):
   ```bash
   python3 app.py
   ```
   Or use the helper script:
   ```bash
   ./run_flask.sh
   ```

## Services

- **PostgreSQL**: Database for Temporal (port 5432)
- **Temporal Server**: Workflow orchestration engine (port 7233)
- **Temporal UI**: Web interface for monitoring workflows (port 8088)
- **Flask App**: Web interface for running workflows (port 8000)

## Project Structure

```
call-it/
├── app/                      # Flask application
│   ├── __init__.py          # App factory
│   ├── config.py            # Flask configuration
│   ├── routes/               # Route blueprints
│   │   ├── main.py          # Main routes
│   │   └── api.py           # API endpoints
│   ├── static/               # Static files
│   │   ├── css/
│   │   └── js/
│   └── templates/           # HTML templates
├── temporal/                 # Temporal workflows & activities
│   ├── workflows/            # Workflow definitions
│   │   └── test.py          # Test workflow
│   ├── activities/           # Activity implementations
│   │   └── test.py          # Test activities
│   ├── shared/               # Shared utilities
│   ├── config.py            # Temporal configuration
│   └── registry.py          # Auto-discovery system
├── app.py                    # Flask entry point
├── temporal_worker.py        # Temporal worker
├── temporal_client.py        # Temporal client
├── docker-compose.yml        # Docker services
└── requirements.txt          # Python dependencies
```

## Running Workflows

### Via Flask App (Recommended)

1. Make sure all services are running: `./start_all.sh`
2. Open http://localhost:8000 in your browser
3. Enter a name and click "Run Test Workflow"

### Via Command Line

```bash
python3 temporal_client.py
```

## Adding New Workflows

See `WORKFLOW_GUIDE.md` for a complete step-by-step guide on creating new workflows, adding them to the Flask app, and creating dedicated pages.

Quick reference:
- `temporal/README.md` - Temporal structure and organization
- `WORKFLOW_GUIDE.md` - Complete workflow creation guide

## Configuration

### Environment Variables

- `FLASK_PORT` - Flask app port (default: 8000)
- `FLASK_ENV` - Flask environment (development/production/testing)
- `TEMPORAL_ADDRESS` - Temporal server address (default: localhost:7233)
- `TEMPORAL_NAMESPACE` - Temporal namespace (default: default)
- `TEMPORAL_TASK_QUEUE` - Default task queue (default: test-task-queue)

## Troubleshooting

### Flask App Not Loading

1. Check if Flask is running: `ps aux | grep app.py`
2. Check logs: `tail -f flask.log` (if running via start_all.sh)
3. Verify port 8000 is not in use: `lsof -i :8000`

### Temporal Worker Not Starting

1. Check if Temporal server is running: `docker-compose ps`
2. Verify server is accessible: `nc -z localhost 7233`
3. Check worker logs: `tail -f worker.log` (if running via start_all.sh)

### Temporal UI Not Accessible

1. **Wait a bit longer** - The UI may take 10-20 seconds to fully start
2. **Check container status:**
   ```bash
   docker-compose ps
   ```
3. **Check UI logs:**
   ```bash
   docker logs temporal-ui
   ```
   You should see: `⇨ http server started on [::]:8080`
4. **Restart the UI:**
   ```bash
   docker-compose restart temporal-ui
   ```

### Temporal Server Connection Issues

1. **Check if Temporal is ready:**
   ```bash
   docker logs temporal | tail -20
   ```
2. **Wait for initialization** - Temporal may take 30-60 seconds to fully start
3. **Restart if needed:**
   ```bash
   docker-compose restart temporal
   ```

## Development

### Project Organization

- **Flask App**: Uses app factory pattern with blueprints for scalability
- **Temporal Workflows**: Organized by domain in `temporal/workflows/`
- **Temporal Activities**: Organized by domain in `temporal/activities/`
- **Auto-discovery**: Workflows and activities are automatically registered

### Creating New Workflows

**📖 See `WORKFLOW_GUIDE.md` for complete step-by-step instructions.**

Quick overview:
1. Create activity in `temporal/activities/`
2. Create workflow in `temporal/workflows/`
3. Register both in their respective `__init__.py` files
4. Add Flask route in `app/routes/main.py`
5. Create HTML template in `app/templates/workflows/`

**Template file:** `docs/workflow_template.py` contains copy-paste templates.

### Adding New Features

1. **New Workflow**: Follow `WORKFLOW_GUIDE.md` for complete instructions
2. **New Activity**: Add to `temporal/activities/` and register in `__init__.py`
3. **New API Endpoint**: Add route to `app/routes/api.py`
4. **New Page**: Add route to `app/routes/main.py` and template to `app/templates/`

## License

MIT
