import os
from io import BytesIO

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# ToDO refactor both functions
@admin.action(description="PDF Druck")
def generate_pdf(modeladmin, request, queryset):

    template_path = "pdf/report.html"
    context = {
        "items": queryset,
    }
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    # create a pdf
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding="UTF-8",
        link_callback=fetch_pdf_resources,
    )

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


@admin.action(description="EAN Druck")
def generate_ean_pdf(modeladmin, request, queryset):

    template_path = "pdf/ean.html"
    context = {
        "items": queryset,
    }

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    # create a pdf
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding="UTF-8",
        link_callback=fetch_pdf_resources,
    )

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def fetch_pdf_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    static_url = settings.STATIC_URL  # Typically /static/
    static_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    media_url = settings.MEDIA_URL  # Typically /static/media/
    media_root = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    return path
