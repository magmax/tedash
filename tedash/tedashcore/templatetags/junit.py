from django import template

register = template.Library()

@register.filter(name="card_class")
def card_class(testcase):
    if testcase.get("error"):
        return "text-bg-danger"
    if testcase.get("failure"):
        return "text-bg-danger"
    if testcase.get("skipped"):
        return "text-bg-secondary"
    return "text-bg-success"

@register.filter(name="testcase_header")
def testcase_header(testcase):
    if testcase.get("error"):
        return f"ERROR: {testcase.get('error_message', 'Unknown reason')}"
    if testcase.get("failure"):
        return f"FAILED: {testcase.get('failure_message', 'Unknown reason')}"
    if testcase.get("skipped"):
        return f"SKIPPED: {testcase.get('skipped_message', 'Unknown reason')}"
    return "SUCCESS"
