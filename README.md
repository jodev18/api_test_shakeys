# API Test Shakeys

A FastAPI-based REST API with JWT authentication, user management, and geographic data (regions and provinces).

## Features

- User Authentication (JWT Tokens)
- Protected Routes
- Region Management
- Province Management
- SQLite Database
- Redis Caching (Optional)

## Prerequisites

- Python 3.x
- uv (Python package installer)
- SQLite3
- Redis (Optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jodev18/api_test_shakeys.git
cd api_test_shakeys
```

2. Install dependencies using uv:
```bash
# or
uv sync  # if using pyproject.toml
```

## Running the Application

Start the FastAPI server:
```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /user/new` - Register new user
- `POST /user/login` - Login and get JWT token

### Regions (Protected Routes)
- `GET /regions` - List all regions
- `GET /regions/{region_id}` - Get specific region

### Provinces (Protected Routes)
- `GET /provinces` - List all provinces
- `GET /provinces/{province_id}` - Get specific province

## Authentication

All region and province endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Database

The application uses SQLite for data storage. The database file is `provinces.db`.

## Docker

### Building and Running with Docker

1. Build the Docker image:
```bash
docker build -t api_test_shakeys .
```

2. Run the container:
```bash
docker run -p 8000:8000 api_test_shakeys
```

The API will be available at `http://localhost:8000`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
