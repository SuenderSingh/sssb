from ..extensions import db
from datetime import datetime

class Goal(db.Model):
    __tablename__ = "goals"
    
    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    goal_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    goal_type = db.Column(db.String(50), nullable=False)  # personal, professional, health, etc.
    priority = db.Column(db.String(20), nullable=False, default="medium")  # low, medium, high
    category = db.Column(db.String(50), nullable=False)
    
    # Date fields
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Foreign key to link goal with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status fields
    is_completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.Date, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('goals', lazy=True, cascade='all, delete-orphan'))
    
    def to_dict(self):
        """Convert goal object to dictionary for JSON response"""
        return {
            'id': self.id,
            'goal_title': self.goal_title,
            'description': self.description,
            'goal_type': self.goal_type,
            'priority': self.priority,
            'category': self.category,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_completed': self.is_completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }
    
    def mark_completed(self):
        """Mark the goal as completed"""
        self.is_completed = True
        self.completion_date = datetime.utcnow().date()
        self.updated_at = datetime.utcnow()
    
    def mark_incomplete(self):
        """Mark the goal as incomplete"""
        self.is_completed = False
        self.completion_date = None
        self.updated_at = datetime.utcnow()
    
    @property
    def days_remaining(self):
        """Calculate days remaining until end date"""
        if self.end_date:
            today = datetime.utcnow().date()
            return (self.end_date - today).days
        return None
    
    @property
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.end_date and not self.is_completed:
            return datetime.utcnow().date() > self.end_date
        return False
    
    def __repr__(self):
        return f'<Goal {self.goal_title} ({self.priority})>'