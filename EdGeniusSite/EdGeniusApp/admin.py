from django.contrib import admin
from .models import Courses, GoldTag, SilverTag, BronzeTag, Instructor
# Register your models here.
admin.site.register(Courses)
admin.site.register(GoldTag)
admin.site.register(SilverTag)
admin.site.register(BronzeTag)
admin.site.register(Instructor)