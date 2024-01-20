
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics
from .serializers import StaffsSerializer,StudentSerializer,CourseSerializer,StudentAndCourseInfoSerializer,GradeSerializer,AttendanceSerializer,FeesSerializer, PaymentSerializer,OverallReportSerializer
from rest_framework.decorators import api_view,permission_classes
from .models import Enrollment,StudentNotification
from .serializers import EnrollmentSerializer,AnnouncementSerializer,StudentNotificationSerializer,StaffNotificationSerializer,ApplicantSerializer,DocumentSerializer,StaffStudentChatSerializer
from .models import Course,Grade, Student,Transcript,StaffNotification
from rest_framework import viewsets
from .import models 
from rest_framework import status
from django.shortcuts import redirect
from django.db.models import Q
from .models import Grade,Staffs,Attendance,Applicant,Fees, Payment
import stripe
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from rest_framework.permissions import AllowAny
from django.views.decorators.http import require_POST
from .models import Document
from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, Http404
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.decorators import method_decorator
from reportlab.lib.pagesizes import letter
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.core.mail import send_mail
from random import randint
import base64
from io import BytesIO


class LoginView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'token': access_token, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User account is disabled'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#Staffs
class StaffsList(generics.ListCreateAPIView):
  queryset=models.Staffs.objects.all()
  serializer_class=StaffsSerializer
 # permission_classes=[permissions.IsAuthenticated]


class StaffsDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset=models.Staffs.objects.all()
  serializer_class=StaffsSerializer
  #permission_classes=[permissions.IsAuthenticated]


@csrf_exempt
def staffs_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            staffsData = models.Staffs.objects.get(email=email)
        except models.Staffs.DoesNotExist:    
            staffsData = None

        if staffsData:
            if not staffsData.verify_status:
                return JsonResponse({'bool': False, 'msg': 'Account is not verified!!'})
            else:
                if staffsData.login_via_otp:
                    otp_digit = randint(100000, 999999)
                    send_mail(
                        'Verify Account',
                        'Please verify your account.',
                        'priyaeswaran321@gmail.com',
                        [email],
                        fail_silently=False,
                        html_message=f'<p>Your OTP is:</p><p>{otp_digit}</p>'
                    )

                    staffsData.otp_digit = otp_digit
                    staffsData.save()

                    return JsonResponse({'bool': True, 'staffs_id': staffsData.id, 'login_via_otp': True})
                else:
                    # Password verification using check_password
                    if check_password(password, staffsData.password):
                        return JsonResponse({'bool': True, 'staffs_id': staffsData.id, 'login_via_otp': False})
                    else:
                        return JsonResponse({'bool': False, 'msg': 'Invalid Email or Password!!'})

        else:
            return JsonResponse({'bool': False, 'msg': 'Invalid Email or Password!!'})

    else:
        return JsonResponse({'bool': False, 'msg': 'Method not allowed'})
          
@csrf_exempt
def verify_staff_via_otp(request, staff_id):
    otp_digit = request.POST.get('otp_digit')

    # Check if the provided OTP is valid for the given staff_id
    verify = models.Staffs.objects.filter(id=staff_id, otp_digit=otp_digit, verify_status=False).first()

    if verify:
        # Update verify_status to True and login_via_otp to True
        verify.verify_status = True
        verify.login_via_otp = True
        verify.save()

        return JsonResponse({'bool': True, 'staff_id': verify.id})
    else:
        return JsonResponse({'bool': False}) 

    
       
@csrf_exempt
def staff_forget_password(request):
    email=request.POST.get('email')
    verify=models.Staffs.objects.filter(email=email).first()
    if verify:
      
        link=f"http://localhost:3000/staff/change/password/{verify.id}/"
        send_mail(
                     'Verify Account',
                     'please verify your account ',
                     'priyaeswaran321@gmail.com',
                     [email],
                     fail_silently=False,
                     html_message=f'<p> Your OTP is </p><p>{link}</p>'
                 )
                  
        
        return JsonResponse({'bool':True,'msg':'Please Check Your Mail'})
    else:
        return JsonResponse({'bool':False,'msg':'Invalid Email!!'})
    



