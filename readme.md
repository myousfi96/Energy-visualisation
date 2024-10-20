# Energy Data Visualization and Analysis Application

This project is an interactive web application for visualizing and analyzing synthetic energy data. It showcases skills in data generation, processing, and visualization using modern technologies like **FastAPI**, **Streamlit**, **Pandas**, and **Plotly**. The application includes real-time data simulation and provides users with interactive tools to explore energy metrics across different regions and time periods.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Technical Overview](#technical-overview)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## Features

- **Synthetic Data Generation**: Generates realistic energy data for multiple regions and metrics over the past 30 days.
- **Interactive Visualizations**: Includes line charts, bar charts, and scatter plots for data exploration.
- **Real-Time Data Monitoring**: Simulates real-time data updates and displays them in an interactive graph.
- **Data Filtering**: Users can filter data by region, metric, and date range.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and responsive user experience.
- **Modular Architecture**: Separates backend and frontend components for scalability and maintainability.
- **Dockerized Setup**: Uses Docker and Docker Compose for easy deployment.

---

## Project Structure

```
energy-data-visualization/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   ├── requirements.txt
└── docker-compose.yml
```

- **backend/**: Contains the FastAPI application that generates and serves synthetic energy data.
- **frontend/**: Contains the Streamlit application that provides the user interface.
- **docker-compose.yml**: Configuration file to set up Docker services for the backend and frontend.

---

## Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: Ensure Docker Compose is installed (usually comes with Docker Desktop).

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/energy-data-visualization.git
cd energy-data-visualization
```

### 2. Build Docker Images

Build the Docker images for both the backend and frontend services:

```bash
docker-compose build
```

---

## Running the Application

Start the application using Docker Compose:

```bash
docker-compose up
```

This command starts both the backend and frontend services. The backend service will generate synthetic energy data upon startup.

---

## Usage

### Access the Application

- **Frontend (Streamlit App)**: Open your web browser and navigate to `http://localhost:8501`.
- **Backend API Docs (Optional)**: Access the FastAPI interactive docs at `http://localhost:8000/docs`.

### Explore the Features

1. **Data Filters**:

   - Use the sidebar to select regions, metrics, and date ranges.
   - The application supports multiple selections for regions and metrics.

2. **Data Exploration**:

   - Group data by region, metric, or date.
   - View the aggregated data in a table format.

3. **Comparative Analysis**:

   - Visualize selected metrics over time using line charts.
   - Compare different energy metrics side by side.

4. **Regional Comparison**:

   - Analyze energy metrics across different regions using bar charts.

5. **Real-Time Data Monitoring**:

   - Observe simulated real-time data updates in a scatter plot.
   - The application auto-refreshes every 5 seconds to display new data points.

---

## Technical Overview

### Backend

- **Framework**: FastAPI
- **Functionality**:
  - Generates synthetic energy data for six regions and four metrics over the past 30 days.
  - Provides API endpoints to retrieve data, regions, and metrics.
  - Uses SQLAlchemy ORM for database interactions.
- **Endpoints**:
  - `GET /energy_data/`: Retrieves all energy data.
  - `GET /energy_data/region/{region}`: Retrieves data for a specific region.
  - `GET /regions/`: Retrieves a list of available regions.
  - `GET /metrics/`: Retrieves a list of available metrics.

### Frontend

- **Framework**: Streamlit
- **Functionality**:
  - Fetches data from the backend API.
  - Provides an interactive interface for data filtering and visualization.
  - Displays various charts and tables for data exploration.
  - Simulates real-time data updates and visualizes them.

---

## Customization

### Adjust Regions and Metrics

- Modify the `regions` and `metrics` lists in `backend/app.py` to customize the data generated.

```python
# In backend/app.py
regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
metrics = ['Power Output', 'Energy Consumption', 'Renewable Generation', 'CO2 Emissions']
```

### Change Data Generation Parameters

- Adjust the date range, frequency, and value ranges in the `generate_synthetic_energy_data` and `generate_metric_value` functions.

### Update Visualization Settings

- Modify the appearance and behavior of charts in `frontend/streamlit_app.py`.
- For example, change marker sizes, colors, or the number of data points displayed.

---

## Troubleshooting

### Common Issues

1. **Frontend Cannot Connect to Backend**

   - **Solution**: Ensure that the `API_URL` in `frontend/streamlit_app.py` points to the correct backend address.
     - If running without Docker networking, set `API_URL = "http://localhost:8000"`.

2. **Backend Service Not Running**

   - **Solution**: Check the backend logs for errors:

     ```bash
     docker-compose logs backend
     ```

     Ensure that the backend service starts correctly and generates data without errors.

3. **CORS Errors**

   - **Solution**: CORS is already configured in the backend to allow all origins. If issues persist, verify the middleware settings in `backend/app.py`.

4. **AttributeError: 'DataFrame' object has no attribute 'append'**

   - **Cause**: Using an outdated method (`append`) in Pandas.
   - **Solution**: The code uses `pd.concat()` to append new data points, which is compatible with newer versions of Pandas.

5. **Visualization Issues**

   - **Empty Charts**: Ensure that the selected filters return data.
   - **Map Not Displaying Data**: Verify that latitude and longitude values are valid and properly formatted.

### Need Help?

If you encounter issues not covered here, feel free to open an issue on the project's GitHub repository or consult the documentation for the libraries used.

---
