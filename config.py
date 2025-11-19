"""
Configuration module for AI Council cloud agents.
"""

import json
from typing import Any, Dict


class AgentConfig:
    """Configuration manager for cloud agents."""
    
    DEFAULT_CONFIG = {
        "max_retries": 3,
        "timeout": 30,
        "enable_logging": True
    }
    
    def __init__(self, config_dict: Dict[str, Any] = None):
        """
        Initialize agent configuration.
        
        Args:
            config_dict: Optional dictionary with configuration values
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config_dict:
            self.config.update(config_dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AgentConfig':
        """
        Create configuration from JSON string.
        
        Args:
            json_str: JSON string containing configuration
            
        Returns:
            AgentConfig instance
        """
        config_dict = json.loads(json_str)
        return cls(config_dict)
    
    def to_json(self) -> str:
        """
        Convert configuration to JSON string.
        
        Returns:
            JSON string representation of configuration
        """
        return json.dumps(self.config, indent=2)
