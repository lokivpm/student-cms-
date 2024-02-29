
from rest_framework import serializers

from . import models
from .models import Enrollment,StaffNotification,StudentNotification
from .models import Grade,Transcript,Attendance,Student
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.hashers import make_password


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user




class StaffsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Staffs
        fields='__all__'

    def create(self,validate_data):
      email=self.validated_data ['email'] 
      otp_digit=self.validated_data['otp_digit']
      instance=super(StaffsSerializer,self).create(validate_data) 
      send_mail(
                'Verify Account',
                'please verify your account ',
                'logapriya202@gmail.com',
                [email],
                fail_silently=False,
                html_message=f'<p> Your OTP is </p><p>{otp_digit}</p>'
            )
      return instance
    
    


      



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
       model=models.Student
       fields='__all__'
    def create(self,validate_data):
       email=self.validated_data ['email'] 
       otp_digit=self.validated_data['otp_digit']
       instance=super(StudentSerializer,self).create(validate_data) 
       send_mail(
                'Verify Account',
                'please verify your account ',
                'logapriya202@gmail.com',
                [email],
                fail_silently=False,
                html_message=f'<p> Your OTP is </p><p>{otp_digit}</p>'
            )
       return instance 
    


#class StudentProfileSerializer(serializers.ModelSerializer):
       #class Meta:
        ##  fields = ['id', 'profilePhoto', 'registerNumber', 'rollNumber', 'department', 'firstName', 'lastName', 'gender', 'dateOfBirth', 'maritalStatus', 'mobileNumber', 'emergencyMobileNumber', 'bloodGroup', 'email', 'religion',  'community',]

 


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'  

class StudentAndCourseInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    semester= serializers.SerializerMethodField()
    regulation= serializers.SerializerMethodField()
    registerNumber= serializers.SerializerMethodField()
    batch=serializers.SerializerMethodField()
    class Meta:
        model = Enrollment
        fields = ['id', 'enrollment_date', 'student', 'course', 'full_name', 'code', 'category','semester','registerNumber','batch','regulation']

    def get_full_name(self, obj):
        return obj.student.full_name
    
    def get_registerNumber(self, obj):
        return obj.student.registerNumber
    
    def get_batch(self, obj):
        return obj.student.batch
    
    def get_code(self, obj):
        return obj.course.code
    
    def get_semester(self, obj):
        return obj.course.semester
  
    def get_category(self, obj):
        return obj.course.category
    
    def get_regulation(self, obj):
        return obj.course.regulation

# class StudentAndCourseInfoSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source='student.full_name')
#     code = serializers.CharField(source='course.code')
#     category = serializers.CharField(source='course.category')
#     semester = serializers.CharField(source='course.semester')
#     registerNumber = serializers.CharField(source='student.registerNumber')
#     batch = serializers.CharField(source='student.batch')

#     class Meta:
#         model = Enrollment
#         fields = ['id', 'enrollment_date', 'student', 'course', 'full_name', 'code', 'category', 'semester', 'registerNumber', 'batch']




class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_code = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    semester= serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ['id', 'grade', 'pass_fail', 'evaluation_type', 'student', 'course', 'student_name', 'course_code', 'category', 'course_type','semester','grade_academic_year']

    def get_student_name(self, obj):
        return obj.student.full_name

    def get_course_code(self, obj):
        return obj.course.code

    def get_category(self, obj):
        return obj.course.category

    def get_course_type(self, obj):
        return obj.course.course_type
    
    def get_semester(self, obj):
        return obj.course.semester



class TranscriptViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['id', 'student', 'content', 'evaluation_type']

class TranscriptGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['student', 'content', 'evaluation_type']


# class CustomTimeField(serializers.TimeField):
#     def to_representation(self, value):
#         if isinstance(value, datetime.time):
#             return value.strftime('%H:%M:%S')
#         return super().to_representation(value)
       



class TimeField(serializers.TimeField):
    def to_representation(self, value):
        # Convert datetime to time
        if value:
            return value.strftime('%H:%M:%S')
        return None




