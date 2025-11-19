/**
 * AI Council - Frontend JavaScript
 */

// API base URL
const API_BASE = '';

// State
let availableModels = [];

/**
 * Initialize the application
 */
async function init() {
    await loadModels();
    setupEventListeners();
}

/**
 * Load available models from the API
 */
async function loadModels() {
    try {
        const response = await fetch(`${API_BASE}/api/models`);
        const data = await response.json();
        availableModels = data.models;
        renderModels();
    } catch (error) {
        console.error('Error loading models:', error);
        showError('Failed to load available models');
    }
}

/**
 * Render model checkboxes
 */
function renderModels() {
    const container = document.getElementById('models-container');
    container.innerHTML = '';

    availableModels.forEach(model => {
        const modelDiv = document.createElement('div');
        modelDiv.className = 'model-item';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `model-${model.name}`;
        checkbox.value = model.name;
        checkbox.disabled = !model.configured;
        
        const label = document.createElement('label');
        label.htmlFor = `model-${model.name}`;
        label.textContent = model.display_name;
        
        if (!model.configured) {
            label.classList.add('disabled');
            label.title = 'API key not configured';
        }
        
        modelDiv.appendChild(checkbox);
        modelDiv.appendChild(label);
        container.appendChild(modelDiv);
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    const startButton = document.getElementById('start-debate');
    startButton.addEventListener('click', startDebate);
}

/**
 * Start a debate
 */
async function startDebate() {
    const question = document.getElementById('question').value.trim();
    const rounds = parseInt(document.getElementById('rounds').value);
    
    // Validate input
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    // Get selected models
    const selectedModels = [];
    availableModels.forEach(model => {
        const checkbox = document.getElementById(`model-${model.name}`);
        if (checkbox && checkbox.checked) {
            selectedModels.push(model.name);
        }
    });
    
    if (selectedModels.length === 0) {
        showError('Please select at least one model');
        return;
    }
    
    // Show loading state
    const resultsSection = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const debateOutput = document.getElementById('debate-output');
    
    resultsSection.style.display = 'block';
    loading.style.display = 'block';
    debateOutput.innerHTML = '';
    
    // Disable the start button
    const startButton = document.getElementById('start-debate');
    startButton.disabled = true;
    startButton.textContent = 'Running Debate...';
    
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
            throw new Error(error.detail || 'Failed to run debate');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Error running debate:', error);
        showError(`Error: ${error.message}`);
    } finally {
        loading.style.display = 'none';
        startButton.disabled = false;
        startButton.textContent = 'Start Debate';
    }
}

/**
 * Display debate results
 */
function displayResults(result) {
    const debateOutput = document.getElementById('debate-output');
    debateOutput.innerHTML = '';
    
    // Display question
    const questionDiv = document.createElement('div');
    questionDiv.className = 'result-question';
    questionDiv.innerHTML = `<h3>Question:</h3><p>${escapeHtml(result.question)}</p>`;
    debateOutput.appendChild(questionDiv);
    
    // Display debate history
    const historyDiv = document.createElement('div');
    historyDiv.className = 'debate-history';
    historyDiv.innerHTML = '<h3>Debate History:</h3>';
    
    result.debate_history.forEach((round, index) => {
        const roundDiv = document.createElement('div');
        roundDiv.className = 'debate-round';
        
        const roundTitle = document.createElement('h4');
        roundTitle.textContent = `Round ${round.round} (${round.type})`;
        roundDiv.appendChild(roundTitle);
        
        round.responses.forEach(resp => {
            const responseDiv = document.createElement('div');
            responseDiv.className = 'model-response';
            
            const modelName = document.createElement('div');
            modelName.className = 'model-name';
            modelName.textContent = resp.model.toUpperCase();
            
            const responseText = document.createElement('div');
            responseText.className = 'response-text';
            responseText.textContent = resp.response;
            
            responseDiv.appendChild(modelName);
            responseDiv.appendChild(responseText);
            roundDiv.appendChild(responseDiv);
        });
        
        historyDiv.appendChild(roundDiv);
    });
    
    debateOutput.appendChild(historyDiv);
    
    // Display final answer
    const finalDiv = document.createElement('div');
    finalDiv.className = 'final-answer';
    finalDiv.innerHTML = `
        <h3>Final Synthesized Answer:</h3>
        <p>${escapeHtml(result.final_answer)}</p>
    `;
    debateOutput.appendChild(finalDiv);
}

/**
 * Show error message
 */
function showError(message) {
    const debateOutput = document.getElementById('debate-output');
    debateOutput.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${escapeHtml(message)}
        </div>
    `;
    
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

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
