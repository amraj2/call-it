// Main JavaScript for workflow form

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('workflowForm');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
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
                result.innerHTML = `
                    <strong>❌ Error:</strong><br>
                    ${data.error || 'Unknown error'}
                `;
            }
        } catch (error) {
            result.className = 'result error';
            result.innerHTML = `
                <strong>❌ Error:</strong><br>
                ${error.message}
            `;
        } finally {
            submitBtn.disabled = false;
            loading.classList.remove('show');
            result.style.display = 'block';
        }
    });
});

