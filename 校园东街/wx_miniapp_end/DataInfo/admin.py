from django.contrib import admin
from .models import Lost, Found, Info, YZW


# Register your models here.
# 寻物启事数据库管理类
class LostManager(admin.ModelAdmin):
    list_display = ['title', 'contact', 'tel']
    list_display_links = ['title']
    list_filter = ['contact']
    search_fields = ['title']
    list_per_page = 50


# 失物招领数据库管理类
class FoundManager(admin.ModelAdmin):
    list_display = ['title', 'contact', 'tel']
    list_display_links = ['title']
    list_filter = ['contact']
    search_fields = ['title']
    list_per_page = 50


# 校园资讯数据库管理类
class InfoManger(admin.ModelAdmin):
    list_display = ['id', 'title', 'kind', 'department']
    list_display_links = ['id']
    list_filter = ['kind', 'department']
    search_fields = ['title']
    list_per_page = 50


# 考研信息管理类
class YZWManger(admin.ModelAdmin):
    list_display = ['id', 'School', 'College', 'Major', 'Number', 'Lesson_1', 'Lesson_2', 'Lesson_3', 'Lesson_4']
    list_display_links = ['id']
    list_filter = ['Lesson_2', 'Lesson_3', ]
    search_fields = ['Lesson_4']
    list_per_page = 50


admin.site.register(Lost, LostManager)
admin.site.register(Found, FoundManager)
admin.site.register(Info, InfoManger)
admin.site.register(YZW, YZWManger)
