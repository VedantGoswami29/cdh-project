from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

################## Student ################
class StudentViews:
    @login_required    
    def addStudent(request):
        if not request.user.is_superuser:
            messages.info(request, 'You Are Not Allowed To Access This Web Page')
            return redirect('/')
        if request.method == "POST":

            roll_number = request.POST.get('roll_number').upper()

            if Student.objects.filter(roll_number=roll_number):
                messages.error(request, f"Student With Roll Number '{roll_number}' Already Exists")
                return redirect('/student/add')
            

            first_name = request.POST.get('first_name').upper()
            last_name = request.POST.get('last_name').upper()
            photo = request.FILES.get('photo')
            group = request.POST.get('group')
            standard = request.POST.get('standard')
            start_year = request.POST.get('start_year')
            student_type = request.POST.get('student_type')
            birth_date = request.POST.get('birth_date')
            student_mobile_number = request.POST.get('student_mobile_number') if request.POST.get('student_mobile_number') else 'Number was not given'
            parrent_mobile_number = request.POST.get('parrent_mobile_number')
            discussed_fee = request.POST.get('discussed_fee')
            remaining_fees = discussed_fee
            status = request.POST.get('status')


            std = Student.objects.create(
                roll_number=roll_number,
                first_name = first_name,
                last_name = last_name,
                photo = photo,
                group = group,
                standard = standard,
                start_year = start_year,
                student_type = student_type,
                birth_date = birth_date,
                student_mobile_number = student_mobile_number,
                parrent_mobile_number = parrent_mobile_number,
                discussed_fee = discussed_fee,
                remaining_fees = remaining_fees,
                status = status
            )
            std.save()
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
            user = User.objects.create_user(username=roll_number, password=f"{std.first_name}@{birth_date_obj.day}{birth_date_obj.month}{std.last_name}")
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, f"{first_name} {last_name}'s Data Is Added To The Database")
            return redirect('/')

        return render(request, 'student/add.html')

    @login_required
    def editStudent(request):
        if not request.user.is_superuser:
            messages.info(request, 'You Are Not Allowed To Access This Web Page')
        if request.method == "POST":
            roll_number = request.POST.get('roll_number').upper()
            std = Student.objects.get(roll_number=roll_number)

            first_name = request.POST.get('first_name').upper()
            last_name = request.POST.get('last_name').upper()
            group = request.POST.get('group')
            standard = request.POST.get('standard')
            start_year = request.POST.get('start_year')
            student_type = request.POST.get('student_type')
            birth_date = request.POST.get('birth_date')
            student_mobile_number = request.POST.get('student_mobile_number', None)
            parrent_mobile_number = request.POST.get('parrent_mobile_number', None)
            discussed_fee = request.POST.get('discussed_fee')
            remaining_fees = discussed_fee
            status = request.POST.get('status')

            std.first_name = first_name
            std.last_name = last_name
            std.group = group
            std.standard = standard
            std.start_year = start_year
            std.student_type = student_type
            std.birth_date = birth_date
            std.student_mobile_number = student_mobile_number
            std.parrent_mobile_number = parrent_mobile_number
            std.discussed_fee = discussed_fee
            std.remaining_fees = remaining_fees
            std.status = status
            if request.FILES:
                os.remove(std.photo.url[1:])
                std.photo = request.FILES.get('photo')

            std.save()
            
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
            user = User.objects.get(username=roll_number)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(f"{std.first_name}@{birth_date_obj.day}{birth_date_obj.month}{std.last_name}")
            user.save()
            

            messages.success(request, f"{first_name} {last_name}'s Data Is Edited To The Database")
            return redirect('/')

        return render(request, 'student/edit.html')

    @login_required
    def getStudent(request):
        if not request.user.is_superuser:
            roll_number = request.user.username
            student = Student.objects.filter(roll_number=roll_number).first()
            return render(request, 'student/info.html', {"student": student})
        
        roll_number = request.GET.get('roll_number')

        if roll_number is not None:
            student = Student.objects.filter(roll_number=roll_number.upper())
            if not student:
                return HttpResponse(f'No Student Data Found For Roll Number {roll_number}', status=404)
            return JsonResponse({'student': list(student.values())[0]})
        else:
            return render(request, 'student/get.html')

    @login_required
    def bulkEditStudents(request):
        if not request.user.is_superuser:
            messages.info(request, 'You Are Not Allowed To Access This Web Page')
            return redirect('/')
        if request.method == "POST":
            start_year = request.POST.get('start_year')
            standard = request.POST.get('standard')
            status = request.POST.get('status')
            students = Student.objects.filter(start_year=start_year)
            for student in students:
                student.standard = standard if standard else student.standard
                student.status = status if status!="No Change" else student.status
                student.save()
            messages.success(request, f'Student with start year {start_year} edited successfully')
            return redirect('/')
        return render(request, 'student/bulkEdit.html')

    @login_required
    def delStudent(request):
        if not request.user.is_superuser:
            messages.info(request, 'You Are Not Allowed To Access This Web Page')
            return redirect('/')
        

        if request.method == "POST":
            roll_number = request.POST.get('roll_number').upper()
            student = Student.objects.filter(roll_number=roll_number)
            user = User.objects.filter(username=roll_number)
            if not student:
                messages.warning(request, f"Student With Roll Number '{roll_number}' Doesn't Exist")
                return redirect('/student/delete')
            student_photo = student.first().photo.url[1:]
            user.delete()
            if os.path.isfile(student_photo):
                os.remove(student_photo)
                student.delete()
                messages.info(request, f"Student With Roll Number {roll_number} Deleted")
            else:
                student.delete()
                messages.warning(request, "Student photo doesn't exist on server")
                messages.info(request, f"Student With Roll Number {roll_number} Deleted")
            return redirect('/')

        
        return render(request, 'student/delete.html')

