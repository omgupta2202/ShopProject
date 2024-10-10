# Shop Registration System

## Overview

The Shop Registration System is a Django web application that allows users to register shops and search for them based on their geographical location. Users can input their latitude and longitude to find shops nearby, utilizing the Haversine formula to calculate distances accurately.

## Features

- **Shop Registration**: Shops can register with details such as name, address, owner name, phone number, email, latitude, and longitude.
- **User Search Functionality**: Users can search for shops by entering their current latitude and longitude.
- **Distance Calculation**: The application calculates the distance from the user's location to registered shops using the Haversine formula.
- **Data Validation**: Ensures data integrity with proper validations for latitude, longitude, and other shop details.

## Technologies Used

- Python
- Django (5.1.2)
- Django REST Framework (for APIs)
- HTML/CSS (Bootstrap for UI)

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

4. **Run the Django development server**:
    ```bash
    python manage.py runserver
    ```

5. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Endpoints

- **Shop Registration**: `POST /shops/register/`
- **Search Shops**: `GET /shops/search/`

## Usage

- **Register a Shop**: Navigate to the "Register Shop" page to input shop details.
- **Search for Shops**: Use the search form in the navigation bar to find shops by entering your latitude and longitude.

