from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom manager to handle user creation (normal and superuser)
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        # Ensure the email is provided and normalized
        if not email:
            raise ValueError('The Email must be set.')
        email = self.normalize_email(email)
        # Create a new user with the provided fields
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Set default fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        # Validation for staff and superuser status
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# Custom user model extending Django's AbstractUser
class CustomUser(AbstractUser):
    # User types to differentiate roles (Basic, Admin, Listing)
    USER_TYPE_CHOICES = (('basic', 'Basic User'),
                         ('admin', 'Admin User'),
                         ('listing', 'Listing User'))
    
    # User type field to categorize users
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='basic')

    # Customize groups and permissions with unique related names to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.'
    )

    # Override username field with additional validation
    username = models.CharField(max_length=150,
                                unique=True,
                                help_text='Required. 150 characters or fewer.',
                                validators=[],
                                error_messages={'unique': "A user with that username already exists."})
    
    # Helper methods to check the user type
    def is_basic(self):
        return self.user_type == 'basic'

    def is_admin(self):
        return self.user_type == 'admin'

    def is_listing(self):
        return self.user_type == 'listing'
    
    # Assign the custom user manager to the model
    objects = CustomUserManager()

# Model for storing voice recordings along with metadata
class VoiceRecording(models.Model):
    # Foreign key linking the recording to a specific user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # Fields to store metadata about the recording
    name = models.TextField()
    gender = models.TextField()
    
    # FileField to store the cloned voice after processing
    cloned = models.FileField(upload_to='cloned_voices/')
    
    # Automatically set the upload timestamp when the record is created
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def audio_file_count(self):
        return self.files.count()

class AudioFile(models.Model):
    recording = models.ForeignKey(VoiceRecording, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='recordings/')

    def __str__(self):
        return f"{self.recording.name} - {self.file.name}"