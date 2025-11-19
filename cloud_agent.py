"""
Cloud Agent Module

This module provides functionality for delegating tasks to cloud-based AI agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json


class CloudAgent(ABC):
    """
    Abstract base class for cloud agents.
    
    Cloud agents are AI systems that can process tasks and return results.
    Subclasses should implement the execute method to define agent-specific behavior.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a cloud agent.
        
        Args:
            name: The name/identifier for this agent
            config: Optional configuration dictionary for the agent
        """
        self.name = name
        self.config = config or {}
    
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task using this cloud agent.
        
        Args:
            task: Dictionary containing task information
            
        Returns:
            Dictionary containing the result of the task execution
        """
        pass
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """
        Validate that a task has the required structure.
        
        Args:
            task: Task dictionary to validate
            
        Returns:
            True if task is valid, False otherwise
        """
        return isinstance(task, dict) and 'type' in task


class CloudAgentDelegator:
    """
    Delegator class that routes tasks to appropriate cloud agents.
    """
    
    def __init__(self):
        """Initialize the delegator with an empty registry of agents."""
        self.agents: Dict[str, CloudAgent] = {}
    
    def register_agent(self, agent: CloudAgent) -> None:
        """
        Register a cloud agent with the delegator.
        
        Args:
            agent: CloudAgent instance to register
        """
        self.agents[agent.name] = agent
    
    def unregister_agent(self, agent_name: str) -> bool:
        """
        Unregister a cloud agent.
        
        Args:
            agent_name: Name of the agent to unregister
            
        Returns:
            True if agent was unregistered, False if not found
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False
    
    def delegate(self, agent_name: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delegate a task to a specific cloud agent.
        
        Args:
            agent_name: Name of the agent to delegate to
            task: Task information to execute
            
        Returns:
            Result dictionary from the agent
            
        Raises:
            ValueError: If agent is not found or task is invalid
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found in registry")
        
        agent = self.agents[agent_name]
        
        if not agent.validate_task(task):
            raise ValueError(f"Invalid task format for agent '{agent_name}'")
        
        return agent.execute(task)
    
    def list_agents(self) -> list:
        """
        Get a list of all registered agent names.
        
        Returns:
            List of agent names
        """
        return list(self.agents.keys())


class SimpleCloudAgent(CloudAgent):
    """
    A simple example implementation of a cloud agent.
    
    This agent processes tasks and returns results with basic metadata.
    """
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task using this simple cloud agent.
        
        Args:
            task: Dictionary containing task information
            
        Returns:
            Dictionary with task result and metadata
        """
        task_type = task.get('type', 'unknown')
        task_data = task.get('data', {})
        
        # Simple processing - echo back the task with status
        result = {
            'status': 'completed',
            'agent': self.name,
            'task_type': task_type,
            'result': f"Processed {task_type} task",
            'input_data': task_data
        }
        
        return result
