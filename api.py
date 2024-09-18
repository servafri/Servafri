from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import VM
from extensions import db

api = Blueprint('api', __name__)

@api.route('/vm/<int:vm_id>/<string:action>', methods=['POST'])
@login_required
def vm_action(vm_id, action):
    vm = VM.query.filter_by(id=vm_id, user_id=current_user.id).first()
    if not vm:
        return jsonify({'success': False, 'message': 'VM not found'}), 404

    if action == 'start':
        if vm.status == 'running':
            return jsonify({'success': False, 'message': 'VM is already running'}), 400
        vm.status = 'running'
    elif action == 'stop':
        if vm.status == 'stopped':
            return jsonify({'success': False, 'message': 'VM is already stopped'}), 400
        vm.status = 'stopped'
    elif action == 'delete':
        db.session.delete(vm)
    else:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': f'VM {action} successful'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error performing action: {str(e)}'}), 500

def init_app(app):
    app.register_blueprint(api, url_prefix='/api')
