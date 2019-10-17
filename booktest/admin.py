from django.contrib import admin
from booktest.models import *

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','tittle','pub_date']

class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id','name','content','gender','book']


admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(HeroInfo,HeroInfoAdmin)
# Register your models here.
