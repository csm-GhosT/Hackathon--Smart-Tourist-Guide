from django.contrib import admin
from firstapp.models import user_data , searched_history
# Register your models here.
admin.site.register(user_data)
admin.site.register(searched_history)
