
FROM python:3.10.8

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$PATH:/root/.cargo/bin"

ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y \
    libsndfile1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "y" | python download_tts_model.py

EXPOSE 8000

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]