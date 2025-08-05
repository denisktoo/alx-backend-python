FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in container
WORKDIR /chats

# Install system dependencies for mysqlclient
RUN apt-get update \
  && apt-get install -y default-libmysqlclient-dev gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the codebase
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "manage.py", "runserver", "-p", "0.0.0.0:8000"]
