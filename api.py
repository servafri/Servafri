from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from models import VM
from extensions import db

class VMResource(Resource):
    @login_required
    def get(self):
        vms = VM.query.filter_by(user_id=current_user.id).all()
        return [{'id': vm.id, 'name': vm.name, 'cpu_cores': vm.cpu_cores, 'ram': vm.ram, 'disk_size': vm.disk_size} for vm in vms]

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('cpu_cores', type=int, required=True)
        parser.add_argument('ram', type=int, required=True)
        parser.add_argument('disk_size', type=int, required=True)
        args = parser.parse_args()

        vm = VM(name=args['name'], cpu_cores=args['cpu_cores'], ram=args['ram'], disk_size=args['disk_size'], user_id=current_user.id)
        db.session.add(vm)
        db.session.commit()

        return {'message': 'VM provisioned successfully', 'id': vm.id}, 201

def initialize_api(api):
    api.add_resource(VMResource, '/api/vms')
