import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.StringIO(template), result)
    if not pdf.err:
        return result.getvalue()
    return None