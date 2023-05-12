from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LIMSuser
from .forms import LIMSuserChangeForm, LIMSuserForm

class LIMSuserAdmin(UserAdmin):
    add_form=LIMSuserForm
    form=LIMSuserChangeForm
    model=LIMSuser
    list_display=("email", "is_staff", "is_active", "first_name", "last_name","company")
    list_filter=("email", "is_staff", "is_active", "first_name", "last_name","company")
    fieldsets =(
        (None, {"fields": ("email", "password", "first_name", "last_name","company")}),
        ("Permissions", {"fields":("is_staff", "is_active", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes":("wide",),
            "fields" : (
                "email", "password1", "password2", "company", "is_staff", 
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering= ("email",)

admin.site.register(LIMSuser, LIMSuserAdmin)