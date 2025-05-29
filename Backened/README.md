# Cloud Computing Management Platform (CCMP) Backend

This is the backend service for the Cloud Computing Management Platform, built with FastAPI and Python.

## Features

- AWS Resource Management
  - EC2 Instance Management
  - S3 Bucket Management
  - CloudWatch Metrics
- User Authentication
- API Documentation
- Caching with Redis
- Database Integration with PostgreSQL

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- AWS Account with appropriate permissions

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
CCMP/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── aws.py
│   ├── models/
│   ├── schemas/
│   └── main.py
├── tests/
├── alembic/
├── requirements.txt
└── README.md
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 