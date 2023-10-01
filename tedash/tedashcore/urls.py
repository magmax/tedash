from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name="index"),
    path('report/junit-xml', views.report_junit_xml, name="report-junit-xml"),
    path('project/<str:name>', views.project, name="project-detail"),
    path('project/<str:project_name>/report/<int:id>', views.report, name="report-detail"),
]
