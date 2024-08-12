from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from APP.models import admin_tables, faculty,students
import os
import face_recognition
import cv2,csv
import numpy as np
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle


# Create your views here.
def home(request):
    return render(request, 'APP/home.html')

# def student_login(request):
#     if request.method == 'POST':
#        stuid = request.POST['username']
#        password = request.POST['password']

#        user = students.objects.get(student_id=stuid)
#        passw = str(user.DOB)
#        print(user, passw)
#        if user.DOB == passw:
#            return render(request, 'APP/student_dashboard.html')
       
#     return render(request, 'APP/student_login.html')


def student_login(request):
    if request.method == 'POST':
        stuid = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = students.objects.get(name=stuid)
        except students.DoesNotExist:
            messages.error(request, 'Invalid student ID or password.')
            return redirect('student_loginpage')

        # Assuming DOB is the password field, compare it with the provided password
        if user.student_id == password:
            messages.success(request, 'Login successful')

            # Write login details to CSV file
            csv_file_path = os.path.join(os.path.dirname(__file__), 'profile.csv')
            with open(csv_file_path, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([user.name, user.student_id,user.DOB,user.gender,user.standard])

            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid student ID or password.')
            return redirect('student_loginpage')
    
    return render(request, 'APP/student_login.html')



def profile(request):
    
    csv_file_path = os.path.join(os.path.dirname(__file__), 'profile.csv')

    # Initialize a list to store attendance records
    profile_record = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            profile_record.append(row)
            print(profile_record)

    # Pass the attendance_records list to the template for rendering
    return render(request, 'APP/profile.html', {'profile_record': profile_record})


def staff_login(request):
    if request.method == 'POST':
        stuid = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = faculty.objects.get(name=stuid)
        except faculty.DoesNotExist:
            messages.error(request, 'Invalid Faculty ID or password.')
            return redirect('staff_loginpage')

        # Assuming DOB is the password field, compare it with the provided password
        print(user.faculty_id)
        if user.faculty_id == password:
            csv_file_path = os.path.join(os.path.dirname(__file__), 'staff_profile.csv')
            with open(csv_file_path, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([user.name, user.faculty_id,user.DOB,user.gender,user.qualification,user.address])
            messages.error(request, 'Login successful')
            return render(request, 'APP/staff_dashboard.html')
        else:
            messages.error(request, 'Invalid student ID or password.')
            return redirect('staff_loginpage')
    
    return render(request, 'APP/staff_login.html')

def staff_profile(request):
    
    csv_file_path = os.path.join(os.path.dirname(__file__), 'staff_profile.csv')

    # Initialize a list to store attendance records
    profile_records = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            profile_records.append(row)
            print(profile_records)

    # Pass the attendance_records list to the template for rendering
    return render(request, 'APP/staff_profile.html', {'profile_records': profile_records})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = admin_tables.objects.get(username=username)

        if user.password == password:
            print('logged in')
            return redirect('admin_dashboard')
        
        else:

            return render(request, 'APP/admin_login.html')
    print("else block")
    return render(request, 'APP/admin_login.html')


def student_dashboard(request):

    return render(request, 'APP/student_dashboard.html')

def staff_dashboard(request):
    return render(request, 'APP/staff_dashboard.html')

def admin_dashboard(request):
    return render(request, 'APP/admin_dashboard.html')


def add_student(request):
    if request.method == 'POST':
        stuid = request.POST['Id']
        name = request.POST['name']
        DOB = request.POST['dob']
        gender = request.POST['gender']
        standard = request.POST['standard']
        address = request.POST['address']
        image = request.FILES['image']
        
        faces_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Faces')
        print(faces_folder_path)
        # Save the image to the 'Faces' folder
        fs = FileSystemStorage(location= faces_folder_path)  # Specify the absolute path to the 'Faces' folder
        filename = fs.save(image.name, image)

        # Save the user details to the database
        user = students(student_id=stuid,name=name,  DOB=DOB, gender=gender, standard=standard, Address=address, image=filename)
        user.save()
        
        return render(request, 'APP/admin_dashboard.html')  # Redirect to a success page
    else:
        return render(request, 'APP/add_student.html') 


def delete_student(request):
    if request.method == 'POST':
        stuid = request.POST.get('Id')
        name = request.POST.get('name')
        print("Post")
        user = get_object_or_404(students, student_id=stuid)
        
        print("user")
        image_filename = user.image.name
        print(image_filename)
        faces_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Faces')
        image_path = os.path.join(faces_folder_path, image_filename)
        if os.path.exists(image_path):
            print("removed")
            os.remove(image_path)


        
        user.delete()
        print("Deleted")

        return render(request, 'APP/admin_dashboard.html')  
    else:
        return render(request, 'APP/delete_student.html')


def scan_face(request):
    users = students.objects.all()
    # for user in users:
    #     print(user)
    # Function to get images from a folder
    def get_images_from_folder(folder_path):
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                images.append(os.path.join(folder_path, filename))
        return images

    # Path to the "Faces" folder
    images_folder = os.path.join(os.path.dirname(__file__), 'Faces')

    # Get images from the "Faces" folder
    known_faces = []
    known_face_encodings = []
    for filename in os.listdir(images_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            image_path = os.path.join(images_folder, filename)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_faces.append(filename)
            known_face_encodings.append(face_encoding)


    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return HttpResponse("Unable to open camera")

    ret, frame = cap.read()

    # Convert frame to RGB for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    face_locations = face_recognition.face_locations(rgb_frame)

    # Open CSV file to store attendance
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Perform face recognition
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_encodings = face_recognition.face_encodings(rgb_frame, [face_location])
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                if True in matches:
                    # Face recognized, write attendance record to CSV
                    matched_index = matches.index(True)
                    matched_face_name = known_faces[matched_index]
                    print(matched_face_name)
                    #print(user.image.name)
                    for user in users:
                        print(user)
                        if user.image.name == matched_face_name:
                            #attendence_status="Present"
                            csv_writer.writerow([user.student_id, user.name, "Present"])
                    print("Attendance recorded for:", matched_face_name)
                    cap.release()
                    return HttpResponse("Attendance Captured")
                else:
                    # Face not recognized, deny access
                    cap.release()
                    return HttpResponse("Face not matched")

    # No face detected
    cap.release()
    return HttpResponse("<h1>No Face Detected<h1>")



def view_attendence(request):
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')

    # Initialize a list to store attendance records
    attendance_records = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            attendance_records.append(row)
            print(attendance_records)

    # Pass the attendance_records list to the template for rendering
    return render(request, 'APP/view_attendence.html', {'attendance_records': attendance_records})

def student_view_attendence(request):
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')

    # Initialize a list to store attendance records
    attendance_record = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            attendance_record.append(row)
            print(attendance_record)

    # Pass the attendance_records list to the template for rendering
    return render(request, 'APP/student_view_attendence.html', {'attendance_record': attendance_record})



def generate_attendance_report(request):
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')

    # Initialize a list to store attendance records
    attendance_records = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            attendance_records.append(row)

    # Create a PDF buffer
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response, pagesize=letter)

    # Define table data
    data = [['Student ID', 'Student Name', 'Attendance Status']]
    data.extend(attendance_records)

    # Create table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table object
    t = Table(data)

    # Apply style to table
    t.setStyle(style)

    # Draw table on the PDF
    width, height = letter
    t.wrapOn(p, width, height)
    t.drawOn(p, 30, 750)

    # Close the PDF object
    p.showPage()
    p.save()

    return response

def staff_generate_attendence(request):
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')

    # Initialize a list to store attendance records
    attendance_recording = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader, None)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the attendance_records list
            attendance_recording.append(row)

    # Create a PDF buffer
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response, pagesize=letter)

    # Define table data
    data = [['Student ID', 'Student Name', 'Attendance Status']]
    data.extend(attendance_recording)

    # Create table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table object
    t = Table(data)

    # Apply style to table
    t.setStyle(style)

    # Draw table on the PDF
    width, height = letter
    t.wrapOn(p, width, height)
    t.drawOn(p, 30, 750)

    # Close the PDF object
    p.showPage()
    p.save()

    return response



