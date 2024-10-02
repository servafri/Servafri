from extensions import db
from models import User, VM, Payment, KubernetesDeployment

def init_db():
    db.create_all()
    print("Database tables created successfully")

if __name__ == "__main__":
    init_db()
