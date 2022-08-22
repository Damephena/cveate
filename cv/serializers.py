from rest_framework import serializers

from cv import models


class ResumeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeTemplate
        fields = ["name", "template_image", "id"]


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EducationHistory
        exclude = ["resume"]


class EmploymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmploymentHistory
        exclude = ["resume"]


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        exclude = ["resume"]


class WebLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebLink
        exclude = ["resume"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        exclude = ["resume"]


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Qualification
        exclude = ["resume"]


class ResumeSerializer(serializers.ModelSerializer):
    employment_history_set = EmploymentHistorySerializer(many=True, required=False)
    educational_history_set = EducationHistorySerializer(many=True, required=False)
    link_set = WebLinkSerializer(many=True, required=False)
    skill_set = SkillSerializer(many=True, required=False)
    qualification_set = QualificationSerializer(many=True, required=False)
    reference_set = ReferenceSerializer(many=True, required=False)

    class Meta:
        model = models.Resume
        fields = (
            "id",
            "user_id",
            "resume_template",
            "job_title",
            "first_name",
            "last_name",
            "email",
            "professional_summary",
            "employment_history_set",
            "educational_history_set",
            "link_set",
            "skill_set",
            "qualification_set",
            "reference_set",
        )
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        employment_history_validated_data = validated_data.pop("employment_history_set")
        educational_history_validated_data = validated_data.pop(
            "educational_history_set"
        )
        link_validated_data = validated_data.pop("link_set")
        skill_validated_data = validated_data.pop("skill_set")
        qualification_validated_data = validated_data.pop("qualification_set")
        reference_validated_data = validated_data.pop("reference_set")

        employment_history_serializer = self.fields["employment_history_set"]
        educational_history_serializer = self.fields["educational_history_set"]
        link_validated_serializer = self.fields["link_set"]
        skill_serializer = self.fields["skill_set"]
        qualification_serializer = self.fields["qualification_set"]
        reference_serializer = self.fields["reference_set"]

        resume = models.Resume.objects.create(**validated_data)

        for each in employment_history_validated_data:
            each["resume"] = resume
        employment_history_serializer.create(employment_history_validated_data)

        for each in educational_history_validated_data:
            each["resume"] = resume
        educational_history_serializer.create(educational_history_validated_data)

        for each in link_validated_data:
            each["resume"] = resume
        link_validated_serializer.create(link_validated_data)

        for each in skill_validated_data:
            each["resume"] = resume
        skill_serializer.create(skill_validated_data)

        for each in qualification_validated_data:
            each["resume"] = resume
        qualification_serializer.create(qualification_validated_data)

        for each in reference_validated_data:
            each["resume"] = resume
        reference_serializer.create(reference_validated_data)

        return resume
