from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from student import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^login/$', views.login),
    url(r'^student_login/', views.student_login),

    url(r'^teacher_login/', views.teacher_login),

    url(r'^$', views.login),
    url(r'^to_index/$', views.to_index),
    url('show_grade', views.show_grade),
    url('query_student', views.query_student),
    url(r'^start_exam/$', views.start_exam),
    url(r'^cal_grade/$', views.cal_grade),
    url(r'^logout/$', views.log_out),
]
