from django.contrib import admin
from .models import MessagesModel, PendingMessagesModel

admin.site.register(MessagesModel, PendingMessagesModel)
