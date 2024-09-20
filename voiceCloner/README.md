Voice Cloning Project

Overview

This project is a Django-based web application that allows users to record and upload their voice recordings, which can then be used to clone voices using Text-to-Speech (TTS) technology. It includes user authentication, voice recording management, and an API for voice cloning.

Features

•	User Authentication: Sign up, login, and logout functionalities.
•	Voice Recording: Upload and manage voice recordings.
•	Voice Cloning: Clone voices using TTS models and save the cloned output.
•	API Endpoints: REST API for managing voice recordings and cloning voices.
•	Swagger Documentation: Interactive API documentation using Swagger.
Installation

git clone https://github.com/ezgiekin/Voice-Cloning-App.git

cd Voice-Cloning-App/voiceCloner

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

API Documentation

•	Swagger UI: /swagger/ - Interactive API documentation.
•	Swagger JSON: /swagger.json/ - Raw Swagger JSON schema.
•	Redoc: /redoc/ - Alternative API documentation.
To deploy with docker

git clone https://github.com/ezgiekin/Voice-Cloning-App.git cd Voice-Cloning-App/voiceCloner

docker build -t image-name .

docker run --name container-name -d -p 8000:8000 image-name

then go to http://localhost:8000