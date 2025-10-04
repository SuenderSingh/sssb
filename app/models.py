# app/models.py
"""
Models module - imports all models from the models package
This maintains backward compatibility while organizing models in separate files
"""

# Import all models from the models package
from .models.user import User
from .models.goal import Goal

# Make models available at module level for backward compatibility
__all__ = ['User', 'Goal']
