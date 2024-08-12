from APP import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="homepage"),
    path('student_login/', views.student_login, name="student_loginpage"),
    path('staff_login/', views.staff_login, name="staff_loginpage"),
    path('admin_login/', views.admin_login, name="admin_loginpage"),
    path('student_dashboard/', views.student_dashboard, name="student_dashboard"),
    path('staff_dashboard/', views.staff_dashboard, name="staff_dashboard"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('add_student/', views.add_student, name="add_student"),
    path('add_faculty/', views.add_faculty, name="add_faculty"),
    path('delete_student/', views.delete_student, name="delete_student"),
    path('delete_faculty/', views.delete_faculty, name="delete_faculty"),
    path('scan_face/', views.scan_face, name="scan_face"),
    path('detectface/', views.detectface, name="detectface"),
    path('view_attendence/', views.view_attendence, name="view_attendence"),
    path('student_view_attendence/', views.student_view_attendence, name="student_view_attendence"),
    path('generate_attendence_report/', views.generate_attendance_report, name="generate_attendence_report"),
    path('staff_generate_attendence/', views.staff_generate_attendence, name="staff_generate_attendence"),
    path('profile/', views.profile, name="profile"),
    path('staff_profile/', views.staff_profile, name="staff_profile"),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)