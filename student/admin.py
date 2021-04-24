from django.contrib import admin

from .models import Student, Teacher, Paper, Question, Grade

# Register your models here.
admin.site.site_header = '在线考试系统后台'
admin.site.site_title = '在线考试系统'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'dept', 'major', 'password', 'email', 'birth')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'dept', 'major', 'birth']
    list_filter = ['name', 'dept', 'major', 'birth']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'dept', 'password', 'email', 'birth')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'dept', 'birth']
    list_filter = ['name', 'dept']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'subject', 'title', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'level', 'chapter', 'score')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('tid', 'major', 'subject', 'exam_time', 'duration')
    list_display_links = ('major', 'subject', 'exam_time', 'duration')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('sid', 'subject', 'grade',)
    list_display_links = ('sid', 'subject', 'grade',)