@csrf_exempt
def staff_change_password(request,staff_id):
    password=request.POST.get('password')
    verify=models.Staffs.objects.filter(id=staff_id).first()
    if verify:
        models.Staffs.objects.filter(id=staff_id).update(password=password)
        return JsonResponse({'bool':True,'msg':'Password has been changed'})
    else:
        return JsonResponse({'bool':False,'msg':'Opps....Some error occur!!'})    
    



# student register
class StudentList(generics.ListCreateAPIView):
  queryset=models.Student.objects.all()
  serializer_class=StudentSerializer
 # permission_classes=[permissions.IsAuthenticated]
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=models.Student.objects.all()
   serializer_class=StudentSerializer
   parser_classes = [MultiPartParser, FormParser]

  
@csrf_exempt
def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            studentData = models.Student.objects.get(email=email)
        except models.Student.DoesNotExist:    
            studentData = None

        if studentData:
            if not studentData.verify_status:
                return JsonResponse({'bool': False, 'msg': 'Account is not verified!!'})
            else:
                if studentData.login_via_otp:
                    otp_digit = randint(100000, 999999)
                    send_mail(
                        'Verify Account',
                        'Please verify your account.',
                        'priyaeswaran321@gmail.com',
                        [email],
                        fail_silently=False,
                        html_message=f'<p>Your OTP is:</p><p>{otp_digit}</p>'
                    )

                    studentData.otp_digit = otp_digit
                    studentData.save()

                    return JsonResponse({'bool': True, 'student_id': studentData.id, 'login_via_otp': True})
                else:
                    # Password verification using check_password
                    if check_password(password, studentData.password):
                        return JsonResponse({'bool': True, 'student_id': studentData.id, 'login_via_otp': False})
                    else:
                        return JsonResponse({'bool': False, 'msg': 'Invalid Email or Password!!'})

        else:
            return JsonResponse({'bool': False, 'msg': 'Invalid Email or Password!!'})

    else:
        return JsonResponse({'bool': False, 'msg': 'Method not allowed'})

@csrf_exempt
def verify_student_via_otp(request,student_id):
    otp_digit=request.POST.get('otp_digit')
    verify = models.Student.objects.filter(id=student_id, otp_digit=otp_digit, verify_status=False).first()
    if verify:
        verify.verify_status = True
        verify.login_via_otp = True
        verify.save()

        return JsonResponse({'bool': True, 'student_id': verify.id})
    else:
        return JsonResponse({'bool': False}) 



@csrf_exempt
def student_forget_password(request):
    email=request.POST.get('email')
    verify=models.Student.objects.filter(email=email).first()
    if verify:
      
        link=f"http://localhost:3000/student/change/password/{verify.id}/"
        send_mail(
                     'Verify Account',
                     'please verify your account ',
                     'priyaeswaran321@gmail.com',
                     [email],
                     fail_silently=False,
                     html_message=f'<p> Your OTP is </p><p>{link}</p>'
                 )
                  
        
        return JsonResponse({'bool':True,'msg':'Please Check Your Mail'})
    else:
        return JsonResponse({'bool':False,'msg':'Invalid Email!!'})
    



@csrf_exempt
def student_change_password(request,student_id):
    password=request.POST.get('password')
    verify=models.Student.objects.filter(id=student_id).first()
    if verify:
        models.Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool':True,'msg':'Password has been changed'})
    else:
        return JsonResponse({'bool':False,'msg':'Opps....Some error occur!!'})            


@csrf_exempt        
@api_view(['GET'])
def get_regulations(request):
    try:
        # Fetch unique regulations from the Course model
        regulations = Course.objects.values_list('regulation', flat=True).distinct()
        return Response({'regulations': list(regulations)})
    except Exception as e:
        return Response({'error': str(e)}, status=500)      


