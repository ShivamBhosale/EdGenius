from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class NewUser(User):
    CHOICES = [('Student', 'Student'), ('Instructor', 'Instructor')]
    user_type = models.CharField(max_length=10, choices=CHOICES, default='Student')

    def __str__(self):
        return self.first_name


class Student(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True, related_name='student')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    membership = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname


class Instructor(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True, related_name='instructor')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.firstname


@receiver(post_save, sender=NewUser)
def create_or_update_related_models(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Student":
            Student.objects.create(user=instance, firstname=instance.first_name, lastname=instance.last_name, email=instance.email)
        elif instance.user_type == "Instructor":
            Instructor.objects.create(user=instance, firstname=instance.first_name, lastname=instance.last_name, email=instance.email)
    else:
        if instance.user_type == "Student":
            try:
                model_type1 = Student.objects.get(user=instance)
                # Update additional data for ModelType1 here if needed
            except Student.DoesNotExist:
                Student.objects.create(user=instance, firstname=instance.first_name, lastname=instance.last_name, email=instance.email)
        elif instance.user_type == "Instructor":
            try:
                model_type2 = Instructor.objects.get(user=instance)
                # Update additional data for ModelType2 here if needed
            except Instructor.DoesNotExist:
                Instructor.objects.create(user=instance, firstname=instance.first_name, lastname=instance.last_name, email=instance.email)


class Membership(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student")
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

class Courses(models.Model):
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    course_image = models.ImageField(upload_to='course_images', blank=True)
    course_tag = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)
    course_video = models.CharField(max_length=1000, blank=True)
    course_files = models.ManyToManyField('CourseFile', blank=True)

    def __str__(self):
        return self.course_name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date = models.DateTimeField()
    attendance = models.CharField(max_length=50)

    def __str__(self):
        return self.student.firstname+' '+self.student.lastname+' || course: '+self.course.course_name

class Grades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    gradeItem = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    feedback = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.student.firstname+' '+self.student.lastname+' || course: '+self.course.course_name


class CourseEnrolled(models.Model):
    student = models.ForeignKey(Student, to_field= 'user', on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.firstname + ' ' + self.student.lastname + ' || course: ' + self.course.course_name

class CourseFile(models.Model):
    course_file = models.FileField(upload_to='course_files')

    def __str__(self):
        return self.course_file.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.course_name)
    if new_slug is not None:
        slug = new_slug
    qs = Courses.objects.filter(slug=slug).order_by('pk')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first())
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Courses)