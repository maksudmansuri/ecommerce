from django.contrib import admin
# from .models import Account
from accounts.models import CustomUser,Admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=('email','username')
    search_fields = ('email','username',)
    filter_horizontal = ()
    list_filter = ()
    # fieldsets = [
    #     ("Course basic Details",{"fields": ["course_code","course_name","course_category","course_subcategory","course_fee","course_duration"]}),
    #     ("Course Details",{"fields": ["course_image","course_video","course_level","course_slug","course_ratting","course_pub_date"]}),
    #     ("Course Desc",{"fields": ["course_requirement","course_desc","course_why_take","course_syllabus","course_in_pdf"]})

    # ]

admin.site.register(CustomUser,CustomUserAdmin)


