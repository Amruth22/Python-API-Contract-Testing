"""
Mock Manager
Manages mock services and responses
"""

import logging
from mocks.mock_responses import get_mock_response

logger = logging.getLogger(__name__)


class MockManager:
    """
    Manages mock services
    """
    
    def __init__(self):
        self.mocks = {}
        self.active_mocks = set()
        logger.info("Mock Manager initialized")
    
    def register_mock(self, name, mock_server):
        """
        Register a mock server
        
        Args:
            name: Mock name
            mock_server: MockServer instance
        """
        self.mocks[name] = mock_server
        logger.info(f"Mock registered: {name}")
    
    def activate_mock(self, name):
        """
        Activate a mock
        
        Args:
            name: Mock name
        """
        if name in self.mocks:
            self.active_mocks.add(name)
            logger.info(f"Mock activated: {name}")
    
    def deactivate_mock(self, name):
        """
        Deactivate a mock
        
        Args:
            name: Mock name
        """
        if name in self.active_mocks:
            self.active_mocks.remove(name)
            logger.info(f"Mock deactivated: {name}")
    
    def is_active(self, name):
        """Check if mock is active"""
        return name in self.active_mocks
    
    def get_mock(self, name):
        """Get mock by name"""
        return self.mocks.get(name)
    
    def clear_all_history(self):
        """Clear request history for all mocks"""
        for mock in self.mocks.values():
            if hasattr(mock, 'clear_history'):
                mock.clear_history()
        logger.info("All mock history cleared")


class MockScenario:
    """
    Defines a testing scenario with mocks
    """
    
    def __init__(self, name):
        """
        Initialize mock scenario
        
        Args:
            name: Scenario name
        """
        self.name = name
        self.mocks = []
        logger.info(f"Mock scenario created: {name}")
    
    def add_mock(self, method, path, response, status=200):
        """
        Add mock to scenario
        
        Args:
            method: HTTP method
            path: Endpoint path
            response: Response data
            status: Status code
        """
        self.mocks.append({
            'method': method,
            'path': path,
            'response': response,
            'status': status
        })
    
    def apply_to_server(self, mock_server):
        """
        Apply scenario to mock server
        
        Args:
            mock_server: MockServer instance
        """
        for mock in self.mocks:
            mock_server.add_mock(
                mock['method'],
                mock['path'],
                mock['response'],
                mock['status']
            )
        
        logger.info(f"Scenario applied: {self.name} ({len(self.mocks)} mocks)")
