"""
AI Council - Cloud Agent Delegation System

A Python framework for delegating tasks to cloud-based AI agents.
"""

from .cloud_agent import CloudAgent, CloudAgentDelegator, SimpleCloudAgent
from .config import AgentConfig

__version__ = "0.1.0"
__all__ = [
    "CloudAgent",
    "CloudAgentDelegator", 
    "SimpleCloudAgent",
    "AgentConfig"
]
