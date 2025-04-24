from django.db import models
import datetime

class MessagesModel(models.Model):
    user = models.CharField(max_length=255, verbose_name='User')

    mid = models.CharField(max_length=255, db_index=True, verbose_name='Message ID', null=True, blank=True)
    message = models.TextField(verbose_name='Message')
    timestamp = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 5, 0, 0), verbose_name="Time:")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
