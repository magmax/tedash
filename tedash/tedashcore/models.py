from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created = models.DateTimeField()
    tests = models.PositiveIntegerField()
    failures = models.PositiveIntegerField()
    errors = models.PositiveIntegerField()
    skipped = models.PositiveIntegerField()
    assertions = models.PositiveIntegerField()
    time = models.DurationField()
    report = models.JSONField()

    def __str__(self):
        return f"{self.name} - {self.created}"
