# Simple Temporal Server

A minimal Temporal server setup with a test workflow and Flask app.

## Quick Start

1. **Start the Temporal server:**
   ```bash
   docker-compose up -d
   ```
   Or use the helper script:
   ```bash
   ./start.sh
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Temporal worker** (in a separate terminal):
   ```bash
   python temporal_worker.py
   ```
   Or use the helper script:
   ```bash
   ./run_worker.sh
   ```

4. **Start the Flask app** (in another terminal):
   ```bash
   python app.py
   ```
   Or use the helper script:
   ```bash
   ./run_flask.sh
   ```

5. **Access the Flask app:**
   Open http://localhost:5001 in your browser

6. **Access the Temporal UI:**
   Open http://localhost:8088 in your browser to monitor workflows

## Services

- **PostgreSQL**: Database for Temporal (port 5432)
- **Temporal Server**: Workflow orchestration engine (port 7233)
- **Temporal UI**: Web interface for monitoring workflows (port 8088)
- **Flask App**: Web interface for running workflows (port 5001)

## Services

- **PostgreSQL**: Database for Temporal (port 5432)
- **Temporal Server**: Workflow orchestration engine (port 7233)
- **Temporal UI**: Web interface for monitoring workflows (port 8088)

## Stop Services

```bash
docker-compose down
```

## Check Status

```bash
docker-compose ps
```

## View Logs

```bash
docker logs temporal
docker logs temporal-ui
```

## Troubleshooting

**If you can't access the UI at http://localhost:8088:**

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
5. **Verify port mapping:**
   The UI runs on port 8080 inside the container, mapped to 8088 on your host

**If you can't connect to the Temporal server (port 7233):**

1. **Check if Temporal is ready:**
   ```bash
   docker logs temporal | tail -20
   ```
2. **Wait for initialization** - Temporal may take 30-60 seconds to fully start
3. **Restart if needed:**
   ```bash
   docker-compose restart temporal
   ```

## Running the Test Workflow

### Via Flask App (Recommended)

1. Make sure the Temporal server is running: `docker-compose up -d`
2. Start the worker: `python temporal_worker.py` (in one terminal)
3. Start the Flask app: `python app.py` (in another terminal)
4. Open http://localhost:5001 in your browser
5. Enter a name and click "Run Test Workflow"

### Via Command Line

```bash
python temporal_client.py
```

## Project Structure

- `test_workflow.py` - Test workflow definition
- `test_activities.py` - Test activity implementation
- `temporal_worker.py` - Worker that executes workflows
- `temporal_client.py` - Client for starting workflows
- `app.py` - Flask web application
- `docker-compose.yml` - Docker services configuration
- `requirements.txt` - Python dependencies
