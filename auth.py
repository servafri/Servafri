from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from models import User, VM
from forms import LoginForm, SignupForm, VMProvisionForm
from extensions import db
from datetime import datetime, timedelta
import random

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('auth.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    # Resource usage (mock data for now)
    cpu_usage = random.randint(20, 80)
    memory_usage = random.randint(30, 90)
    storage_usage = random.randint(10, 70)
    
    # VM data
    vms = VM.query.filter_by(user_id=current_user.id).all()
    vm_count = len(vms)
    running_vm_count = sum(1 for vm in vms if vm.status == 'running')
    
    # Billing data
    current_balance = current_user.balance
    estimated_monthly_cost = sum(vm.cpu_cores * 10 + vm.ram * 5 + vm.disk_size * 0.1 for vm in vms)

    # Generate mock data for historical resource usage
    days = 7
    historical_data = {
        'dates': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days-1, -1, -1)],
        'cpu': [random.randint(20, 80) for _ in range(days)],
        'memory': [random.randint(30, 90) for _ in range(days)],
        'storage': [random.randint(10, 70) for _ in range(days)]
    }

    # Generate mock data for VM type distribution
    vm_types = ['Small', 'Medium', 'Large']
    vm_type_distribution = [random.randint(1, 10) for _ in range(len(vm_types))]

    # Generate mock data for network traffic
    network_traffic = {
        'incoming': [random.randint(50, 200) for _ in range(24)],
        'outgoing': [random.randint(30, 150) for _ in range(24)]
    }

    return render_template('dashboard.html',
                           cpu_usage=cpu_usage,
                           memory_usage=memory_usage,
                           storage_usage=storage_usage,
                           vm_count=vm_count,
                           running_vm_count=running_vm_count,
                           vms=vms,
                           current_balance=current_balance,
                           estimated_monthly_cost=estimated_monthly_cost,
                           historical_data=historical_data,
                           vm_types=vm_types,
                           vm_type_distribution=vm_type_distribution,
                           network_traffic=network_traffic)

@auth.route('/compute')
@login_required
def compute():
    return render_template('compute.html', vm_form=VMProvisionForm())

# Add other routes as needed
