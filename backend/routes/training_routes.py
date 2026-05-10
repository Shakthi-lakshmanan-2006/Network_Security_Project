from flask import Blueprint, request, jsonify

training_bp = Blueprint('training', __name__, url_prefix='/api/training')

COURSES = [
    {
        'id': 'phishing-101',
        'name': 'Phishing Detection Basics',
        'description': 'Learn to identify and report phishing emails before they cause damage.',
        'modules': 4,
        'duration': '30 minutes',
        'category': 'Email Security',
        'difficulty': 'Beginner',
        'icon': 'email',
    },
    {
        'id': 'password-security',
        'name': 'Password Security Best Practices',
        'description': 'Create, store, and manage secure passwords using modern techniques.',
        'modules': 4,
        'duration': '25 minutes',
        'category': 'Account Security',
        'difficulty': 'Beginner',
        'icon': 'lock',
    },
    {
        'id': 'social-engineering',
        'name': 'Social Engineering Awareness',
        'description': 'Recognize and defend against social engineering and manipulation attacks.',
        'modules': 4,
        'duration': '40 minutes',
        'category': 'Human Threats',
        'difficulty': 'Intermediate',
        'icon': 'group',
    },
    {
        'id': 'data-protection',
        'name': 'Data Protection Fundamentals',
        'description': 'Protect sensitive information and comply with data security policies.',
        'modules': 4,
        'duration': '35 minutes',
        'category': 'Compliance',
        'difficulty': 'Intermediate',
        'icon': 'shield',
    },
    {
        'id': 'incident-response',
        'name': 'Incident Response Procedures',
        'description': 'Learn how to respond to, contain, and recover from security incidents.',
        'modules': 5,
        'duration': '45 minutes',
        'category': 'Response',
        'difficulty': 'Advanced',
        'icon': 'warning',
    },
]

@training_bp.route('/courses', methods=['GET'])
def get_courses():
    """Get available training courses"""
    return jsonify({'courses': COURSES, 'total': len(COURSES)}), 200

@training_bp.route('/progress', methods=['GET'])
def get_progress():
    """Get training progress (mock for dev)"""
    try:
        from models import TrainingProgress
        from database import db
        progress = db.session.query(TrainingProgress).all()
        return jsonify({'progress': [p.to_dict() for p in progress]}), 200
    except Exception:
        # Return mock data if DB empty
        return jsonify({'progress': [], 'total': 0}), 200

@training_bp.route('/update', methods=['POST'])
def update_progress():
    """Update training progress"""
    data = request.get_json() or {}
    course_id = data.get('course_id')
    module_id = data.get('module_id')
    user_id = data.get('user_id', 1)

    if not course_id or not module_id:
        return jsonify({'error': 'Course ID and Module ID required'}), 400

    try:
        from models import TrainingProgress
        from database import db
        from datetime import datetime

        progress = db.session.query(TrainingProgress).filter_by(
            user_id=user_id, course_id=course_id
        ).first()

        if not progress:
            progress = TrainingProgress(
                user_id=user_id,
                course_id=course_id,
                course_name=data.get('course_name', 'Security Course'),
                completed_modules=[],
                quiz_scores=[]
            )
            db.session.add(progress)

        if module_id not in (progress.completed_modules or []):
            progress.completed_modules = (progress.completed_modules or []) + [module_id]

        total_modules = next((c['modules'] for c in COURSES if c['id'] == course_id), 4)
        progress.completion_percentage = min(
            100, int((len(progress.completed_modules) / total_modules) * 100)
        )
        progress.last_accessed = datetime.utcnow()

        if progress.completion_percentage == 100 and not progress.completed:
            progress.completed = True
            progress.completed_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Progress updated', 'progress': progress.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500