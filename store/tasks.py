from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation(email, order_id):
    try:
        subject = 'Order Confirmation'
        message = f'Your order with ID {order_id} has been successfully placed.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, email_from, recipient_list)
        return f'Email sent to {email}'
    except Exception as e:
        return f'Failed to send email: {str(e)}'


