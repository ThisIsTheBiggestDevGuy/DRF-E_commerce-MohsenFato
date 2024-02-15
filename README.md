Hi
this is my first fully completed DRF project to showcase my designing, structuring and coding skills (i'll refuse to use "engineering").



if you want to know about the project, download and study the file "E-commerce Documentation.pdf" fore a detailed explanation of my project.

if you want to clone, run and test the project for yourself, here's the step-by-step guide:


- Clone the Repository:
Clone your Django project repository from GitHub to your local machine using Git.

- Install Docker Desktop:
If you haven't already, download and install Docker Desktop from the official Docker website. Follow the installation instructions for your operating system.

- Navigate to the Project Directory:
Open a terminal or command prompt and navigate to the root directory of your Django project.

- Build the Docker Containers:
Run the following command to build the Docker containers defined in the docker-compose.yml file:
docker-compose build

- write a docker-compos.yml:
here's a basic example of that:
version: '3'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword



- Start the Docker Containers:
Once the containers are built, start the Docker containers using the following command:
docker-compose up

- Access the Application:
Once Docker Compose has finished setting up the containers, you can access your Django application in a web browser at http://localhost:8000.

- Access the Admin Panel:
If your project includes Django's admin panel, you can access it at http://localhost:8000/admin and log in using the superuser credentials.

- Interact with the Database:
The PostgreSQL database is running in a Docker container. You can interact with the database using tools like psql or database management software. Use the following credentials:

Host: localhost
Port: 5432
Database: e_commerce
Username: "yourusername"
Password: "yourpass"

- Stop the Containers:
When you're finished working with the application, you can stop the Docker containers by pressing Ctrl + C in the terminal where they are running.
