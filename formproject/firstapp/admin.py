from django.contrib import admin
from firstapp.models import user_data , searched_history,monument_reviews,information
# Register your models here.
admin.site.register(user_data)
admin.site.register(searched_history)
admin.site.register(monument_reviews)
admin.site.register(information)
