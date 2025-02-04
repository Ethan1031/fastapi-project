# To have all of the necessary steps to create our own custom image. 

# Set up our base image. 
FROM python:3.9.7

# Setup working directory, which provide a path, and creating a folder called app. 
# app : Store all my application code, tell docker where the code to run
WORKDIR /usr/src/app

# 。/ means our working directory
COPY requirement.txt ./

# Store all our dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy all our code to current directory in our container
COPY . . 

# Specifies the default command to run when the container starts.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

