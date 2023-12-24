from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django import forms


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ('username',)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'img')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password',)}
            ),
        )

    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
