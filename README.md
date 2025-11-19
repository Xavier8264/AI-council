# AI-council

A Python framework for delegating tasks to cloud-based AI agents. The AI Council provides a flexible system for registering, managing, and delegating work to multiple cloud agents.

## Features

- **Agent Registration**: Register and manage multiple cloud agents
- **Task Delegation**: Delegate tasks to specific agents by name
- **Extensible Architecture**: Extend the `CloudAgent` base class to create custom agents
- **Configuration Management**: Flexible configuration system for agent settings
- **Task Validation**: Built-in validation for task structure

## Installation

```bash
# Clone the repository
git clone https://github.com/Xavier8264/AI-council.git
cd AI-council
```

## Quick Start

```python
from cloud_agent import CloudAgentDelegator, SimpleCloudAgent
from config import AgentConfig

# Create a delegator
delegator = CloudAgentDelegator()

# Create and register agents
agent = SimpleCloudAgent("my-agent")
delegator.register_agent(agent)

# Create a task
task = {
    "type": "analysis",
    "data": {
        "content": "Data to process"
    }
}

# Delegate the task
result = delegator.delegate("my-agent", task)
print(result)
```

## Usage

### Creating Custom Agents

Extend the `CloudAgent` base class to create custom agents:

```python
from cloud_agent import CloudAgent

class MyCustomAgent(CloudAgent):
    def execute(self, task):
        # Implement your custom logic here
        return {
            "status": "completed",
            "result": "Custom processing result"
        }
```

### Configuration

Use the `AgentConfig` class to manage agent configurations:

```python
from config import AgentConfig

config = AgentConfig({
    "max_retries": 5,
    "timeout": 60
})

agent = SimpleCloudAgent("my-agent", config.to_dict())
```

### Running the Example

```bash
python example.py
```

### Running Tests

```bash
python -m unittest test_cloud_agent.py
```

## Architecture

The system consists of three main components:

1. **CloudAgent**: Abstract base class for all agents
2. **CloudAgentDelegator**: Central registry and routing system for agents
3. **AgentConfig**: Configuration management for agents

## API Reference

### CloudAgent

- `__init__(name, config)`: Initialize an agent
- `execute(task)`: Execute a task (abstract method)
- `validate_task(task)`: Validate task structure

### CloudAgentDelegator

- `register_agent(agent)`: Register a new agent
- `unregister_agent(agent_name)`: Unregister an agent
- `delegate(agent_name, task)`: Delegate a task to an agent
- `list_agents()`: List all registered agents

### AgentConfig

- `get(key, default)`: Get a configuration value
- `set(key, value)`: Set a configuration value
- `to_json()`: Export configuration as JSON
- `from_json(json_str)`: Import configuration from JSON

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.