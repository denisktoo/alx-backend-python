from django.db.models.signals import post_save
from .models import Message, Notification
from django.dispatch import receiver, Signal

# @receiver(post_save, sender=Message)
# def create_notification_on_new_message(sender, instance, created, **kwargs):
#     if created:
#         conversation = instance.conversation
#         sender = instance.sender
#         receiver = conversation.participants.exclude(user_id=sender.user_id).first()
#         if receiver:
#             Notification.objects.create(
#                 message=instance,
#                 receiver=receiver,
#                 notification=f"You got one new message from {sender.first_name} sent at {instance.sent_at}."
#             )
