from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class Instructor(models.Model):
    instructorName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.instructorName
class Courses(models.Model):
    CourseName = models.CharField(max_length=100)
    courseID = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1000)
    course_image = models.ImageField(upload_to='course_images', blank=True)
    course_tag = models.CharField(max_length=100)
    instructorName = models.ForeignKey(Instructor, max_length=100, on_delete=models.CASCADE,null=True)
    slug = models.SlugField(default='',max_length=100, null=True, blank=True)
    course_video = models.CharField(max_length=1000, blank=True)
    course_pdf = models.FileField(upload_to='course_pdfs', blank=True)
   
    def __str__(self):
        return self.CourseName
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.CourseName)
    if new_slug is not None:
        slug = new_slug
    qs = Courses.objects.filter(slug=slug).order_by('courseID')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().courseID)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Courses)
    
class GoldTag(models.Model):
    Course = models.ForeignKey(Courses,max_length=100,on_delete=models.CASCADE)
    
class SilverTag(models.Model):
    Course = models.ForeignKey(Courses,max_length=100,on_delete=models.CASCADE)
    
class BronzeTag(models.Model):
    Course = models.ForeignKey(Courses,max_length=100,on_delete=models.CASCADE)
    

    