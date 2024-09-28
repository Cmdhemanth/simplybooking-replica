# SimplyBooking Replica

A simple appointment booking system where users can sign in, manage their own dashboard, add services that people can book, and view their scheduled bookings. The website is dynamically generated once an admin account is registered.

## Features
- **User Authentication**: Sign up and log in functionality for users.
- **User Dashboard**: After signing in, users can manage their own dashboard, add services they offer, and view bookings.
- **Dynamic Website Creation**: A dedicated website for booking services is dynamically created upon admin registration.
- **Booking Management**: Users can track how many bookings have been scheduled for their services.
- **SQLite Database**: The system uses SQLite to store user, service, and booking information.
- **Flask Framework**: The project uses Flask to handle HTTP requests and responses.

## Technologies Used
- **Flask**: Backend framework for handling HTTP requests and responses.
- **SQLite**: Lightweight database used for storing data.
- **HTML/CSS/JavaScript**: Frontend for user interfaces and dynamic content rendering.

## Setup

### Requirements
- Python 3.x
- Flask
- SQLite

### Installation Steps
1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-repo/simplybooking-replica.git
    cd simplybooking-replica
    ```

2. **Set up a Virtual Environment** (optional but recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**
    ```bash
    flask run
    ```

5. **Access the Application**
    Open your browser and navigate to `http://127.0.0.1:5000/`.
