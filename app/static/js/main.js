// Main JavaScript for workflow forms

document.addEventListener('DOMContentLoaded', function() {
    // Handle all workflow forms
    const workflowForms = document.querySelectorAll('.workflow-form');
    
    workflowForms.forEach(function(form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const workflowId = form.dataset.workflowId;
            const submitBtn = form.querySelector('.run-workflow-btn');
            const resultDiv = document.getElementById(`result-${workflowId}`);
            const loading = document.getElementById('loading');
            
            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.textContent = 'Running...';
            if (loading) loading.style.display = 'block';
            
            // Clear previous result
            if (resultDiv) {
                resultDiv.className = 'workflow-result';
                resultDiv.style.display = 'none';
                resultDiv.innerHTML = '';
            }
            
            // Collect form data
            const formData = new FormData(form);
            const params = {};
            for (const [key, value] of formData.entries()) {
                if (value.trim() !== '') {
                    params[key] = value.trim();
                }
            }
            
            try {
                const response = await fetch(`/api/workflows/${workflowId}/run`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(params)
                });
                
                const data = await response.json();
                
                if (resultDiv) {
                    if (response.ok) {
                        resultDiv.className = 'workflow-result success';
                        resultDiv.innerHTML = `
                            <strong>✅ Success!</strong><br>
                            <div style="margin-top: 8px;">${escapeHtml(String(data.result))}</div>
                            ${data.workflow_id ? `<small style="display: block; margin-top: 8px; opacity: 0.7;">Workflow ID: ${data.workflow_id}</small>` : ''}
                        `;
                    } else {
                        resultDiv.className = 'workflow-result error';
                        resultDiv.innerHTML = `
                            <strong>❌ Error:</strong><br>
                            <div style="margin-top: 8px;">${escapeHtml(data.error || 'Unknown error')}</div>
                        `;
                    }
                    resultDiv.style.display = 'block';
                }
            } catch (error) {
                if (resultDiv) {
                    resultDiv.className = 'workflow-result error';
                    resultDiv.innerHTML = `
                        <strong>❌ Error:</strong><br>
                        <div style="margin-top: 8px;">${escapeHtml(error.message)}</div>
                    `;
                    resultDiv.style.display = 'block';
                }
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = `Run ${form.closest('.workflow-card').querySelector('.workflow-name').textContent}`;
                if (loading) loading.style.display = 'none';
            }
        });
    });
});

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
