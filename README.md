# 🏋️‍♂️ Fitness Tracker: Health & Consultation Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg)](https://www.djangoproject.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-brightgreen.svg)]()
[![Google Calendar API](https://img.shields.io/badge/Google_Calendar-Integrated-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, multi-tier fitness ecosystem built with **Django**. This platform bridges the gap between fitness enthusiasts and professional trainers by offering personalized health tracking, dynamic workout assignments, real-time communication, and automated consultation scheduling.

## ✨ Key Features

The platform operates on a robust Role-Based Access Control (RBAC) system, catering to three distinct user types:

### 👤 For Users
* **Personalized Profiles & Goals:** Set granular fitness goals, track daily progress, and maintain interactive health journals.
* **Workout Management:** Receive and log tailored workout plans directly from assigned trainers.
* **Consultation Booking:** Seamlessly book 1-on-1 sessions with trainers. Appointments automatically sync to your **Google Calendar**.
* **Real-Time Communication:** Chat and video conference directly with trainers using a high-performance **WebSocket** pipeline.
* **Trainer Reviews:** Leave ratings and feedback for trainers based on consultation quality.

### 🏋️‍♀️ For Trainers
* **Client Management Dashboard:** Monitor client progress, analyze milestone analytics, and adjust routines dynamically.
* **Workout Assignments:** Create and deploy personalized exercise regimens for individual users.
* **Schedule Management:** Manage availability and conduct virtual consultations via integrated video conferencing.

### 🛡️ For Admins
* **Platform Oversight:** Complete control over user management, role assignments, and platform analytics.
* **Data Moderation:** Ensure platform integrity and manage trainer verifications.

## 🛠️ Technical Architecture & Stack

* **Backend Framework:** Python, Django
* **Real-Time Communication:** Django Channels, WebSockets, Redis (for channel layers)
* **Authentication:** OAuth 2.0 (Secure login), Session Management
* **External Integrations:** Google Calendar API (Automated event scheduling)
* **Database:** SQLite (Dev) / PostgreSQL (Prod recommended)

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

* Python 3.10+
* Redis (Required for WebSocket communication)
* Google Cloud Console account (for Calendar API and OAuth credentials)

### Installation

1. **Clone the repository:**

    git clone https://github.com/CrossShot06/fitness-tracker.git
    cd fitness-tracker

2. **Create and activate a virtual environment:**

    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

3. **Install dependencies:**

    pip install -r requirements.txt

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory and configure the following variables:

    SECRET_KEY=your_django_secret_key
    DEBUG=True

    # Google API Credentials
    GOOGLE_OAUTH_CLIENT_ID=your_client_id
    GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
    GOOGLE_CALENDAR_API_KEY=your_api_key
   
    # Redis (For Channels/WebSockets)
    REDIS_URL=redis://127.0.0.1:6379/1

5. **Run Database Migrations:**

    python manage.py makemigrations
    python manage.py migrate

6. **Create a Superuser (Admin):**

    python manage.py createsuperuser

7. **Start the Redis Server:**
   *(Ensure Redis is installed and running on your machine on port 6379)*

8. **Run the Development Server:**

    # Using Daphne or standard runserver for ASGI
    python manage.py runserver

   Navigate to `http://127.0.0.1:8000/` to view the application.

## 📡 WebSockets & Google API Implementation
* **WebSockets:** Utilizes Django Channels to handle asynchronous HTTP and WebSocket protocols. This ensures low-latency, bi-directional communication for the chat and live video features.
* **Google Calendar API:** Leveraging Google's RESTful API to programmatically create, fetch, and update calendar events based on user-trainer bookings, secured via OAuth tokens.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/CrossShot06/fitness-tracker/issues).

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author
**Soham Sarkar**
* GitHub: [@CrossShot06](https://github.com/CrossShot06)
* LinkedIn: [Soham Sarkar](https://www.linkedin.com/in/soham-sarkar-a6a0a2317/)
