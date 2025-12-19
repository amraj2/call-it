"""Flask app for running Temporal workflows."""

import asyncio
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from temporal_client import start_test_workflow

app = Flask(__name__)
CORS(app)

# HTML template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Temporal Test Workflow</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            display: block;
        }
        .result.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            display: block;
        }
        .loading {
            text-align: center;
            color: #667eea;
            margin-top: 20px;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .workflow-id {
            font-size: 0.85em;
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Temporal Test Workflow</h1>
        <p class="subtitle">Run a test workflow to verify your Temporal setup</p>
        
        <form id="workflowForm">
            <div class="form-group">
                <label for="name">Your Name:</label>
                <input type="text" id="name" name="name" value="World" placeholder="Enter your name">
            </div>
            <button type="submit" id="submitBtn">Run Test Workflow</button>
        </form>
        
        <div class="loading" id="loading">⏳ Running workflow...</div>
        
        <div class="result" id="result"></div>
    </div>

    <script>
        document.getElementById('workflowForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            // Reset UI
            submitBtn.disabled = true;
            loading.classList.add('show');
            result.className = 'result';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/api/run-test', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: name || 'World' })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    result.className = 'result success';
                    result.innerHTML = `
                        <strong>✅ Success!</strong><br>
                        ${data.result}
                    `;
                } else {
                    result.className = 'result error';
                    result.innerHTML = `<strong>❌ Error:</strong><br>${data.error || 'Unknown error'}`;
                }
            } catch (error) {
                result.className = 'result error';
                result.innerHTML = `<strong>❌ Error:</strong><br>${error.message}`;
            } finally {
                submitBtn.disabled = false;
                loading.classList.remove('show');
                result.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """Render the main page."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/run-test", methods=["POST"])
def run_test():
    """API endpoint to run the test workflow."""
    try:
        data = request.get_json() or {}
        name = data.get("name", "World")
        
        # Run the async workflow
        result = asyncio.run(start_test_workflow(name))
        
        return jsonify({
            "success": True,
            "result": result,
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("FLASK_PORT", 5001))
    print(f"🌐 Flask app starting on http://localhost:{port}")
    print("📋 Make sure the Temporal worker is running: python temporal_worker.py")
    app.run(host="0.0.0.0", port=port, debug=True)

