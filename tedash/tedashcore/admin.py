from django.contrib import admin
from . import models

class ReportInline(admin.TabularInline):
    model = models.Report
    exclude = [
        "report",
    ]

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ReportInline,
    ]

@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    pass
