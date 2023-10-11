from django.contrib import admin
from .models import UserMessages,UserExtraInformation,Contact,subscriber

admin.site.register(UserExtraInformation)
# admin.site.register(AdminMessages)
admin.site.register(UserMessages)
admin.site.register(Contact)
admin.site.register(subscriber)