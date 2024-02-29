from django.urls import path,include
from .import views
from django.views.decorators.http import require_POST
from rest_framework.routers import DefaultRouter
   
from .views import CourseListCreateView, CourseRetrieveUpdateDestroyView,CourseList, EnrollmentCreate,StudentEnrolledCoursesAPIView,AllEnrolledStudentsAPIView,submit_attendance,submit_grades,view_grades, generate_transcript,AttendanceListCreateView,get_student_attendance,LoginView,create_announcement,get_staff_notifications,get_student_notifications
from .views import StripeCheckoutView,StudentList,StaffsList,ApplicantListCreateView,ApplicantDetailView,send_message,DocumentListCreateView,DocumentDetailView,download_document,get_admission_status,update_admission_status,UserList,FeesListCreateView,PaymentListCreateView,FeesInformationView,set_fees,get_fees,handle_payment_success




urlpatterns = [
    
    path('create-checkout-session', StripeCheckoutView.as_view()),
    path('payment/success/', handle_payment_success, name='handle_payment_success'),
    path('staffs-register/', views.StaffsList.as_view()),
    path('verify/staff/<int:staff_id>/', views.verify_staff_via_otp),
    path('staff/forget/password/', views.staff_forget_password),
    path('staff/change/password/<int:staff_id>/', views.staff_change_password),
  
    
    path('staffs/<int:pk>/', views.StaffsDetail.as_view()),
    path('staffs-login/', views.staffs_login),
    path('verify/student/<int:student_id>/', views.verify_student_via_otp),
     path('student/forget/password/', views.student_forget_password),
    path('student/change/password/<int:student_id>/', views.student_change_password),
    #path('category', views.CategoryList.as_view()), 
    # path('student/profile/<int:pk>/', views.StudentDetail.as_view()),
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('student-login/', views.student_login),

    path('course-creation/', views.create_course, name='create_course'),
    path('courses/', views.course_list),
    path('courses/up/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-retrieve-update-destroy'),
    path('course/', CourseList.as_view(), name='course-list'),
    path('regulations/', views.get_regulations, name='get_regulations'),
    path('batch/', views.get_batch, name='get_batch'),


    path('enrollments/', EnrollmentCreate.as_view(), name='enrollment-create'),
    path('enrollment/list/<int:student_id>/', StudentEnrolledCoursesAPIView.as_view(), name='student-enrolled-courses'),
    path('enrolled/students/list/', AllEnrolledStudentsAPIView.as_view(), name='all-enrolled-students'),
    path('course/categories/<str:regulation>/',views. get_course_categories, name='get_course_categories'),
    path('student/category/<str:regulation>/<str:category>/<str:batch>/', views.get_students_for_category, name='get_students_for_category'),

    path('submit/grades/', submit_grades, name='submit_grades'),
    path('students/grades/<int:student_id>/', view_grades, name='view_grades'),

    # path('students/transcript/<int:student_id>/', generate_transcript, name='generate_transcript'),
   # Assuming you have a semester parameter as an integer
    path('students/transcript/<int:student_id>/<int:semester>/<str:evaluation_type>/download/', generate_transcript, {'download': True}, name='generate_transcript_with_semester_evaluation_type_download'),
    path('students/transcript/<int:student_id>/<int:semester>/<str:evaluation_type>/', generate_transcript, name='generate_transcript_with_semester_evaluation_type'),

    # path('students/download/transcript/<int:student_id>/<str:evaluation_type>/', TranscriptDownloadView.as_view(), name='transcript_download'),


    path('submit/attendance/', submit_attendance, name='submit_attendance'),
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('student/attendance/<int:student_id>/', get_student_attendance, name='get_student_attendance'),



    path('login/', LoginView.as_view(), name='login'),

    path('create/announcement/', create_announcement, name='create_announcement'),

    path('staff/notifications/<int:staff_id>/', get_staff_notifications, name='get_staff_notifications'),
    path('student/notifications/<int:student_id>/', get_student_notifications, name='get_student_notifications'),

   
  
    path('applicants/', ApplicantListCreateView.as_view(), name='applicant-list-create'),
    path('applicants/<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    path('student/admission/status/', get_admission_status, name='admission-status'),
    path('update/admission/status/<int:student_id>/', update_admission_status, name='update_admission_status'),


    path('send/message/<int:student_id>/', send_message, name='send_message'),
    
    path('documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:pk>/download/', download_document, name='download_document'),
    path('student/<int:student_id>/documents/', views.DocumentListForStudent.as_view(), name='document-list-for-student'),
    
  

    path('list/students/', StudentList.as_view(), name='student-list'),
    path('list/staffs/', StaffsList.as_view(), name='staffs-list'),
    path('user/', UserList.as_view(), name='user-list'),
    #student staff
    path('student/send/message/<int:staff_id>/<int:student_id>/', views.save_staff_student_msg),
    path('get/message/<int:staff_id>/<int:student_id>/', views.MessageList().as_view()),
   #admin staff
    path('staff/admin/send/message/<int:staff_id>/<int:user_id>/', views.save_admin_msg),
    path('get/admin/staff/message/<int:staff_id>/<int:user_id>/', views.AdminStaffMessageList().as_view()),
   #admin student
    path('student/admin/send/message/<int:student_id>/<int:user_id>/', views.save_admin_student_msg),
    path('get/admin/student/message/<int:student_id>/<int:user_id>/', views.AdminStudentMessageList().as_view()),


    path('send/group/message/<int:staff_id>/', views.save_staff_student_group_msg),
    path('send/group/message/student/<int:student_id>/', views.save_staff_student_group_msg_from_student),

    path('fees/', FeesListCreateView.as_view(), name='fees-list-create'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),  
    path('fees/payments/',FeesInformationView.as_view(), name='latest-fees-information'), 

    path('set/fees/', set_fees, name='set-fees'),
    path('get/fees/', get_fees, name='get-fees'),

    path('overall/report/', views.OverallReportView.as_view(), name='overall-report'),
    path('academic/years/', views.academic_years, name='academic_years'),

    path('faq/',views.FaqListCreateAPIView.as_view(), name='FaqListCreateAPIView-create'),


    path('contact/', views.ContactList.as_view()),



]






    #path('enroll/', include(router.urls)),
    

   

   


