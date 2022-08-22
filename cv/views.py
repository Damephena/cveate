from django_renderpdf.views import PDFView
from django.views.generic.detail import DetailView
from rest_framework import generics, permissions, viewsets

from .custom_permissions import IsOwnerOrAdmin
from .models import (EducationHistory, EmploymentHistory, Qualification,
                     Reference, Resume, ResumeTemplate, Skill, WebLink)
from .serializers import ResumeSerializer, ResumeTemplateSerializer

# from django_xhtml2pdf.views import PdfMixin
# from xhtml2pdf import pisa
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import pdfkit
# from django_xhtml2pdf.utils import generate_pdf

# def generate(response, pk):
#     resume = Resume.objects.get(id=pk)
#     context = {"resume": Resume.objects.get(id=pk)}
#     context["employment_history"] = EmploymentHistory.objects.filter(resume=resume.id)

#     context["education_history"] = EducationHistory.objects.filter(resume=resume.id)

#     context["web_links"] = WebLink.objects.filter(resume=resume.id)
#     context["skills"] = Skill.objects.filter(resume=resume.id)
#     context["qualifications"] = Qualification.objects.filter(resume=resume.id)
#     context["references"] = Reference.objects.filter(resume=resume.id)
#     template_name = f"resumes/{context['resume'].resume_template.name}.html"
#     resp = HttpResponse(content_type='application/pdf')
#     result = generate_pdf(template_name, file_object=resp)
#     return result

# def generate_pdf(request):
#     report = Resume.objects.all()
#     template_path = 'profile_brand_report.html'

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Report.pdf"'

#     html = render_to_string(template_path, {'report': report})
#     print (html)

#     pisaStatus = pisa.CreatePDF(html, dest=response)

#     return response

# # def generate(request, pk):
#     """Pass some extra context to the template."""
#     resume = Resume.objects.get(id=pk)
#     context = {"resume": Resume.objects.get(id=pk)}
#     context["employment_history"] = EmploymentHistory.objects.filter(resume=resume.id)

#     context["education_history"] = EducationHistory.objects.filter(resume=resume.id)

#     context["web_links"] = WebLink.objects.filter(resume=resume.id)
#     context["skills"] = Skill.objects.filter(resume=resume.id)
#     context["qualifications"] = Qualification.objects.filter(resume=resume.id)
#     context["references"] = Reference.objects.filter(resume=resume.id)
#     template_name = f"resumes/{context['resume'].resume_template.name}.html"

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Report.pdf"'

#     html = render_to_string(template_name, context)
#     print (html)

#     pisaStatus = pisa.CreatePDF(html, dest=response)

#     # return response
#     return response
class ProductPdfView(PDFView, generics.RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    # template_name = "product_pdf.html"

    def get_context_data(self, *args, **kwargs):

        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)

        resume = Resume.objects.get(id=kwargs["pk"])

        context["resume"] = Resume.objects.get(id=kwargs["pk"])
        context["employment_history"] = EmploymentHistory.objects.filter(
            resume=resume.id
        )
        context["education_history"] = EducationHistory.objects.filter(resume=resume.id)
        context["web_links"] = WebLink.objects.filter(resume=resume.id)
        context["skills"] = Skill.objects.filter(resume=resume.id)
        context["qualifications"] = Qualification.objects.filter(resume=resume.id)
        context["references"] = Reference.objects.filter(resume=resume.id)

        # Gets the template_name dynamically
        self.template_name = f"pdf/{context['resume'].resume_template.name}.html"
        self.download_name = (
            f"{context['resume'].resume_template.name}_{context['resume'].first_name}.pdf"
        )
        self.prompt_download = True

        return context



class ResumeTemplateViewset(viewsets.ModelViewSet):

    """
    list: List all resume templates,
    retrieve: Get a single resume template by ID.
    """

    queryset = ResumeTemplate.objects.all()
    serializer_class = ResumeTemplateSerializer
    http_method_names = ["get"]


class ResumeViewset(viewsets.ModelViewSet):

    """
    list: List all resumes belonging to this authenticated user.
    create: Create a new resume as an authenticated user.
    retrieve: Retrieve resume (by ID) belonging to this authenticated user.
    partial_update: Update resume (by ID) belonging to this authenticated user.
    destroy: Delete resume (by ID) belonging to this authenticated user.
    """

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action != "create":
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        try:
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                return Resume.objects.filter(user_id=self.request.user)
        except Exception:
            return Resume.objects.none()
        return super().get_queryset()


class ResumePDFView(generics.RetrieveAPIView):

    """
    Generate resumes based on provided HTML files.
    Note: CSS is adviced to be in `<style></style>` tags compared to external sheet.
    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    `prompt_download` attribute set as `True` begins download immediately
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_context_data(self, *args, **kwargs):

        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)

        resume = Resume.objects.get(id=kwargs["pk"])

        context["resume"] = Resume.objects.get(id=kwargs["pk"])
        context["employment_history"] = EmploymentHistory.objects.filter(
            resume=resume.id
        )
        context["education_history"] = EducationHistory.objects.filter(resume=resume.id)
        context["web_links"] = WebLink.objects.filter(resume=resume.id)
        context["skills"] = Skill.objects.filter(resume=resume.id)
        context["qualifications"] = Qualification.objects.filter(resume=resume.id)
        context["references"] = Reference.objects.filter(resume=resume.id)

        # Gets the template_name dynamically
        self.template_name = f"pdf/{context['resume'].resume_template.name}.html"
        self.download_name = (
            f"{context['resume'].resume_template.name}_{context['resume'].first_name}.pdf"
        )
        self.prompt_download = True

        return context
