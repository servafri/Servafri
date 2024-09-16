from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from extensions import db
from models import User, VM
from forms import LoginForm, SignupForm, VMProvisionForm

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
    return render_template('login.html', form=form)

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

@auth.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    vms = VM.query.filter_by(user_id=current_user.id).all()
    form = VMProvisionForm()
    return render_template('dashboard.html', vms=vms, form=form)

@auth.route('/provision_vm', methods=['POST'])
@login_required
def provision_vm():
    form = VMProvisionForm()
    if form.validate_on_submit():
        vm = VM(
            name=form.name.data,
            cpu_cores=form.cpu_cores.data,
            ram=form.ram.data,
            disk_size=form.disk_size.data,
            user_id=current_user.id
        )
        db.session.add(vm)
        db.session.commit()
        flash('VM provisioned successfully!')
    else:
        flash('Error provisioning VM. Please check your input.')
    return redirect(url_for('auth.dashboard'))