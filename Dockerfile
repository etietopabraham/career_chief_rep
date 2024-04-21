# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install AllenNLP and other necessary packages directly
RUN pip install --no-cache-dir allennlp==2.10.1 allennlp-models==2.10.1

# Copy only the necessary SRL script files
# COPY ./src/srl_script.py /app/srl_script.py

# Run when the container launches
CMD ["python", "srl_script.py"]
