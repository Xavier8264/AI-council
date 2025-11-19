"""
Unit tests for the cloud agent delegation system.
"""

import unittest
from cloud_agent import CloudAgent, CloudAgentDelegator, SimpleCloudAgent
from config import AgentConfig


class TestCloudAgent(unittest.TestCase):
    """Test cases for CloudAgent base class."""
    
    def test_agent_initialization(self):
        """Test that agents can be initialized with name and config."""
        agent = SimpleCloudAgent("test-agent", {"key": "value"})
        self.assertEqual(agent.name, "test-agent")
        self.assertEqual(agent.config["key"], "value")
    
    def test_agent_initialization_without_config(self):
        """Test that agents can be initialized without config."""
        agent = SimpleCloudAgent("test-agent")
        self.assertEqual(agent.name, "test-agent")
        self.assertEqual(agent.config, {})
    
    def test_task_validation(self):
        """Test task validation."""
        agent = SimpleCloudAgent("test-agent")
        
        # Valid task
        valid_task = {"type": "test", "data": {}}
        self.assertTrue(agent.validate_task(valid_task))
        
        # Invalid tasks
        self.assertFalse(agent.validate_task({}))
        self.assertFalse(agent.validate_task({"data": {}}))
        self.assertFalse(agent.validate_task("not a dict"))


class TestSimpleCloudAgent(unittest.TestCase):
    """Test cases for SimpleCloudAgent."""
    
    def test_execute_task(self):
        """Test task execution."""
        agent = SimpleCloudAgent("test-agent")
        task = {
            "type": "analysis",
            "data": {"content": "test"}
        }
        
        result = agent.execute(task)
        
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["agent"], "test-agent")
        self.assertEqual(result["task_type"], "analysis")
        self.assertEqual(result["input_data"], {"content": "test"})
    
    def test_execute_task_without_data(self):
        """Test task execution without data field."""
        agent = SimpleCloudAgent("test-agent")
        task = {"type": "simple"}
        
        result = agent.execute(task)
        
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["input_data"], {})


class TestCloudAgentDelegator(unittest.TestCase):
    """Test cases for CloudAgentDelegator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.delegator = CloudAgentDelegator()
        self.agent1 = SimpleCloudAgent("agent-1")
        self.agent2 = SimpleCloudAgent("agent-2")
    
    def test_register_agent(self):
        """Test registering an agent."""
        self.delegator.register_agent(self.agent1)
        self.assertIn("agent-1", self.delegator.agents)
    
    def test_unregister_agent(self):
        """Test unregistering an agent."""
        self.delegator.register_agent(self.agent1)
        result = self.delegator.unregister_agent("agent-1")
        
        self.assertTrue(result)
        self.assertNotIn("agent-1", self.delegator.agents)
    
    def test_unregister_nonexistent_agent(self):
        """Test unregistering a non-existent agent."""
        result = self.delegator.unregister_agent("nonexistent")
        self.assertFalse(result)
    
    def test_list_agents(self):
        """Test listing registered agents."""
        self.delegator.register_agent(self.agent1)
        self.delegator.register_agent(self.agent2)
        
        agents = self.delegator.list_agents()
        
        self.assertEqual(len(agents), 2)
        self.assertIn("agent-1", agents)
        self.assertIn("agent-2", agents)
    
    def test_delegate_task(self):
        """Test delegating a task to an agent."""
        self.delegator.register_agent(self.agent1)
        task = {"type": "test", "data": {}}
        
        result = self.delegator.delegate("agent-1", task)
        
        self.assertEqual(result["agent"], "agent-1")
        self.assertEqual(result["status"], "completed")
    
    def test_delegate_to_nonexistent_agent(self):
        """Test delegating to a non-existent agent raises error."""
        task = {"type": "test", "data": {}}
        
        with self.assertRaises(ValueError) as context:
            self.delegator.delegate("nonexistent", task)
        
        self.assertIn("not found", str(context.exception))
    
    def test_delegate_invalid_task(self):
        """Test delegating an invalid task raises error."""
        self.delegator.register_agent(self.agent1)
        invalid_task = {"data": {}}  # Missing 'type' field
        
        with self.assertRaises(ValueError) as context:
            self.delegator.delegate("agent-1", invalid_task)
        
        self.assertIn("Invalid task", str(context.exception))


class TestAgentConfig(unittest.TestCase):
    """Test cases for AgentConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AgentConfig()
        
        self.assertEqual(config.get("max_retries"), 3)
        self.assertEqual(config.get("timeout"), 30)
        self.assertTrue(config.get("enable_logging"))
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = AgentConfig({"max_retries": 5, "custom_key": "custom_value"})
        
        self.assertEqual(config.get("max_retries"), 5)
        self.assertEqual(config.get("custom_key"), "custom_value")
    
    def test_get_with_default(self):
        """Test getting config value with default."""
        config = AgentConfig()
        
        self.assertEqual(config.get("nonexistent", "default"), "default")
    
    def test_set_config(self):
        """Test setting configuration values."""
        config = AgentConfig()
        config.set("new_key", "new_value")
        
        self.assertEqual(config.get("new_key"), "new_value")
    
    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = AgentConfig({"key": "value"})
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["key"], "value")
    
    def test_json_serialization(self):
        """Test JSON serialization and deserialization."""
        config = AgentConfig({"key": "value", "number": 42})
        json_str = config.to_json()
        
        new_config = AgentConfig.from_json(json_str)
        
        self.assertEqual(new_config.get("key"), "value")
        self.assertEqual(new_config.get("number"), 42)


if __name__ == "__main__":
    unittest.main()
