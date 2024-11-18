from django.contrib import admin
from .models import *
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'group', 'standard', 'start_year', 'roll_number', 'birth_date', 'discussed_fee', 'remaining_fees', 'student_mobile_number', 'parrent_mobile_number', 'status']
    
admin.site.register(Student, StudentAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'document_name', 'upload_time', 'document']
admin.site.register(StudentDocument, DocumentAdmin)

# Customising admin panel
admin.site.site_header = "Mudra Classes"
admin.site.index_title = "Mudra Classes Admin Portal"
admin.site.site_title = "Mudra Classes - Admin"