# app/models/__init__.py
"""
Models package - imports all models for easy access
"""
from .user import User
from .goal import Goal

# Make models available at package level
__all__ = ['User', 'Goal']