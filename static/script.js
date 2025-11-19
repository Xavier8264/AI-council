/**
 * Frontend JavaScript for AI Council Debate application
 */

// API base URL
const API_BASE = '';

// DOM elements
let modelCheckboxes = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    await loadAvailableModels();
    setupEventListeners();
});

/**
 * Load available AI models from the API
 */
async function loadAvailableModels() {
    try {
        const response = await fetch(`${API_BASE}/api/models`);
        const data = await response.json();
        
        const modelContainer = document.getElementById('model-selection');
        modelContainer.innerHTML = '';
        
        data.models.forEach((model, index) => {
            const checkbox = document.createElement('div');
            checkbox.className = 'model-checkbox';
            checkbox.innerHTML = `
                <input type="checkbox" id="model-${index}" value="${model}" ${index < 2 ? 'checked' : ''}>
                <label for="model-${index}">${model}</label>
            `;
            modelContainer.appendChild(checkbox);
        });
    } catch (error) {
        console.error('Error loading models:', error);
        showError('Failed to load available models');
    }
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    const startButton = document.getElementById('start-debate');
    startButton.addEventListener('click', startDebate);
}

/**
 * Start the debate
 */
async function startDebate() {
    const question = document.getElementById('question').value.trim();
    const rounds = parseInt(document.getElementById('rounds').value);
    
    // Get selected models
    const selectedModels = Array.from(document.querySelectorAll('#model-selection input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    // Validation
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    if (selectedModels.length === 0) {
        showError('Please select at least one AI model');
        return;
    }
    
    // Show loading state
    const resultsSection = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const output = document.getElementById('debate-output');
    
    resultsSection.style.display = 'block';
    loading.style.display = 'block';
    output.innerHTML = '';
    
    // Disable start button
    const startButton = document.getElementById('start-debate');
    startButton.disabled = true;
    startButton.textContent = 'Debating...';
    
    try {
        const response = await fetch(`${API_BASE}/api/debate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                models: selectedModels,
                rounds: rounds
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Debate failed');
        }
        
        const result = await response.json();
        displayDebateResults(result);
    } catch (error) {
        console.error('Error during debate:', error);
        showError(`Debate failed: ${error.message}`);
    } finally {
        loading.style.display = 'none';
        startButton.disabled = false;
        startButton.textContent = 'Start Debate';
    }
}

/**
 * Display debate results
 */
function displayDebateResults(result) {
    const output = document.getElementById('debate-output');
    
    let html = `<div class="debate-results">`;
    
    // Display question
    html += `<div class="question-display">
        <h3>Question:</h3>
        <p>${escapeHtml(result.question)}</p>
    </div>`;
    
    // Display debate history
    html += `<div class="debate-history">`;
    result.debate_history.forEach((round) => {
        html += `<div class="round">
            <h3>Round ${round.round}</h3>
            <div class="round-responses">`;
        
        round.responses.forEach((resp) => {
            html += `<div class="model-response">
                <h4>${escapeHtml(resp.model)}</h4>
                <p>${escapeHtml(resp.response)}</p>
            </div>`;
        });
        
        html += `</div></div>`;
    });
    html += `</div>`;
    
    // Display final answer
    html += `<div class="final-answer">
        <h3>📝 Final Synthesized Answer</h3>
        <p>${escapeHtml(result.final_answer)}</p>
    </div>`;
    
    html += `</div>`;
    
    output.innerHTML = html;
}

/**
 * Show error message
 */
function showError(message) {
    const output = document.getElementById('debate-output');
    output.innerHTML = `<div class="error-message">⚠️ ${escapeHtml(message)}</div>`;
    
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
