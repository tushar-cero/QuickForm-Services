# QuickForms Services

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**

        Clone this repo.

2. **Create and activate a virtual environment**:

    ```bash
    # Create virtual environment
    python3 -m venv env

    # Activate virtual environment
    source .venv/bin/activate
    ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the FastAPI application:

```bash
uvicorn main:app --reload
```