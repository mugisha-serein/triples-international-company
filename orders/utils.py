from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):

    subject = f"Order Confirmation - Order #{order.id}"
    message = f"""
        Hi {order.user.username},

        Thank you for your order! Your order #{order.id} has been received.

        Total Amount: ${order.total_amount}
        Status: {order.status}

        You can view your order history in your account.

        Regards,
        Triple S International Company Ltd.
        """
    recipient_list = [order.customer_email]
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email for user_email in recipient_list],
        fail_silently=False,
    )