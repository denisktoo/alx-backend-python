from django.db import models

    
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user).exclude(read_by=user).only('message_id', 'content', 'timestamp')