class AttendanceSerializer(serializers.ModelSerializer):
    student_id = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    semester= serializers.SerializerMethodField()
  
    start_time = TimeField()
    end_time = TimeField()

    class Meta:
        model = Attendance
        fields = ['id', 'enrollment', 'date', 'start_time', 'end_time', 'attendance', 'student_id', 'course_type', 'category','semester','period','attendance_academic_year']

    def get_student_id(self, obj):
        return obj.enrollment.student.id

    def get_course_type(self, obj):
        return obj.enrollment.course.course_type

    def get_category(self, obj):
        return obj.enrollment.course.category
    
    def get_semester(self, obj):
        return obj.enrollment.course.semester
  

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time is not None and end_time is not None:
            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time.")

        return data
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Ensure that start_time and end_time are represented as strings
        representation['start_time'] = self.format_time(instance.start_time) if instance.start_time else None
        representation['end_time'] = self.format_time(instance.end_time) if instance.end_time else None
       
        return representation

    def format_time(self, time):
        # Custom method to format time while handling timezone
        if time.tzinfo is not None:
            return time.strftime('%H:%M:%S %z')
        else:
            return time.strftime('%H:%M:%S')






class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = '__all__'

class StaffNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffNotification
        fields = '__all__'

class StudentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentNotification
        fields = '__all__'



#class MessageSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Message
        #fields = ['id', 'sender_student', 'sender_staff', 'receiver_student', 'receiver_staff', 'content', 'timestamp']

class ApplicantSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = models.Applicant
        fields = '__all__'



class DocumentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    registerno = serializers.SerializerMethodField()

    class Meta:
        model = models.Document
        fields = ['id', 'student', 'title', 'file', 'created_at', 'registerno', 'student_name']

    def get_student_name(self, obj):
        student = obj.student
        if student:
            return student.full_name
        return None

    def get_registerno(self, obj):
        student = obj.student
        if student:
            return student.registerNumber
        return None



class StaffStudentChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffStudentChat
        fields = ['id' ,'staff','student','msg_from','msg_text','msg_time','user']  
    def to_representation(self, instance):
        representation=super(StaffStudentChatSerializer,self).to_representation(instance)
        representation['msg_time']=instance.msg_time.strftime("%Y-%m-%d %H:%M")
        return representation      
    



class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fees
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = '__all__'  


# class OverallReportSerializer(serializers.Serializer):
#     attendance = serializers.SerializerMethodField()
#     grades = serializers.SerializerMethodField()

#     class Meta:
#         fields = ['attendance', 'grades']

#     def get_attendance(self, instance):
#         attendance_data = Attendance.objects.all()
#         return AttendanceSerializer(attendance_data, many=True).data

#     def get_grades(self, instance):
#         grades_data = Grade.objects.all()
#         return GradeSerializer(grades_data, many=True).data
    

class OverallReportSerializer(serializers.Serializer):
    attendance = serializers.SerializerMethodField()
    grades = serializers.SerializerMethodField()
    applicants = serializers.SerializerMethodField()
    batch=serializers.SerializerMethodField()

    class Meta:
        fields = ['attendance', 'grades', 'applicants','batch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, value in representation.items():
            if isinstance(value, list) and all(isinstance(item, int) for item in value):
                # Handle the case where the field is a list of integers
                continue
            representation[field_name] = self.fields[field_name].to_representation(value)
        return representation

    def get_attendance(self, instance):
        attendance_data = Attendance.objects.all()
        return AttendanceSerializer(attendance_data, many=True).data

    def get_grades(self, instance):
        grades_data = Grade.objects.all()
        return GradeSerializer(grades_data, many=True).data

   
    def get_applicants(self, instance):
        applicants_data = models.Applicant.objects.all()
        return ApplicantSerializer(applicants_data, many=True).data
    
    def get_batch(self, instance):
        batch_data = Student.objects.all()
        return StudentSerializer(batch_data, many=True).data


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = ['question', 'answer']




 




class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Contact
        fields = ['id', 'username','email','query','add_time']   
   


    # class OverallReportSerializer(serializers.Serializer):
    # attendance = serializers.SerializerMethodField()
    # grades = serializers.SerializerMethodField()

    # class Meta:
    #     fields = ['attendance', 'grades']

    # def get_attendance(self, instance):
    #     attendance_data = Attendance.objects.all()
    #     return AttendanceSerializer(attendance_data, many=True).data

    # def get_grades(self, instance):
    #     grades_data = Grade.objects.all()
    #     return GradeSerializer(grades_data, many=True).data