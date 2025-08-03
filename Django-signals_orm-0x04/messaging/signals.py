from django.db.models.signals import post_save, pre_save, post_delete
from .models import Message, Notification, MessageHistory, User
from django.dispatch import receiver, Signal

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        sender = instance.sender
        receiver = conversation.participants.exclude(user_id=sender.user_id).first()
        if receiver:
            Notification.objects.create(
                message=instance,
                receiver=receiver,
                notification=f"You got one new message from {sender.first_name} sent at {instance.sent_at}."
            )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.message_body != instance.message_body:
               MessageHistory.objects.create(
                   Message=old_message,
                   old_body=old_message.message_body,
               )
               instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages where the user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications targeted at the user
    Notification.objects.filter(receiver=instance).delete()

    # Delete 