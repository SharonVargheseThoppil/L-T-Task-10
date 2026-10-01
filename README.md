# Containerizing Flask Deep Learning API

## Task 10

This project demonstrates how to containerize and deploy a Flask-based deep learning API using Docker.

## Build and run

    docker build -t cifar_flask-deep-learning-api:2.0 .
    docker run -d --name flask-api -p 5000:5000 cifar_flask-deep-learning-api:2.0

## Test

    curl.exe http://localhost:5000/health
    curl.exe -X POST -F "image=@test_image.jpg" http://localhost:5000/predict