@csrf_exempt        
@api_view(['GET'])
def get_batch(request):
    try:

        batch = Student.objects.values_list('batch', flat=True).distinct()
        return Response({'batch': list(batch)})
    except Exception as e:
        return Response({'error': str(e)}, status=500)             
            
         
#course creation         
@csrf_exempt
@api_view(['POST'])
def create_course(request):
    if request.method == 'POST':
        try:
            code = request.data.get('code')
            course_description = request.data.get('course_description')
            course_type = request.data.get('course_type')
            category = request.data.get('category')
            regulation = request.data.get('regulation')
            academic_year = request.data.get('academic_year')
            semester = request.data.get('semester')
            course_duration = request.data.get('course_duration')
            grade_ponits = request.data.get('grade_ponits')
            created_by = request.data.get('staff_id')  # Add this line to get staff_id from the request

            # Get the staff member based on the provided staff_id
            created_by = Staffs.objects.get(id=created_by)  # Corrected from id to staff_id

            # Create a new Course object
            course = Course.objects.create(
                code=code,
                course_description=course_description,
                course_type=course_type,
                category=category,
                regulation=regulation,
                academic_year=academic_year,
                semester=semester,
                course_duration=course_duration,
                grade_ponits=grade_ponits,
                created_by=created_by,
            )

            return JsonResponse({'message': 'Course created successfully', 'course_id': course.id}, status=201)

        except Staffs.DoesNotExist:
            return JsonResponse({'error': f'Staff member not found with ID {created_by}'}, status=404)

        except Exception as e:
            return JsonResponse({'error': f'Error creating the course: {str(e)}'}, status=400)


        
 #course list       
@csrf_exempt  
@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        regulation = request.GET.get('regulation', None)

        if regulation:
            # Filter courses based on the selected regulation
            courses = Course.objects.filter(regulation=regulation)
        else:
            # Return all courses if no regulation is specified
            courses = Course.objects.all()

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
#course details
@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

#view course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer    



class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        regulation = self.request.query_params.get('regulation', None)
        semester = self.request.query_params.get('semester', None)

        queryset = Course.objects.all()

        if regulation:
            queryset = queryset.filter(regulation=regulation)
        if semester:
            queryset = queryset.filter(semester=semester)

        return queryset