################## Documents ################
class DocumentViews:
    
    @login_required
    def addDocument(request):
        if request.method == "POST":
            roll_number = request.POST.get('roll_number', None) or request.user.username
            student = Student.objects.filter(roll_number=roll_number.upper())
            if not student:
                messages.warning(request, f"Student With Roll Number '{roll_number}' Doesn't Exist")
                return redirect('/document/add')
            
            document_name = request.POST.get('document_name')
            document = request.FILES.get('document')
            
            docs = StudentDocument.objects.create(
                student = student[0],
                document_name = document_name,
                document = document
            )
            docs.save()
            
            messages.success(request, "Document added successfully")
            return redirect('/')
        return render(request, 'document/add.html')
            
    @login_required
    def allDocuments(request):
        if request.user.is_superuser:
            roll_number = request.GET.get('roll_number', '').upper()
            if not roll_number:
                param = {'form': True}
                return render(request, 'document/alldocs.html', param)
            documents = StudentDocument.objects.filter(student__roll_number=roll_number)
            data = {'documents': list(documents.values('document', 'document_name', 'id')), 'student_name': documents[0].student.full_name if documents else roll_number}
            return JsonResponse(data)
        
        roll_number = request.user.username
        documents = StudentDocument.objects.filter(student__roll_number=roll_number)
        param = {'documents': documents, 'form': False}
        return render(request, 'document/alldocs.html', param)
        
    
    @login_required
    def editDocument(request, file=None):
        if request.method == "GET":
            document = StudentDocument.objects.filter(document=f"document/{file}").first()
            if not request.user.is_superuser and request.user.username != document.student.roll_number:
                messages.warning(request, "You don't have access to edit this file")
                return redirect("/document/all-docs")
            if not document:
                messages.error(request, "File not found")
                return redirect("/document/all-docs")
            param = {
                "file": file,
                "document": document
            }
            return render(request, "document/edit.html", param)
        
        file = request.POST.get("file")
        document_name = request.POST.get("document_name")
        document = StudentDocument.objects.get(document=f"document/{file}")
        document.document_name = document_name
        
        if request.FILES:
            os.remove(document.document.url[1:])
            document.document = request.FILES.get("document")
        document.upload_time = timezone.now()
        
        document.save()
        messages.success(request, "Document edited successfully")
        return redirect("/document/all-docs")
         
    @login_required
    def delDocument(request, file):
        document = StudentDocument.objects.filter(document=f"document/{file}").first()
        if not request.user.is_superuser and request.user.username != document.student.roll_number:
            messages.warning(request, "You don't have access to delete this file")
            return redirect("/document/all-docs")
        if not document:
            return HttpResponse("File does not exist !!!")
        document_file = document.document.url[1:]
        if os.path.isfile(document_file):
            os.remove(document_file)
            document.delete()
            return HttpResponse("Document deleted successfully")
        else:
            return HttpResponse("File does not exist on server !!!")
        
        

################## Attendence ################

class AttendenceViews:
    @login_required
    def fillAttendence(request):
        pass
    
    @login_required
    def editAttendence(request):
        pass