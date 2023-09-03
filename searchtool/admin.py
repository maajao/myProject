from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Database, UserManager, User, Tag

admin.site.register(Database)
admin.site.register(User)
admin.site.register(Tag)
# admin.site.register(UserManager)

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email"]

    def save(self, commit=True):
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "is_admin"]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.Meta.fields.remove("password")

class UserAdminA(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = (
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    )

    add_fieldsets = (
        (None, {
            "fields": ["email", "password"]}
         ),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


#admin.site.register(User, UserAdmin)
