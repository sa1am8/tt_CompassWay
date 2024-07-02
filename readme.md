# Loan Payment Schedule API

This project provides a backend service to generate and modify a loan payment schedule using Docker, Django, Django REST Framework, SQLite, and optionally Redis.

## Features

1. Generate a loan payment schedule with principal and interest payments.
2. Modify the principal amount of any payment and recalculate subsequent payments.

## Technologies Used

- Docker
- Django
- Django REST Framework
- PostgreSQL (via Docker)
- SQLite (default database)

## Setup and Running

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. **Clone the repository**

    ```sh
    git clone https://github.com/your-repo/loan-payment-schedule.git
    cd loan-payment-schedule
    ```

2. **Create a `.env` file**

    Create a `.env` file in the root of your project and add the following environment variables:

    ```env
    POSTGRES_DB=mydatabase
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    DATABASE_URL=postgres://myuser:mypassword@db:5432/mydatabase
    ```

3. **Build and run the Docker containers**

    ```sh
    docker-compose up --build
    ```

4. **Run database migrations**

    Open a new terminal and run:

    ```sh
    docker-compose exec web pipenv run python manage.py migrate
    ```

5. **Access the application**

    The application should now be running at `http://localhost:8000`.

## API Endpoints

### Generate Payment Schedule

- **URL:** `/api/schedule/`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
        "amount": 1000,
        "loan_start_date": "2024-01-10",
        "number_of_payments": 4,
        "periodicity": "1m",
        "interest_rate": 10.0
    }
    ```

- **Response:**

    ```json
    [
        {
            "id": 1,
            "date": "2024-02-10",
            "principal": 240.00,
            "interest": 10.00
        },
        ...
    ]
    ```

### Update Payment

- **URL:** `/api/payment/<int:payment_id>/`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
        "new_principal": 100.00
    }
    ```

- **Response:**

    ```json
    [
        {
            "id": 1,
            "date": "2024-02-10",
            "principal": 100.00,
            "interest": 10.00
        },
        ...
    ]
    ```

## Running Tests

To run tests, execute the following command:

```sh
docker-compose exec web pipenv run python manage.py test
