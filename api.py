from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from models import VM, KubernetesDeployment
from extensions import db
from azure_utils import create_vm
from kubernetes_utils import create_deployment, list_deployments, delete_deployment
from datetime import datetime

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

        try:
            azure_vm = create_vm(args['name'], args['cpu_cores'], args['ram'], args['disk_size'])
            vm = VM(
                name=azure_vm['name'],
                cpu_cores=args['cpu_cores'],
                ram=args['ram'],
                disk_size=args['disk_size'],
                user_id=current_user.id,
                azure_id=azure_vm['id']
            )
            db.session.add(vm)
            db.session.commit()
            return {'message': 'VM provisioned successfully', 'id': vm.id, 'azure_id': azure_vm['id']}, 201
        except Exception as e:
            return {'message': f'Error provisioning VM: {str(e)}'}, 500

class KubernetesResource(Resource):
    @login_required
    def get(self):
        deployments = KubernetesDeployment.query.filter_by(user_id=current_user.id).all()
        return [{'id': dep.id, 'name': dep.name, 'image': dep.image, 'replicas': dep.replicas, 'status': dep.status} for dep in deployments]

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('replicas', type=int, default=1)
        args = parser.parse_args()

        try:
            success, message = create_deployment(args['name'], args['image'], args['replicas'])
            if success:
                deployment = KubernetesDeployment(
                    name=args['name'],
                    image=args['image'],
                    replicas=args['replicas'],
                    user_id=current_user.id,
                    created_at=datetime.utcnow(),
                    status='Created'
                )
                db.session.add(deployment)
                db.session.commit()
                return {'message': 'Kubernetes deployment created successfully', 'id': deployment.id}, 201
            else:
                return {'message': f'Error creating Kubernetes deployment: {message}'}, 500
        except Exception as e:
            return {'message': f'Error creating Kubernetes deployment: {str(e)}'}, 500

    @login_required
    def delete(self, deployment_id):
        deployment = KubernetesDeployment.query.filter_by(id=deployment_id, user_id=current_user.id).first()
        if deployment:
            try:
                success, message = delete_deployment(deployment.name)
                if success:
                    db.session.delete(deployment)
                    db.session.commit()
                    return {'message': 'Kubernetes deployment deleted successfully'}, 200
                else:
                    return {'message': f'Error deleting Kubernetes deployment: {message}'}, 500
            except Exception as e:
                return {'message': f'Error deleting Kubernetes deployment: {str(e)}'}, 500
        else:
            return {'message': 'Kubernetes deployment not found'}, 404

def initialize_api(api):
    api.add_resource(VMResource, '/api/vms')
    api.add_resource(KubernetesResource, '/api/kubernetes')
    api.add_resource(KubernetesResource, '/api/kubernetes/<int:deployment_id>', endpoint='kubernetes_delete')
