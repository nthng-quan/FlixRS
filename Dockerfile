FROM python:3.9-slim
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.in .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.in

# Copy the rest of the application code to the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the entry point for the container
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
