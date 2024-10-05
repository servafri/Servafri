import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from urllib.parse import urlparse, urlencode
from models import User, VM, Payment
from forms import VMProvisionForm, BillingForm
from extensions import mongo
from azure_utils import create_vm
from paystackapi.paystack import Paystack
from datetime import datetime
import requests
import hmac
import hashlib
import os

auth = Blueprint('auth', __name__)

@auth.route('/dashboard')
def dashboard():
    if 'profile' not in session:
        return redirect(url_for('login'))
    
    user = User.get_user_by_email(session['profile']['email'])
    vms = VM.get_vms_by_user_id(user.get_id())
    vm_form = VMProvisionForm()
    billing_form = BillingForm()
    return render_template('dashboard.html', user=user, vms=vms, vm_form=vm_form, billing_form=billing_form)

@auth.route('/provision_vm', methods=['POST'])
def provision_vm():
    if 'profile' not in session:
        return redirect(url_for('login'))
    
    form = VMProvisionForm()
    if form.validate_on_submit():
        try:
            user = User.get_user_by_email(session['profile']['email'])
            azure_vm = create_vm(form.name.data, form.cpu_cores.data, form.ram.data, form.disk_size.data, form.os_image.data)
            vm = VM(
                name=azure_vm['name'],
                cpu_cores=form.cpu_cores.data,
                ram=form.ram.data,
                disk_size=form.disk_size.data,
                user_id=user.get_id(),
                azure_id=azure_vm['id'],
                ip_address=azure_vm['ip_address'],
                os_image=form.os_image.data
            )
            vm.save()
            flash('VM provisioned successfully!', 'success')
        except Exception as e:
            flash(f'Error provisioning VM: {str(e)}', 'error')
    else:
        flash('Error provisioning VM. Please check your input.', 'error')
    return redirect(url_for('auth.dashboard'))

@auth.route('/payment', methods=['POST'])
def payment():
    if 'profile' not in session:
        return redirect(url_for('login'))
    
    form = BillingForm()
    if form.validate_on_submit():
        try:
            user = User.get_user_by_email(session['profile']['email'])
            paystack = Paystack(secret_key=os.environ.get('PAYSTACK_SECRET_KEY'))
            response = paystack.transaction.initialize(
                amount=int(form.amount.data * 100),
                email=form.email.data,
                callback_url=url_for('auth.verify_payment', _external=True)
            )
            if response['status']:
                payment = Payment(
                    user_id=user.get_id(),
                    amount=form.amount.data,
                    reference=response['data']['reference'],
                    status='pending',
                    created_at=datetime.utcnow()
                )
                payment.save()
                return redirect(response['data']['authorization_url'])
            else:
                flash('Error initializing payment. Please try again.', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Network error: Unable to connect to payment gateway. Please try again later.', 'error')
        except KeyError as e:
            flash(f'Unexpected response from payment gateway. Please try again or contact support.', 'error')
        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}. Please try again or contact support.', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'error')
    return redirect(url_for('auth.dashboard'))

@auth.route('/verify_payment')
def verify_payment():
    if 'profile' not in session:
        return redirect(url_for('login'))
    
    reference = request.args.get('reference')
    if reference:
        try:
            paystack = Paystack(secret_key=os.environ.get('PAYSTACK_SECRET_KEY'))
            response = paystack.transaction.verify(reference)
            if response['status']:
                payment = mongo.db.payments.find_one({"reference": reference})
                if payment:
                    mongo.db.payments.update_one({"_id": payment['_id']}, {"$set": {"status": "success"}})
                    user = User.get_user_by_email(session['profile']['email'])
                    user.balance += payment['amount']
                    user.save()
                    flash('Payment successful! Your balance has been updated.', 'success')
                else:
                    flash('Payment verification failed. Please contact support.', 'error')
            else:
                flash('Payment verification failed. Please try again or contact support.', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Network error: Unable to verify payment. Please check your account balance and contact support if needed.', 'error')
        except KeyError as e:
            flash(f'Unexpected response during payment verification. Please contact support.', 'error')
        except Exception as e:
            flash(f'An unexpected error occurred during payment verification: {str(e)}. Please contact support.', 'error')
    else:
        flash('Invalid payment reference.', 'error')
    return redirect(url_for('auth.dashboard'))

@auth.route('/paystack_webhook', methods=['POST'])
def paystack_webhook():
    payload = request.data
    signature = request.headers.get('X-Paystack-Signature')

    if not signature:
        return 'No signature', 400

    secret = os.environ.get('PAYSTACK_SECRET_KEY').encode('utf-8')
    computed_signature = hmac.new(secret, payload, hashlib.sha512).hexdigest()

    if signature != computed_signature:
        return 'Invalid signature', 400

    event = request.json
    if event and event['event'] == 'charge.success':
        reference = event['data']['reference']
        payment = mongo.db.payments.find_one({"reference": reference})
        if payment:
            mongo.db.payments.update_one({"_id": payment['_id']}, {"$set": {"status": "success"}})
            user = User.get_user_by_id(payment['user_id'])
            if user:
                user.balance += payment['amount']
                user.save()
                return 'Webhook processed', 200
            else:
                return 'User not found', 404
        else:
            return 'Payment not found', 404
    
    return 'Webhook received', 200