'''def scan_face(request):
    images_folder = os.path.join(os.path.dirname(__file__), 'Faces')

    # Load known faces and their encodings
    known_faces = []
    known_face_encodings = []

    for filename in os.listdir(images_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(images_folder, filename)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_faces.append(filename)
            known_face_encodings.append(face_encoding)

    # Open CSV file to store attendance
    csv_file_path = os.path.join(os.path.dirname(__file__), 'attendance.csv')
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Capture video from camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera.")
            return HttpResponse("Unable to open camera")

        ret, frame = cap.read()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_encodings = face_recognition.face_encodings(rgb_frame, [face_location])

            for face_encoding in face_encodings:
                # Compare face encoding with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                
                if True in matches:
                    # Face recognized, store attendance
                    # Get the student ID and name from the known_faces list
                    student_index = matches.index(True)
                    student_name = known_faces[student_index]
                    # Store student attendance in CSV file
                    csv_writer.writerow([student_name, "Present"])
                    # Redirect to a success page or route
                    return redirect('detectface')
                else:
                    # Face not recognized
                    return redirect('#')

        # No face detected
        return HttpResponse("<h1>No Face Detected</h1>")
        
        cap.release()

        return HttpResponse("<h1>Attendance Recorded Successfully</h1>")'''


def detectface(request):
    return render(request, 'APP/detectface.html')


def add_faculty(request):
    if request.method == 'POST':
        facultyid = request.POST['Id']
        name = request.POST['name']
        DOB = request.POST['dob']
        gender = request.POST['gender']
        qualification = request.POST['qualification']
        address = request.POST['address']

        user = faculty(faculty_id=facultyid, name=name,  DOB=DOB, gender=gender, qualification=qualification, address=address)

        user.save()

        return render(request, 'APP/admin_dashboard.html')
    
    return render(request, 'APP/add_faculty.html')


def delete_faculty(request):
    if request.method == 'POST':
        if request.method == 'POST':
            facid = request.POST.get('Id')
            name = request.POST.get('name')
            print("Post")
            user = get_object_or_404(faculty, faculty_id=facid)
            
            print("user")
            user.delete()
            print("Deleted")

            return render(request, 'APP/admin_dashboard.html')  
    else:
        return render(request, 'APP/delete_faculty.html')


   
