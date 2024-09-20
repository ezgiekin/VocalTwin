from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import VoiceRecording,AudioFile
from .forms import LoginForm, RegisterForm, VoiceRecordingEdit, CloneText
from TTS.api import TTS
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework import viewsets
from .models import VoiceRecording, AudioFile
from .serializers import VoiceRecordingSerializer, AudioFileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class VoiceRecordingViewSet(viewsets.ModelViewSet):
    queryset = VoiceRecording.objects.all()
    serializer_class = VoiceRecordingSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the VoiceRecording instance
            voice_recording = serializer.save()
            # Handle the AudioFile if provided
            if 'audio' in request.data:
                audio_file_serializer = AudioFileSerializer(data={'recording': voice_recording.id, 'file': request.data['audio']})
                if audio_file_serializer.is_valid():
                    audio_file_serializer.save()
                else:
                    return Response(audio_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer


# Renders the opening page
def opening(request):
    return render(request, 'base/opening.html')

# Handles voice recording and uploading (only accessible to logged-in users)
@login_required(login_url="base:login")
def record_voice(request):
    context = {'records': VoiceRecording.objects.all()}
    if request.method == 'POST':
        audio_file = request.FILES.get('audio') 
        uploaded_audio = request.FILES.get('uploaded_audio')
        if audio_file or uploaded_audio:
            # Creates a new VoiceRecording instance with the submitted data
            voice_recording = VoiceRecording.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
            )

            AudioFile.objects.create(
                recording=voice_recording,
                file=uploaded_audio if uploaded_audio else audio_file
            )
            return JsonResponse({"message": "Upload successful"}, status=200)
        return JsonResponse({"message": "No audio file provided"}, status=400)
    
    return render(request, 'base/record.html', context=context)

# Handles login functionality
def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('base:record_voice')
            else:
                form.add_error(None, "Invalid username or password")
    
    return render(request, 'base/login.html', {'loginform': form})

# Handles user registration
def sign_up(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()  # Saves new user
        return redirect('base:login')
    
    return render(request, 'base/signup.html', {'sign_upform': form})

# Handles logout functionality
def logout(request):
    auth_logout(request)
    return redirect("base:opening")

# Deletes a specific VoiceRecording instance by ID
def delete_object_function(request, id):
    VoiceRecording.objects.filter(id=id).delete()
    return redirect('base:record_voice')

# Handles voice cloning using TTS
def clone(request, id):
    ob = get_object_or_404(VoiceRecording, id=id)
    form = CloneText(request.POST)
    
    if request.method == "POST" and form.is_valid():
        text = request.POST.get("text")
        language = request.POST.get("text_language")

        # Create an in-memory file object
        output_file = BytesIO()

        audio_Files = ob.files.all()
        file_paths = [audio_file.file.path for audio_file in audio_Files]
        
        # Generate cloned voice using TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        tts.tts_to_file(text=text, file_path=output_file, speaker_wav=file_paths, language=language, split_sentences=True)

        # Save cloned voice to the database
        output_file.seek(0)  # Move to the start of the BytesIO object
        ob.cloned.save(f"{id}_output.wav", ContentFile(output_file.read()))
        output_file.close()  # Clean up in-memory file object
        
        return redirect('base:result', id=ob.id)
    
    return render(request, 'base/clone.html', {"cloneform": form})

# Displays the result after cloning
def result(request, id):
    ob = get_object_or_404(VoiceRecording, id=id)
    return render(request, "base/result.html", {'record': ob})

# Handles editing of VoiceRecording instances
def edit(request, id):
    ob = get_object_or_404(VoiceRecording, id=id)
    form = VoiceRecordingEdit(request.POST or None, instance=ob)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('base:record_voice')
    
    return render(request, 'base/edit.html', {"editform": form})

#Adds a voice record to a already existing person
def add_record(request,id):
    ob = get_object_or_404(VoiceRecording,id=id)
    if request.method == "POST":
        audio_file = request.FILES.get('audio')
        if audio_file:
            new_audio_file = AudioFile(recording=ob, file=audio_file)
            new_audio_file.save()
            return redirect("base:record_voice")
    return render(request,"base/add_record.html")

@api_view(['POST'])
def clone_voice_api(request, id):
    try:
        voice_recording = VoiceRecording.objects.get(id=id)
    except VoiceRecording.DoesNotExist:
        return Response({"error": "VoiceRecording not found"}, status=status.HTTP_404_NOT_FOUND)

    text = request.data.get('text')
    language = request.data.get('language')

    if not text or not language:
        return Response({"error": "Text and language must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Create an in-memory file object
    output_file = BytesIO()

    # Generate cloned voice using TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    tts.tts_to_file(text=text, file_path=output_file, speaker_wav=[voice_recording.files.first().file.path], language=language, split_sentences=True)

    # Save cloned voice to the database
    output_file.seek(0)
    voice_recording.cloned.save(f"{id}_output.wav", ContentFile(output_file.read()))
    output_file.close()

    serializer = VoiceRecordingSerializer(voice_recording)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_audio_to_record(request, id):
    try:
        voice_recording = VoiceRecording.objects.get(id=id)
    except VoiceRecording.DoesNotExist:
        return Response({"error": "VoiceRecording not found"}, status=status.HTTP_404_NOT_FOUND)

    if 'audio' in request.FILES:
        audio_file = request.FILES['audio']
        AudioFile.objects.create(recording=voice_recording, file=audio_file)
        return Response({"message": "Audio file added successfully"}, status=status.HTTP_201_CREATED)

    return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)