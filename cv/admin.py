from django.contrib import admin
from cv import models

admin.site.register(models.ResumeTemplate)
admin.site.register(models.Resume)