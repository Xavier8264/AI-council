"""
Example usage of the AI Council cloud agent delegation system.
"""

from cloud_agent import CloudAgentDelegator, SimpleCloudAgent
from config import AgentConfig


def main():
    """Demonstrate cloud agent delegation."""
    
    # Create a delegator
    delegator = CloudAgentDelegator()
    
    # Create and configure agents
    agent_config = AgentConfig({
        "max_retries": 5,
        "timeout": 60
    })
    
    # Create simple agents
    agent1 = SimpleCloudAgent("agent-1", agent_config.to_dict())
    agent2 = SimpleCloudAgent("agent-2", agent_config.to_dict())
    
    # Register agents
    delegator.register_agent(agent1)
    delegator.register_agent(agent2)
    
    # List registered agents
    print("Registered agents:", delegator.list_agents())
    
    # Create a task
    task = {
        "type": "analysis",
        "data": {
            "content": "Sample data to analyze",
            "priority": "high"
        }
    }
    
    # Delegate task to agent-1
    print("\nDelegating task to agent-1...")
    result1 = delegator.delegate("agent-1", task)
    print(f"Result from agent-1: {result1}")
    
    # Delegate different task to agent-2
    task2 = {
        "type": "processing",
        "data": {
            "items": [1, 2, 3, 4, 5]
        }
    }
    
    print("\nDelegating task to agent-2...")
    result2 = delegator.delegate("agent-2", task2)
    print(f"Result from agent-2: {result2}")
    
    # Demonstrate error handling
    print("\nTrying to delegate to non-existent agent...")
    try:
        delegator.delegate("non-existent", task)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Unregister an agent
    print("\nUnregistering agent-1...")
    delegator.unregister_agent("agent-1")
    print("Remaining agents:", delegator.list_agents())


if __name__ == "__main__":
    main()
