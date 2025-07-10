# Train Schedule Management API

A Dockerized FastAPI backend application for managing and querying train schedules. This project provides a set of RESTful APIs to handle train and station data, including adding new schedules and searching for routes.

The application loads initial data from `trains.json` and `stations.json` into memory and persists any new additions or updates back to these files.

## Tech Stack

- **Backend:** Python 3.12, FastAPI
- **Server:** Uvicorn
- **Containerization:** Docker, Docker Compose
- **Data Storage:** In-memory dictionaries with JSON file persistence

---

## Features

- **Train APIs:** Get all trains, get a specific train's schedule, and add a new train.
- **Station APIs:** Get all station names, get a specific station's schedule, and add/update a station's schedule.
- **Search API:** Find all trains that run between a specified origin and destination station.
- **Data Persistence:** All create/update operations are saved back to the `trains.json` and `stations.json` files.
- **Dockerized Environment:** The entire application is containerized for easy setup and consistent deployment, with hot-reloading enabled for development.
- **Interactive API Docs:** Automatically generated, interactive API documentation available at `/docs`.

---

## Project Structure

```
/train-schedule-api
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- trains.json
|   |-- stations.json
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).

### Installation & Running the Application

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/chiillbro/Train-Schedule-Management-API.git
    cd TRAINSTATIONS
    ```

2.  **Build and run the application using Docker Compose:**
    _This single command will build the Docker image and start the API service._

    ```bash
    docker-compose up --build
    ```

3.  **The API is now running!**
    - The API will be accessible at `http://localhost:8001`.
    - The interactive documentation (Swagger UI) can be accessed at `http://localhost:8001/docs`.

### Using the API

You can use tools like Postman, `curl`, or the interactive Swagger UI to interact with the endpoints.

**Example: Search for trains from StationA to StationB**

```bash
curl -X GET "http://localhost:8001/search?from=StationA&to=StationB"
```

---

## Stopping the Application

To stop the running containers, press `Ctrl + C` in the terminal where `docker-compose` is running, and then run:

```bash
docker-compose down
```

This will stop and remove the containers and the network created by Docker Compose.
