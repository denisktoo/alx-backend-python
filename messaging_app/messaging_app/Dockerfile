FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in container
WORKDIR /chats

# Install system dependencies for mysqlclient
RUN apt-get update \
  && apt-get install -y default-libmysqlclient-dev gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from one level above
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy entire Django app from parent directory into container
COPY ../ .

# Expose port 8000
EXPOSE 8000

# Run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
