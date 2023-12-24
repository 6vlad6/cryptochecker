from django.contrib import admin
from .models import *

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )

admin.site.register(Tag, TagAdmin)


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title', 'tags', )

admin.site.register(Developer, DeveloperAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('title', 'ticker', 'developer', 'description')
    list_filter = ('title', 'ticker', 'developer', 'tags', )

admin.site.register(Token, TokenAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'reason', 'qnt', 'price', 'date')
    list_filter = ('id', 'user', 'token', 'reason', 'date', )

admin.site.register(Transaction, TransactionAdmin)


class SavedTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('id', 'user', 'tokens', )

admin.site.register(SavedToken, SavedTokenAdmin)


class SavedDeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('id', 'user', 'developers', )

admin.site.register(SavedDeveloper, SavedDeveloperAdmin)
