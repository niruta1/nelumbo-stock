from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Purpose)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Staff)
admin.site.register(StaffLeave)
admin.site.register(StaffFeedback)
admin.site.register(ItemRequest)
admin.site.register(Medicine)
admin.site.register(StockOut)
admin.site.register(Sale)
admin.site.register(Dispense)