#student enrollment
class EnrollmentCreate(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class StudentEnrolledCoursesAPIView(generics.ListAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
       
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student=models.Student.objects.get(pk=student_id)
            return Enrollment.objects.filter(student=student).distinct()
        
        elif 'staff_id' in self.kwargs:
            staff_id=self.kwargs['staff_id'] 
            staff=models.Staffs.objects.get(pk=staff_id) 
            return models.Enrollment.objects.filter(subject_staff=staff).distinct()
         
    
class AllEnrolledStudentsAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
        return Enrollment.objects.all()

    def get_serializer(self, *args, **kwargs):
       
        kwargs['context'] = self.get_serializer_context()
        kwargs['many'] = True
        return StudentAndCourseInfoSerializer(*args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_course_categories(request, regulation):
    try:
        # Fetch unique course categories based on the selected regulation
        categories = Course.objects.filter(regulation=regulation).values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_students_for_category(request, regulation, category,batch):
    try:
        # Fetch students enrolled for the specified course category and regulation
        students = Enrollment.objects.filter(course__regulation=regulation, course__category=category,student__batch=batch).distinct()
        serializer = StudentAndCourseInfoSerializer(students, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500) 
 
       
   
#submit grades

@csrf_exempt
@api_view(['POST'])
def submit_grades(request):
    try:
        grades_data = request.data.get('grades')  

    
        for enrollment_id, grade_data in grades_data.items():
            enrollment = Enrollment.objects.get(pk=enrollment_id)

          
            enrollment.grade = grade_data.get('grade', '')
            enrollment.pass_fail = grade_data.get('passFail', '')
            enrollment.evaluation_type = grade_data.get('evaluationType', '')

            enrollment.save()

         
            Grade.objects.create(
                student=enrollment.student,
                course=enrollment.course,
                grade=enrollment.grade,
                pass_fail=enrollment.pass_fail,
                evaluation_type=enrollment.evaluation_type
            )

        return JsonResponse({'message': 'Grades submitted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    


    #view grade
@api_view(['GET'])
def view_grades(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        grades = Grade.objects.filter(student=student)

        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

# Transcript generation endpoint
@api_view(['GET'])
def generate_transcript(request, student_id,semester=None, evaluation_type=None, download=False):
    try:
        student = Student.objects.get(pk=student_id)

        if semester is None or evaluation_type is None:
            return JsonResponse({'error': 'Semester and evaluation type are required for transcript generation.'}, status=400)

        grades = Grade.objects.filter(student=student, evaluation_type__iexact=evaluation_type, course__semester=semester)

        transcript_content = f"Transcript for {student.full_name} (Roll No: {student.rollNumber}):\n\n"

        for grade in grades:
            transcript_content += f"Course Code: {grade.course.code}\n"
            transcript_content += f"Course Title: {grade.course.category}\n"
            transcript_content += f"Grade: {grade.grade}\n"
            transcript_content += f"Pass/Fail: {grade.pass_fail}\n"
            transcript_content += f"Course Type: {grade.course.course_type}\n"
            transcript_content += f"Evaluation Type: {grade.evaluation_type}\n\n"

        # transcript_content += "--------------------------------------\n"
        # transcript_content += "Overall GPA: [Calculate GPA Here]\n"
        # transcript_content += "--------------------------------------\n"

        if download:

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.setFont("Helvetica", 12)
            text_object = p.beginText(100, 750)
            text_object.setFont("Helvetica", 12)

            for line in transcript_content.split('\n'):
                text_object.textLine(line)

            p.drawText(text_object)
            p.save()
            buffer.seek(0)

            # If it's a download, include the Content-Disposition header
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=Transcript_{semester}_{evaluation_type}.pdf'


            return response
        else:
            # If it's for viewing, return the transcript content as JSON
            return JsonResponse({'transcript_content': transcript_content})
    
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



# @method_decorator(csrf_exempt, name='dispatch')
# class TranscriptDownloadView(APIView):
#     def get(self, request, student_id, evaluation_type):
#         print(f"Received student_id: {student_id}, evaluation_type: {evaluation_type}")

#         try:
#             transcripts = Transcript.objects.filter(student__id=student_id, evaluation_type=evaluation_type)

#             if transcripts.exists():
#                 transcript = transcripts.first()

#                 # Create a BytesIO buffer to write the PDF content
#                 buffer = BytesIO()

#                 # Create a PDF object using the BytesIO buffer
#                 p = canvas.Canvas(buffer, pagesize=letter)

#                 # Set the font and size for better alignment
#                 p.setFont("Helvetica", 12)

#                 # Create a TextObject for multiline text
#                 text_object = p.beginText(100, 750)
#                 text_object.setFont("Helvetica", 12)

#                 # Add multiline text to the TextObject
#                 for line in transcript.content.split('\n'):
#                     text_object.textLine(line)

#                 # Draw the TextObject to the canvas
#                 p.drawText(text_object)

#                 # Save the PDF to the BytesIO buffer
#                 p.save()

#                 # Move the buffer's pointer to the beginning
#                 buffer.seek(0)

#                 # Create a response object with the PDF content
#                 response = HttpResponse(buffer, content_type='application/pdf')
#                 response['Content-Disposition'] = f'attachment; filename=Transcript_{evaluation_type}.pdf'

#                 return response
#             else:
#                 raise Http404("Transcript not found")
#         except Transcript.DoesNotExist:
#             raise Http404("Transcript not found")
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




           




#attendace list


class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        try:
            enrollment_id = self.request.data.get('enrollment')
            enrollment = get_object_or_404(Enrollment, pk=enrollment_id)

            start_time_str = self.request.data.get('start_time')
            end_time_str = self.request.data.get('end_time')
            date_str = self.request.data.get('date')

            # Ensure that start_time, end_time, and date are properly formatted
            start_time = parse_datetime(f'2000-01-01T{start_time_str}')
            end_time = parse_datetime(f'2000-01-01T{end_time_str}')
            date = parse_datetime(date_str).date()

            serializer.save(enrollment=enrollment, start_time=start_time, end_time=end_time, date=date)

            return Response({'success': 'Attendance submitted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f'Error in perform_create: {e}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def submit_attendance(request):
    try:
        attendance_data = request.data.get('attendance', {})

        for enrollment_id, attendance_info in attendance_data.items():
            try:
                enrollment_id = int(enrollment_id)
                enrollment = Enrollment.objects.get(id=enrollment_id)
            except (ValueError, Enrollment.DoesNotExist):
                return Response({'error': f'Enrollment with id {enrollment_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AttendanceSerializer(data=attendance_info)
            if serializer.is_valid():
                serializer.save(enrollment=enrollment)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Attendance submitted successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
     print(f'Error in perform_create: {e}')
     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_student_attendance(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        student_enrollments = Enrollment.objects.filter(student=student)
        all_attendance = []

        for enrollment in student_enrollments:
            enrollment_attendance = Attendance.objects.filter(enrollment=enrollment)
            all_attendance.extend(enrollment_attendance)

        serializer = AttendanceSerializer(all_attendance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



 
 
   
    




  
    
#announcement

@csrf_exempt
@api_view(['POST'])
def create_announcement(request):
    serializer = AnnouncementSerializer(data=request.data)
    
    if serializer.is_valid():
        announcement = serializer.save()

        target = request.data.get('target')

        if target == 'staff':
            staffs = Staffs.objects.all()
            notifications = [StaffNotification(staff=staff, announcement=announcement, message=announcement.message) for staff in staffs]
            StaffNotification.objects.bulk_create(notifications)

        elif target == 'student':
            students = Student.objects.all()
            notifications = [StudentNotification(student=student, announcement=announcement, message=announcement.message) for student in students]
            StudentNotification.objects.bulk_create(notifications)


        elif target == 'both':
            staffs = Staffs.objects.all()
            students = Student.objects.all()
            staff_notifications = [StaffNotification(staff=staff, announcement=announcement, message=announcement.message) for staff in staffs]
            student_notifications = [StudentNotification(student=student, announcement=announcement, message=announcement.message) for student in students]
            StaffNotification.objects.bulk_create(staff_notifications)
            StudentNotification.objects.bulk_create(student_notifications)

        return Response({'status': 'Announcement created successfully.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#staffnotification    
@csrf_exempt
@api_view(['GET'])
def get_staff_notifications(request, staff_id):
    notifications = StaffNotification.objects.filter(staff_id=staff_id)
    serializer = StaffNotificationSerializer(notifications, many=True)
    return Response(serializer.data)



@csrf_exempt
@api_view(['GET'])
def get_student_notifications(request, student_id):
    notifications = StudentNotification.objects.filter(student_id=student_id)
    serializer = StudentNotificationSerializer(notifications, many=True)
    return Response(serializer.data)







#fees payment

stripe.api_key = 'sk_test_51OCxr9SCNzugdY3nFtZkMSlmlHeupgjKO9FcYcFTjubgzzYld9BcfLSXXvEXu1aSnXPNUujKTuRftJDZBf8D5eLG00d7ATL6Eu'
class StripeCheckoutView(APIView):
    def post(self, request): 
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                       
                        'price': 'price_1OCyjTSCNzugdY3nxKUUcoRS',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
         
            print(f"Stripe Error: {e}")
            return Response(
                {'error': 'Something went wrong with Stripe'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
  
            print(f"Unexpected Error: {e}")
            return Response(
                {'error': 'Something unexpected went wrong'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
stripe.api_key = "sk_test_51OCxr9SCNzugdY3nFtZkMSlmlHeupgjKO9FcYcFTjubgzzYld9BcfLSXXvEXu1aSnXPNUujKTuRftJDZBf8D5eLG00d7ATL6Eu"
endpoint_secret = "whsec_gzjeatVMhUeVFO8DqJN8LZacJZhZCxMh"

@csrf_exempt
def handle_payment_success(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        sig_header = request.headers.get('stripe-signature', '')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] in ['customer.created', 'customer.deleted', 'customer.updated',
                             'price.created', 'price.deleted', 'price.updated', 'invoice.paid']:
            # Custom logic for handling specific events
            print(f"Received event of type: {event['type']}")
            
            # Perform actions based on the event type

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests


#admission list

class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class ApplicantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def perform_update(self, serializer):
        instance = serializer.save(status='accepted')
        student_id = self.request.data.get('student_id')

        if student_id:
            try:
                student = Student.objects.get(pk=student_id)
                instance.student = student
                instance.save()
                student.admission_status = True
                student.save()
                return Response({'message': 'Admission status updated successfully'})
            except Student.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Student ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        

@api_view(['POST'])
def update_admission_status(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.admission_status = True
        student.save()

        # Update all associated applicants' status to 'accepted'
        applicants = Applicant.objects.filter(student=student)
        applicants.update(status='accepted')

        return Response({'message': 'Admission status updated successfully'})
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Applicant.DoesNotExist:
        return Response({'error': 'No applicants found for the student'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    
@csrf_exempt
@api_view(['GET'])
def get_admission_status(request):
    try:
        student_id = request.GET.get('student_id')
        student = Student.objects.get(id=student_id)
        admission_status = 'admitted' if student.admission_status else 'not_admitted'
        return JsonResponse({'admission_status': admission_status})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt  
@require_POST
def send_message(request, student_id):
    try:
       
        student = Applicant.objects.get(id=student_id)
        message = request.POST.get('message', '')
        student.message = message
        student.save()
        return JsonResponse({'success': True})
    except Applicant.DoesNotExist:
         return JsonResponse({'success': False, 'error': 'Applicant not found'})
    
class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =models.Document.objects.all()
    serializer_class = DocumentSerializer   


class DocumentListForStudent(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Document.objects.filter(student_id=student_id)
    

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        serializer.save(student_id=student_id)
    


    

#ducuments
@csrf_exempt
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    response = FileResponse(document.file)
    response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'

    return response



#messase student staff
@csrf_exempt
def save_staff_student_msg(request,staff_id,student_id):
   
        staff=models.Staffs.objects.get(id=staff_id) 
        student=models.Student.objects.get(id=student_id) 
        msg_text = request.POST.get('msg_text')  
        msg_from = request.POST.get('msg_from')    
        msgRes=models.StaffStudentChat.objects.create(
            staff=staff,
            student=student,
            msg_text=msg_text,
            msg_from=msg_from,

        )
        if msgRes:
           return JsonResponse({'bool':True,'msg':'Message has been send'})
        else:
           return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})   


class MessageList(generics.ListAPIView):
    queryset = models.StaffStudentChat.objects.all()
    serializer_class = StaffStudentChatSerializer
    def get_queryset(self):
        staff_id=self.kwargs['staff_id']
        student_id=self.kwargs['student_id']
        staff = Staffs.objects.get(pk=staff_id)
        student = Student.objects.get(pk=student_id)
        return models.StaffStudentChat.objects.filter(staff=staff,student=student).exclude(msg_text='')
    



@csrf_exempt
def save_staff_student_group_msg(request, staff_id):
    staff = Staffs.objects.get(id=staff_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')
    enrolledList=models.Enrollment.objects.filter(course__created_by=staff).distinct()
    msgRes = None
    for enrolled in  enrolledList:
        msgRes = models.StaffStudentChat.objects.create(
            staff=staff,
            student=enrolled.student,
            msg_text=msg_text,
            msg_from=msg_from,
        )

    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been sent'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occurred!!'})
    



@csrf_exempt
def save_staff_student_group_msg_from_student(request, student_id):
    student = Student.objects.get(id=student_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')
    courseList=models.Course.objects.filter(enrollments__student=student).distinct()
    msgRes = None
    for course in  courseList:
        msgRes = models.StaffStudentChat.objects.create(
            staff=course.created_by,
            student=student,
            msg_text=msg_text,
            msg_from=msg_from,
        )

    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been sent'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occurred!!'})    


#adminmessage


@csrf_exempt
def save_admin_msg(request, staff_id, user_id):
    try:
        staff = Staffs.objects.get(id=staff_id)
        user = User.objects.get(id=user_id)

        msg_text = request.POST.get('msg_text')
        msg_from = request.POST.get('msg_from')

        msgRes =  models.StaffStudentChat.objects.create(
            staff=staff,
            user=user,
            msg_text=msg_text,
            msg_from=msg_from,
        )

        if msgRes:
            return JsonResponse({'bool': True, 'msg': 'Message has been sent'})
        else:
            return JsonResponse({'bool': False, 'msg': 'Oops... Some error occurred!!'})

    except ObjectDoesNotExist:
        return JsonResponse({'bool': False, 'msg': 'Invalid staff or user ID'}) 


class AdminStaffMessageList(generics.ListAPIView):
    queryset = models.StaffStudentChat.objects.all()
    serializer_class = StaffStudentChatSerializer
    def get_queryset(self):
        staff_id=self.kwargs['staff_id']
        user_id=self.kwargs['user_id']
        staff = Staffs.objects.get(pk=staff_id)
        user = User.objects.get(pk=user_id)
        return models.StaffStudentChat.objects.filter(staff=staff,user=user).exclude(msg_text='')
    


@csrf_exempt
def save_admin_student_msg(request,student_id,user_id):
   
        student=models.Student.objects.get(id=student_id) 
        user=models.User.objects.get(id=user_id) 

        msg_text = request.POST.get('msg_text')  
        msg_from = request.POST.get('msg_from')    
        
        msgRes=models.StaffStudentChat.objects.create(
            student=student,
            user=user,
            msg_text=msg_text,
            msg_from=msg_from,

        )
        if msgRes:
           return JsonResponse({'bool':True,'msg':'Message has been send'})
        else:
           return JsonResponse({'bool':False,'msg':'Oops... Some Error Occured!!'})   


class AdminStudentMessageList(generics.ListAPIView):
    queryset = models.StaffStudentChat.objects.all()
    serializer_class = StaffStudentChatSerializer
    def get_queryset(self):
        student_id=self.kwargs['student_id']
        user_id=self.kwargs['user_id']
        student = Student.objects.get(pk=student_id)
        user = User.objects.get(pk=user_id)
        return models.StaffStudentChat.objects.filter(student=student,user=user).exclude(msg_text='')    
    



 #admin details   
class UserList(generics.ListCreateAPIView):
  queryset=models.User.objects.all()
  serializer_class=UserSerializer


class FeesListCreateView(generics.ListCreateAPIView):
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer

    def perform_create(self, serializer):
        # Set the student for the fees based on your authentication logic
        student = get_object_or_404(Student, user=self.request.user)
        serializer.save(student=student)


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class FeesInformationView(generics.RetrieveAPIView):
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer

    def get(self, request, *args, **kwargs):
        try:
            fees_instance = Fees.objects.latest('id')
            serializer = self.get_serializer(fees_instance)
            return Response(serializer.data)
        except Fees.DoesNotExist:
            return Response({'error': 'No fees information available'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def set_fees(request):
    if request.method == 'POST':
        try:
            # Extract the amount from the request data
            amount = float(request.POST.get('amount', 0))

            # Set the fees in your database or any other storage mechanism.
            # In this example, I'm creating a new Fees instance.
            # You may want to update the existing instance or handle it differently based on your logic.

            # Replace the following line with your logic to set the fees in the database
            Fees.objects.create(amount=amount, student=None)

            return JsonResponse({'message': 'Fees set successfully'})
        except ValueError:
            return JsonResponse({'error': 'Invalid amount format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_fees(request):
    try:
        fees_instance = Fees.objects.latest('id')
        fees_amount = fees_instance.amount if fees_instance else 0
        return JsonResponse({'amount': fees_amount})
    except Fees.DoesNotExist:
        return JsonResponse({'error': 'No fees information available'}, status=404)
    

class OverallReportView(generics.RetrieveAPIView):
    serializer_class = OverallReportSerializer

    def get(self, request, *args, **kwargs):
        # Fetch data for each model
        applicant_data = Applicant.objects.all()
        applicant_serializer = ApplicantSerializer(applicant_data, many=True)

        attendance_data = Attendance.objects.all()
        attendance_serializer = AttendanceSerializer(attendance_data, many=True)

        grades_data = Grade.objects.all()
        grades_serializer = GradeSerializer(grades_data, many=True)

        enrollment_data = Enrollment.objects.all()
        enrollment_serializer = EnrollmentSerializer(enrollment_data, many=True)

        # Calculate percentages for each model
        applicant_percentage = calculate_applicant_percentage(applicant_data)
        attendance_percentage = calculate_attendance_percentage(attendance_data)
        grades_percentage = calculate_grades_percentage(grades_data)
        enrollment_percentage = calculate_enrollment_percentage(enrollment_data)

        # Combine data for overall report
        overall_report_data = {
            'applicants': applicant_serializer.data,
            'attendance': attendance_serializer.data,
            'grades': grades_serializer.data,
            'enrollments': enrollment_serializer.data,
            'applicant_percentage': applicant_percentage,
            'attendance_percentage': attendance_percentage,
            'grades_percentage': grades_percentage,
            'enrollment_percentage': enrollment_percentage,
        }

        serializer = self.get_serializer(overall_report_data)
        return Response(serializer.data)

@csrf_exempt
def calculate_applicant_percentage(applicant_data):
    # Your logic to calculate applicant percentage
    # Example: Calculate the percentage of approved applicants

    total_applicants = applicant_data.count()

    # Fetch the total number of students
    total_students = Student.objects.count()

    if total_applicants == 0 or total_students == 0:
        return 0.0

    approved_count = applicant_data.filter(status='approved').count()
    
    # Your logic to calculate applicant percentage
    # Example: Calculate the percentage of approved applicants out of total students
    applicant_percentage = (approved_count / total_students) * 100.0

    return round(applicant_percentage, 2)

@csrf_exempt
def calculate_attendance_percentage(attendance_data):
    # Your logic to calculate attendance percentage
    # Example: Calculate the average attendance percentage
    total_attendance = attendance_data.count()
    if total_attendance == 0:
        return 0.0

    present_count = attendance_data.filter(attendance='P').count()
    attendance_percentage = (present_count / total_attendance) * 100.0
    return round(attendance_percentage, 2)

@csrf_exempt
def calculate_grades_percentage(grades_data):
    # Your logic to calculate grades percentage
    # Example: Calculate the average grade percentage
    total_grades = grades_data.count()
    if total_grades == 0:
        return 0.0

    excellent_count = grades_data.filter(grade='Pass').count()
    grades_percentage = (excellent_count / total_grades) * 100.0
    return round(grades_percentage, 2)


@csrf_exempt
def calculate_enrollment_percentage(enrollment_data):
    total_enrollments = enrollment_data.count()
    
    # Fetch the total number of students
    total_students = Student.objects.count()

    if total_enrollments == 0 or total_students == 0:
        return 0.0

    # Replace 'some_field' with an actual field in the Enrollment model
    completed_count = enrollment_data.filter(course__category='enrolled').count()

    # Your logic to calculate enrollment percentage
    # Example: Calculate the percentage of completed enrollments out of total students
    enrollment_percentage = (completed_count / total_students) * 100.0

    return round(enrollment_percentage, 2)






















