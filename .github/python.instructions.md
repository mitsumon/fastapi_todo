---
applyTo: "**/*.py"
---
## FastAPI Guidelines
- Use async/await for all I/O operations
- Use Clean Architecture principles
- Separate layers: domain(entities, value objects), application(use cases, interfaces), infrastructure(models, repositories(implementations)), presentation(api endpoints, schemas)
- Use Google Style DocStrings
- Use type hints for all functions and methods
- Use dependency injection for services and repositories
- Use Pydantic models for data validation and serialization
- Use SQLAlchemy ORM for database interactions
- Use Alembic for database migrations
- Use logging for error handling and debugging
- Write unit tests for all layers using pytest
