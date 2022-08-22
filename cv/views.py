from django_renderpdf.views import PDFView
from rest_framework import generics, permissions, viewsets

from .custom_permissions import IsOwnerOrAdmin
from .models import (EducationHistory, EmploymentHistory, Qualification,
                     Reference, Resume, ResumeTemplate, Skill, WebLink)
from .serializers import ResumeSerializer, ResumeTemplateSerializer


class ResumePDFView(PDFView, generics.RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

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
        self.template_name = f"resumes/{context['resume'].resume_template.name}.html"
        self.download_name = (
            f"{context['resume'].resume_template.name}_{context['resume'].first_name}.pdf"
        )
        self.prompt_download = False

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
