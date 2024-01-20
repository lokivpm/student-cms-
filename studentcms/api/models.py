
from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
# import bcrypt
# pip install bcrypt






#staffs
class Staffs(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profilePhoto = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    staffCode = models.CharField(max_length=50,unique=True,null=True, blank=True)
    firstName = models.CharField(max_length=50,null=True, blank=True)
    lastName = models.CharField(max_length=100,null=True, blank=True)
    department=models.CharField(max_length=100,null=True, blank=True)
    staffType=models.CharField(max_length=100,null=True, blank=True)
    staffRoll=models.CharField(max_length=100,null=True, blank=True)
    dateOfJoining = models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=100,null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    maritalStatus=models.CharField(max_length=100,null=True, blank=True)
    bloodGroup=models.CharField(max_length=100,null=True, blank=True)
    mobileNumber=models.CharField(max_length=100,null=True, blank=True)
    emergencyMobileNumber=models.CharField(max_length=100,null=True, blank=True)
    verify_status=models.BooleanField(default=False)
    otp_digit=models.CharField(max_length=10,null=True)
    login_via_otp=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    # def set_password(self, raw_password):
    #     # Hash the password using bcrypt
    #     self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

    # def check_password(self, raw_password):
    #     # Check if the provided password matches the stored hash
    #     return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
   


# Course model
class Course(models.Model):
    code = models.CharField(max_length=10)
    course_description = models.TextField()
    course_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    academic_year=models.CharField(max_length=10,null=True, blank=True)
    semester=models.CharField(max_length=5, null=True, blank=True)
    course_duration=models.CharField(max_length=50, null=True, blank=True)
    grade_ponits=models.CharField(max_length=4, null=True, blank=True)
    regulation=models.CharField(max_length=4, null=True, blank=True)
    created_by = models.ForeignKey(Staffs, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.code
      

# Student model
class Student(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    profilePhoto = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    registerNumber = models.CharField(max_length=50,null=True, blank=True)
    rollNumber = models.CharField(max_length=50,null=True, blank=True)
    department = models.CharField(max_length=100,null=True, blank=True)
    firstName = models.CharField(max_length=100,null=True, blank=True)
    lastName = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    batch=models.CharField(max_length=100,null=True, blank=True)
    maritalStatus = models.CharField(max_length=20,null=True, blank=True)
    mobileNumber = models.CharField(max_length=15,null=True, blank=True)
    emergencyMobileNumber = models.CharField(max_length=15,null=True, blank=True)
    bloodGroup = models.CharField(max_length=5,null=True, blank=True)
    religion = models.CharField(max_length=20,null=True, blank=True)
    community = models.CharField(max_length=20,null=True, blank=True)
    admission_status = models.BooleanField(default=False)
    verify_status=models.BooleanField(default=False)
    otp_digit=models.CharField(max_length=10,null=True)
    login_via_otp=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.full_name
    

    
   
   
   


# Enrollment model
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='enrollments')
    subject_staff=models.ForeignKey(Staffs, on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

#grades
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)  
    pass_fail = models.CharField(max_length=4)  
    evaluation_type = models.CharField(max_length=20)

#trascript
class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    evaluation_type = models.CharField(max_length=50,null=True, blank=True)
    transcript_file = models.FileField(upload_to='transcripts/',null=True, blank=True)

   
  

#attendance
class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('OD', 'OnDuty'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    attendance = models.CharField(max_length=2, choices=ATTENDANCE_CHOICES)

    def __str__(self):
        return f"{self.enrollment.student} - {self.date} - {self.get_attendance_display()}"



class Announcement(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class StaffNotification(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class StudentNotification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)









class Applicant(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    desired_major = models.CharField(max_length=20)
    school_name=models.CharField(max_length=30)
    high_school_gpa = models.FloatField()
    aadhaar_number=models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='pending') 
    message = models.TextField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications',null=True, blank=True)
 

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True, blank=True)

class StaffStudentChat(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE,null=True, blank=True)
    student= models.ForeignKey(Student, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    msg_text=models.TextField(max_length=100)
    msg_from=models.CharField(max_length=100)
    msg_time=models.DateTimeField(auto_now_add=True)   


   

class Fees(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Fees {self.id} - Amount: {self.amount}, Student: {self.student.full_name if self.student else 'None'}"



  


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fees = models.ForeignKey(Fees, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField() 
    
    def __str__(self):
        return f"Payment {self.id} - Amount Paid: {self.amount_paid}, Student: {self.student.full_name if self.student else 'None'}"


