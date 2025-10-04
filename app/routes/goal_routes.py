# app/routes/goal_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..extensions import db
from ..models import User, Goal

goal_bp = Blueprint("goals", __name__)

# Add Goal API
@goal_bp.route("/add/goal", methods=["POST"])
@jwt_required()
def add_goal():
    try:
        # Get current user
        user_id_str = get_jwt_identity()
        
        # Convert string back to integer with error handling
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid user ID in token"}), 401
            
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Debug: Print received data
        print(f"Received data: {data}")
        
        # Validate required fields
        required_fields = ['goal_title', 'goal_type', 'priority', 'category', 'start_date', 'end_date']
        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError as e:
            return jsonify({"error": f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}"}), 400
        
        # Validate date logic - allow same day goals
        if start_date > end_date:
            return jsonify({"error": "End date must be on or after start date"}), 400
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high']
        if data['priority'].lower() not in valid_priorities:
            return jsonify({"error": "Priority must be one of: low, medium, high"}), 400
        
        # Create new goal
        new_goal = Goal(
            goal_title=data['goal_title'],
            description=data.get('description', ''),
            goal_type=data['goal_type'],
            priority=data['priority'].lower(),
            category=data['category'],
            start_date=start_date,
            end_date=end_date,
            user_id=user_id
        )
        
        # Save to database
        db.session.add(new_goal)
        db.session.commit()
        
        return jsonify({
            "message": "Goal created successfully",
            "goal": new_goal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get All Goals API
@goal_bp.route("/goals", methods=["GET"])
@jwt_required()
def get_all_goals():
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)  # Convert string back to integer
        
        # Get query parameters for filtering
        goal_type = request.args.get('goal_type')
        priority = request.args.get('priority')
        category = request.args.get('category')
        is_completed = request.args.get('is_completed')
        
        # Build query
        query = Goal.query.filter_by(user_id=user_id)
        
        # Apply filters if provided
        if goal_type:
            query = query.filter_by(goal_type=goal_type)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        if is_completed is not None:
            completed = is_completed.lower() == 'true'
            query = query.filter_by(is_completed=completed)
        
        # Get goals ordered by creation date (newest first)
        goals = query.order_by(Goal.created_at.desc()).all()
        
        return jsonify({
            "goals": [goal.to_dict() for goal in goals],
            "total": len(goals)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update Goal API
@goal_bp.route("/goal/<int:goal_id>", methods=["PUT"])
@jwt_required()
def update_goal(goal_id):
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)  # Convert string back to integer
        
        # Find the goal
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        # Get request data
        data = request.get_json()
        
        # Update fields if provided
        if 'goal_title' in data:
            goal.goal_title = data['goal_title']
        if 'description' in data:
            goal.description = data['description']
        if 'goal_type' in data:
            goal.goal_type = data['goal_type']
        if 'priority' in data:
            if data['priority'].lower() in ['low', 'medium', 'high']:
                goal.priority = data['priority'].lower()
            else:
                return jsonify({"error": "Priority must be one of: low, medium, high"}), 400
        if 'category' in data:
            goal.category = data['category']
        if 'start_date' in data:
            try:
                goal.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
        if 'end_date' in data:
            try:
                goal.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        if 'is_completed' in data:
            goal.is_completed = data['is_completed']
            if data['is_completed']:
                goal.completion_date = datetime.utcnow().date()
            else:
                goal.completion_date = None
        
        # Validate date logic if both dates are present - allow same day goals
        if goal.start_date and goal.end_date and goal.start_date > goal.end_date:
            return jsonify({"error": "End date must be on or after start date"}), 400
        
        # Update timestamp
        goal.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            "message": "Goal updated successfully",
            "goal": goal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get Single Goal API
@goal_bp.route("/goal/<int:goal_id>", methods=["GET"])
@jwt_required()
def get_goal(goal_id):
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)  # Convert string back to integer
        
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        return jsonify({"goal": goal.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete Goal API
@goal_bp.route("/goal/<int:goal_id>", methods=["DELETE"])
@jwt_required()
def delete_goal(goal_id):
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)  # Convert string back to integer
        
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({"message": "Goal deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500