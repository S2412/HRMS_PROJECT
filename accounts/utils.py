# accounts/utils.py
import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, purpose='login'):
    subject = f"Your OTP for {purpose.capitalize()}"
    message = f"Your OTP code is: {otp}"
    send_mail(subject, message, 'admin@hrms.com', [email])