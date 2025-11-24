import os

# Create static directory
os.makedirs('static', exist_ok=True)

# Create index.html
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Council - Offline LLM Debate Platform</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI Council</h1>
            <p class="subtitle">Offline debate platform with unanimous consent - Powered by Ollama</p>
        </header>

        <div class="config-status" id="configStatus">
            <span>Checking Ollama status...</span>
        </div>

        <main>
            <section class="input-section">
                <h2>Ask Your Question</h2>
                <form id="debateForm">
                    <div class="form-group">
                        <label for="question">Question:</label>
                        <textarea 
                            id="question" 
                            name="question" 
                            rows="4" 
                            placeholder="Enter your question here... (e.g., 'What are the most effective strategies for combating climate change?')"
                            required
                        ></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="rounds">Maximum Debate Rounds:</label>
                        <input 
                            type="number" 
                            id="rounds" 
                            name="rounds" 
                            min="1" 
                            max="20" 
                            value="10"
                        >
                        <small>Debate continues until consensus or max rounds reached</small>
                    </div>

                    <button type="submit" id="submitBtn" class="btn-primary">
                        Start Debate
                    </button>
                </form>
            </section>

            <section class="results-section" id="resultsSection" style="display: none;">
                <h2>Debate Results</h2>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>The AI models are debating locally... Seeking unanimous consent.</p>
                    <p class="loading-detail">This may take a few minutes depending on your models.</p>
                </div>

                <div id="debateResults" style="display: none;">
                    <div class="consensus-banner" id="consensusBanner">
                        <!-- Consensus status will be inserted here -->
                    </div>

                    <div class="question-display">
                        <h3>Question:</h3>
                        <p id="displayQuestion"></p>
                    </div>

                    <div class="debate-history" id="debateHistory"></div>

                    <div class="final-answer">
                        <h3>📊 Final Synthesized Answer</h3>
                        <div id="finalAnswer" class="answer-content"></div>
                    </div>
                </div>

                <div id="errorDisplay" style="display: none;" class="error">
                    <h3>⚠️ Error</h3>
                    <p id="errorMessage"></p>
                </div>
            </section>
        </main>

        <footer>
            <p>Powered by Ollama - 100% offline and private | Built with FastAPI & Python</p>
        </footer>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>''')

# Create script.js
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write('''// Check Ollama and model status on load
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        const configStatus = document.getElementById('configStatus');
        
        if (!data.ollama_running) {
            configStatus.innerHTML = `
                <span class="status-error">⚠️ Ollama is not running. Please start with: ollama serve</span>
            `;
            configStatus.className = 'config-status error';
            return;
        }
        
        const readyCount = data.ready_models;
        const totalCount = data.total_configured;
        
        if (readyCount === 0) {
            configStatus.innerHTML = `
                <span class="status-error">⚠️ No models available. Please pull models: ollama pull llama3.1</span>
            `;
            configStatus.className = 'config-status error';
        } else if (readyCount < totalCount) {
            const modelList = Object.entries(data.configured_models)
                .filter(([k, v]) => v)
                .map(([k, v]) => k)
                .join(', ');
            
            configStatus.innerHTML = `
                <span class="status-warning">⚠ ${readyCount}/${totalCount} models ready: ${modelList}</span>
            `;
            configStatus.className = 'config-status warning';
        } else {
            const modelList = Object.keys(data.configured_models).join(', ');
            
            configStatus.innerHTML = `
                <span class="status-success">✓ All ${readyCount} models ready: ${modelList}</span>
            `;
            configStatus.className = 'config-status success';
        }
    } catch (error) {
        const configStatus = document.getElementById('configStatus');
        configStatus.innerHTML = `
            <span class="status-error">⚠️ Cannot connect to server</span>
        `;
        configStatus.className = 'config-status error';
    }
}

// Handle form submission
document.getElementById('debateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = document.getElementById('question').value.trim();
    const max_rounds = parseInt(document.getElementById('rounds').value);
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    // Show results section and loading state
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('debateResults').style.display = 'none';
    document.getElementById('errorDisplay').style.display = 'none';
    
    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Seeking Consensus...';
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    
    try {
        const response = await fetch('/api/debate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question, max_rounds })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to run debate');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        displayError(error.message);
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Start Debate';
        document.getElementById('loading').style.display = 'none';
    }
});

