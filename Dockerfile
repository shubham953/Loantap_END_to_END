# The Dockerfile defines the image's environment
# Import Python runtime and set up working directory
FROM python:3.8
WORKDIR app
ADD . /app
COPY \requirements.txt .
# Install any necessary dependencies
RUN pip install -r requirements.txt
COPY \app.py .




# Run app.py when the container launches
CMD ["python", "app.py","--host","0.0.0.0"]