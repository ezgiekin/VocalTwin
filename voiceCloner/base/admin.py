from django.contrib import admin
from .models import VoiceRecording, CustomUser,AudioFile
from django.contrib.auth.admin import UserAdmin

# Register VoiceRecording with its associated ModelAdmin class
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'user', 'uploaded_at')

# Customize the CustomUser admin interface
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    def delete_model(self, request, obj):
        VoiceRecording.objects.filter(user=obj).delete()
        obj.delete()

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('recording_name', 'recording_gender', 'recording_user', 'file')

    def recording_name(self, obj):
        return obj.recording.name
    recording_name.admin_order_field = 'recording__name'  # Allows sorting by this field
    recording_name.short_description = 'Recording Name'

    def recording_gender(self, obj):
        return obj.recording.gender
    recording_gender.admin_order_field = 'recording__gender'
    recording_gender.short_description = 'Recording Gender'

    def recording_user(self, obj):
        return obj.recording.user.username
    recording_user.admin_order_field = 'recording__user'
    recording_user.short_description = 'Recording User'