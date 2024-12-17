# fastapi-uv-example

This is an example of API project using:

- **FastAPI**: Builds high-performance APIs; includes automatic, interactive documentation.
- **pydantic**: Enforces data types and validation, simplifying data handling.
- **pytest**: Ensures code reliability through comprehensive testing.
- **uv**: Manages dependencies and packaging efficiently.
- **ruff**: Lints code to ensure consistency and readability.
- **scaler**: First class OpenAPI (formerly Swagger) support.

## Getting Started

Follow these steps to set up and run the project:

### Prerequisites

- Python 3.12

### Installation

To install project dependencies, use the following command:

```bash
make install
```

This command will set up the project's virtual environment and install all required dependencies specified in [pyproject.toml](./pyproject.toml).

## Running the Application

To run the application locally, use the following command:

```bash
make run
```

This will start the FastAPI server, allowing you to interact with the API.

## Running Tests

To run tests using pytest, execute the following command:

```bash
make test
```

## Scaler API

To view the API documentation, navigate to [http://localhost:5000/scaler](http://localhost:5000/scalar) in your browser.
