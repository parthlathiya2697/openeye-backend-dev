# Article Generation Automation

Generate Articles based on:
    - Trending Articles
    - Most Viewed Articles

Implement:
    - FastApi : Serving as a Backend for requests from,
    - Frontend : Where users will interact and see the content

Technology Stack:
    - Uvicorn
    - FastAPI
    - SQLAlchemy Cloud
    - Pydantic

Test:
    - Jwt token expirey

Alembic Migration Commands
    - alembic revision --autogenerate -m "Added user mobile number in user table"
    - alembic upgrade head
