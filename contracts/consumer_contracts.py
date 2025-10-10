"""
Consumer-Driven Contracts
Contracts defined by API consumers
"""

import logging

logger = logging.getLogger(__name__)


class ConsumerContract:
    """
    Consumer-driven contract
    Defines what a consumer expects from a provider
    """
    
    def __init__(self, consumer_name, provider_name):
        """
        Initialize consumer contract
        
        Args:
            consumer_name: Name of consumer (e.g., 'MobileApp')
            provider_name: Name of provider (e.g., 'UserAPI')
        """
        self.consumer_name = consumer_name
        self.provider_name = provider_name
        self.interactions = []
        
        logger.info(f"Consumer contract created: {consumer_name} -> {provider_name}")
    
    def add_interaction(self, description, request, response):
        """
        Add an interaction to the contract
        
        Args:
            description: Interaction description
            request: Expected request format
            response: Expected response format
        """
        interaction = {
            'description': description,
            'request': request,
            'response': response
        }
        
        self.interactions.append(interaction)
        logger.info(f"Interaction added: {description}")
    
    def to_dict(self):
        """Convert contract to dictionary"""
        return {
            'consumer': self.consumer_name,
            'provider': self.provider_name,
            'interactions': self.interactions
        }


class ConsumerContractRegistry:
    """
    Registry for consumer-driven contracts
    """
    
    def __init__(self):
        self.contracts = []
        logger.info("Consumer Contract Registry initialized")
    
    def register(self, contract):
        """
        Register a consumer contract
        
        Args:
            contract: ConsumerContract instance
        """
        self.contracts.append(contract)
        logger.info(f"Consumer contract registered: {contract.consumer_name} -> {contract.provider_name}")
    
    def get_contracts_for_provider(self, provider_name):
        """
        Get all contracts for a provider
        
        Args:
            provider_name: Provider name
            
        Returns:
            List of contracts
        """
        return [c for c in self.contracts if c.provider_name == provider_name]
    
    def get_all_contracts(self):
        """Get all contracts"""
        return self.contracts


# Example consumer contracts
def mobile_app_user_contract():
    """
    Contract from Mobile App for User API
    """
    contract = ConsumerContract("MobileApp", "UserAPI")
    
    # Interaction 1: Get user by ID
    contract.add_interaction(
        description="Get user by ID",
        request={
            'method': 'GET',
            'path': '/api/users/1'
        },
        response={
            'status': 200,
            'body': {
                'id': 1,
                'username': 'string',
                'email': 'string'
            }
        }
    )
    
    # Interaction 2: Create user
    contract.add_interaction(
        description="Create new user",
        request={
            'method': 'POST',
            'path': '/api/users',
            'body': {
                'username': 'john_doe',
                'email': 'john@example.com'
            }
        },
        response={
            'status': 201,
            'body': {
                'id': 'integer',
                'username': 'john_doe',
                'email': 'john@example.com'
            }
        }
    )
    
    return contract


def web_app_order_contract():
    """
    Contract from Web App for Order API
    """
    contract = ConsumerContract("WebApp", "OrderAPI")
    
    # Interaction: Get user orders
    contract.add_interaction(
        description="Get orders for user",
        request={
            'method': 'GET',
            'path': '/api/orders?user_id=1'
        },
        response={
            'status': 200,
            'body': {
                'orders': 'array',
                'count': 'integer'
            }
        }
    )
    
    return contract