function displayResults(data) {
    // Display consensus banner
    const consensusBanner = document.getElementById('consensusBanner');
    if (data.consensus_reached) {
        consensusBanner.innerHTML = `
            <div class="consensus-success">
                <h3>✓ Unanimous Consensus Reached!</h3>
                <p>All models agreed after ${data.consensus_round} round(s)</p>
            </div>
        `;
    } else {
        consensusBanner.innerHTML = `
            <div class="consensus-partial">
                <h3>⚠ Partial Agreement</h3>
                <p>Models reached maximum rounds (${data.total_rounds}) without full consensus</p>
            </div>
        `;
    }
    
    // Display question
    document.getElementById('displayQuestion').textContent = data.question;
    
    // Display debate history
    const historyContainer = document.getElementById('debateHistory');
    historyContainer.innerHTML = '';
    
    data.debate_history.forEach((round, index) => {
        const roundDiv = document.createElement('div');
        roundDiv.className = 'debate-round';
        
        // Add consensus indicator if this was the consensus round
        const consensusIndicator = (data.consensus_reached && round.round === data.consensus_round) 
            ? ' <span class="consensus-indicator">✓ Consensus Reached</span>' 
            : '';
        
        const roundTitle = document.createElement('h3');
        roundTitle.innerHTML = `Round ${round.round}: ${round.description}${consensusIndicator}`;
        roundDiv.appendChild(roundTitle);
        
        round.responses.forEach(resp => {
            const responseDiv = document.createElement('div');
            responseDiv.className = 'model-response';
            
            const modelName = document.createElement('h4');
            modelName.textContent = resp.model;
            modelName.className = 'model-name';
            responseDiv.appendChild(modelName);
            
            const responseText = document.createElement('div');
            responseText.className = 'response-text';
            responseText.textContent = resp.response;
            responseDiv.appendChild(responseText);
            
            roundDiv.appendChild(responseDiv);
        });
        
        historyContainer.appendChild(roundDiv);
    });
    
    // Display final answer
    document.getElementById('finalAnswer').textContent = data.final_answer;
    
    // Show results
    document.getElementById('debateResults').style.display = 'block';
}

function displayError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorDisplay').style.display = 'block';
}

// Check health on page load
checkHealth();
''')

# Create style.css
with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(''':root {
    --primary-color: #2563eb;
    --primary-dark: #1e40af;
    --success-color: #059669;
    --error-color: #dc2626;
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --text-color: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 30px;
    box-shadow: var(--shadow-lg);
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

header .subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

.config-status {
    text-align: center;
    padding: 12px 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-weight: 500;
}

.config-status.success {
    background-color: #d1fae5;
    color: var(--success-color);
}

.config-status.error {
    background-color: #fee2e2;
    color: var(--error-color);
}

.config-status.warning {
    background-color: #fef3c7;
    color: #d97706;
}

.input-section, .results-section {
    background: var(--card-bg);
    padding: 30px;
    border-radius: 12px;
    box-shadow: var(--shadow);
    margin-bottom: 30px;
}

.input-section h2, .results-section h2 {
    margin-bottom: 20px;
    color: var(--primary-color);
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: var(--text-color);
}

.form-group textarea,
.form-group input {
    width: 100%;
    padding: 12px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s;
}

.form-group textarea:focus,
.form-group input:focus {
    outline: none;
    border-color: var(--primary-color);
}

.form-group small {
    display: block;
    margin-top: 5px;
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    padding: 14px 32px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.1s;
    box-shadow: var(--shadow);
}

.btn-primary:hover:not(:disabled) {
    background-color: var(--primary-dark);
    transform: translateY(-1px);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.loading {
    text-align: center;
    padding: 40px;
}

.loading-detail {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: 10px;
}

.spinner {
    border: 4px solid var(--border-color);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.consensus-banner {
    margin-bottom: 30px;
}

.consensus-success {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    padding: 20px;
    border-radius: 8px;
    border: 2px solid var(--success-color);
    text-align: center;
}

.consensus-success h3 {
    color: var(--success-color);
    margin-bottom: 10px;
}

.consensus-partial {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    padding: 20px;
    border-radius: 8px;
    border: 2px solid #d97706;
    text-align: center;
}

.consensus-partial h3 {
    color: #d97706;
    margin-bottom: 10px;
}

.consensus-indicator {
    color: var(--success-color);
    font-weight: 600;
    margin-left: 10px;
    font-size: 0.9em;
}

.question-display {
    background-color: var(--bg-color);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    border-left: 4px solid var(--primary-color);
}

.question-display h3 {
    margin-bottom: 10px;
    color: var(--primary-color);
}

.debate-round {
    margin-bottom: 40px;
    padding-bottom: 30px;
    border-bottom: 2px solid var(--border-color);
}

.debate-round:last-child {
    border-bottom: none;
}

.debate-round h3 {
    color: var(--primary-color);
    margin-bottom: 20px;
    font-size: 1.4rem;
}

.model-response {
    background-color: var(--bg-color);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 4px solid var(--text-secondary);
}

.model-name {
    color: var(--primary-color);
    font-size: 1.1rem;
    margin-bottom: 10px;
}

.response-text {
    color: var(--text-color);
    white-space: pre-wrap;
    line-height: 1.7;
}

.final-answer {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    padding: 30px;
    border-radius: 12px;
    margin-top: 40px;
    border: 2px solid var(--primary-color);
}

.final-answer h3 {
    color: var(--primary-color);
    font-size: 1.5rem;
    margin-bottom: 20px;
}

.answer-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    white-space: pre-wrap;
    line-height: 1.8;
    font-size: 1.05rem;
}

.error {
    background-color: #fee2e2;
    color: var(--error-color);
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid var(--error-color);
}

.error h3 {
    margin-bottom: 10px;
}

footer {
    text-align: center;
    padding: 30px 20px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }
    
    .container {
        padding: 10px;
    }
    
    .input-section, .results-section {
        padding: 20px;
    }
}
''')

print("Static files created successfully!")
