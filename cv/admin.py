from django.contrib import admin
from cv import models

admin.site.register(models.ResumeTemplate)
admin.site.register(models.Resume)
admin.site.register(models.EducationHistory)
admin.site.register(models.EmploymentHistory)
admin.site.register(models.Qualification)
admin.site.register(models.Reference)
admin.site.register(models.Skill)
admin.site.register(models.WebLink)