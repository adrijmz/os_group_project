# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download nltk stopwords
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Make port 5000 available to the world outside this container
# EXPOSE 5000

# Run app.py when the container launches
CMD ["bash", "-c", "python src/functionalities/grobid.py && python src/functionalities/wikidataProcess.py && python src/functionalities/openalex.py && python src/functionalities/abstract_lda.py && python src/functionalities/knowledge_graph.py && python src/api/app.py"]
