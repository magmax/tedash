import datetime
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from . import models
from . import forms
from .importers.junit import JunitImporter


@require_http_methods(["GET", "POST"])
@csrf_exempt
def report_junit_xml(request):
    if request.method == "GET":
        return render(request, "upload.html", {"form": forms.UploadFileForm()})
    form = forms.UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest()

    project, created = models.Project.objects.get_or_create(name=request.POST["project_name"])

    importer = JunitImporter(request.FILES["file"])
    metadata = importer.metadata
    now = datetime.datetime.now()
    report = models.Report.objects.create(
        project=project,
        name=metadata["name"],
        tests=metadata["tests"],
        failures=metadata.get("failures"),
        errors=metadata.get("errors"),
        skipped=metadata.get("skipped"),
        assertions=metadata.get("assertions"),
        time=datetime.timedelta(seconds=metadata.get("duration" , 0)),
        created=datetime.datetime.fromisoformat(metadata.get("timestamp")),
        report=importer.data,
    )

    return render(request, "import_report.html", {"msg": "Imported"})

@require_http_methods(["GET"])
def projects(request):
    projects = models.Project.objects.all()
    return render(request, "projects.html", {"projects": projects})

@require_http_methods(["GET"])
def project(request, name):
    project = models.Project.objects.prefetch_related().get(name=name)
    return render(request, "project-detail.html", {"project": project})

@require_http_methods(["GET"])
def report(request, project_name, id):
    report = models.Report.objects.prefetch_related().get(pk=id)
    import json
    print(json.dumps(report.report, indent=2))
    return render(request, "report-detail.html", {"report": report})


