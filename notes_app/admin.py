from django.contrib import admin
from .models import NoteModel, User

# Register your models here.
@admin.register(NoteModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("note_id", "note_title", "note_content","last_update","created_on","user")
    
    def __str__(self):
        return self.note_title
    

@admin.register(User)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_name", "user_email","password","last_update","created_on")  

    def __str__(self):
        return self.user_name
    

