# Shop Registration System

## Overview

The Shop Registration System is a Django web application designed to enable users to register shops and search for them based on geographical location. Users can input their latitude and longitude to find nearby shops, utilizing the Haversine formula for accurate distance calculations.

## Features

- **Shop Registration**: Users can register shops with essential details, including:
  - Name
  - Address
  - Owner Name
  - Phone Number
  - Email
  - Latitude
  - Longitude

- **User Search Functionality**: Users can search for shops by entering their current latitude and longitude.

- **Distance Calculation**: The application calculates the distance from the user's location to registered shops using the Haversine formula.

- **Data Validation**: Ensures data integrity with proper validations for latitude, longitude, and other shop details.

- **API Documentation**: The project utilizes Swagger for API documentation, making it easy to interact with the API endpoints.

## Technologies Used

- **Backend**: Python
- **Web Framework**: Django (5.1.2)
- **API Development**: Django REST Framework
- **Frontend**: HTML/CSS (Bootstrap for responsive UI)

## Project Setup

### Prerequisites

- Python 3.x
- Django 5.1.2
- Django REST Framework

### Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install required packages**:
    ```bash
    pip install django djangorestframework
    ```

4. **Run database migrations** (if applicable):
    ```bash
    python manage.py migrate
    ```

5. **Run the Django development server**:
    ```bash
    python manage.py runserver
    ```

6. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Endpoints

- **Shop Registration**: 
  - `POST /shops/register/` - Register a new shop with details.
  
- **Check Shop Name**: 
  - `GET /shops/check-shop-name/` - Check if a shop name is already taken.
  
- **Check Latitude and Longitude**: 
  - `GET /shops/check-lat-long/` - Validate latitude and longitude values.
  
- **List Shops**: 
  - `GET /shops/list/` - Retrieve a list of all registered shops.
  
- **Search Shops**: 
  - `GET /shops/search/` - Search for shops based on user-provided latitude and longitude.

- **API Documentation**: 
  - Swagger UI is available at `http://localhost:8000/docs/`, providing interactive documentation for the API endpoints.

## Usage

- **Register a Shop**: Navigate to the "Register Shop" page to input shop details. Ensure that all fields are filled out correctly to avoid validation errors.

- **Search for Shops**: Use the search form in the navigation bar to find shops by entering your latitude and longitude. The application will return a list of nearby shops along with their distances from your location.
