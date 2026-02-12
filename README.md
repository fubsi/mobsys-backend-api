# mobsys-backend-api

Backend API component for accessing the Aiven online database. This service provides secure database connectivity with SSL authentication.

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- SSL certificate file (`cert.pem`) for authentication
- Access credentials for the Aiven database

## Setup

### 1. Environment Configuration

Create a `.env` file in the project root directory:

```bash
cp .env.template .env
```

Edit the `.env` file with your Aiven database configuration values:

```env
# Full connection URI (includes all connection details)
AIVEN_SERVICE_URI=postgresql://user:password@host:port/database

# Individual connection parameters
AIVEN_DATABASE_NAME=your_database_name
AIVEN_HOST=your-aiven-host.aivencloud.com
AIVEN_PORT=12345
AIVEN_USER=your_username
AIVEN_PASSWORD=your_password

# Path to the Aiven SSL certificate
AIVEN_CERT_PATH=path/to/your/cert.pem
```

### 2. SSL Certificate

Place your SSL certificate file (`cert.pem`) in the project root directory. This certificate is required for secure SSL authentication with the Aiven database.

### 3. Install Dependencies

This project uses `uv` for dependency management. Install the required Python packages:

```bash
uv sync
```

This will create a virtual environment and install all dependencies defined in `pyproject.toml`.

## Usage

Run the backend API using `uv`:

```bash
uv run main.py
```

Alternatively, activate the virtual environment and run directly:

```bash
# Activate the virtual environment
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/Mac

# Run the application
python main.py
```

## Project Structure

```
mobsys-backend-api/
├── backend/
│   ├── classes/
│   │   └── aiven.py
│   └── __init__.py
├── main.py
├── example_connection.py
├── pyproject.toml
├── .env.template
└── README.md
```

## Security Notes

- **Never commit** your `.env` file or `cert.pem` to version control
- Keep your database credentials secure
- Ensure the SSL certificate is valid and up to date


## Latest Updates

Table *"Termine"* has changed:
- added column - "Titel"
- added column - "Uid"

Corresponding changes to backend *routes*
- Adds columns to several technical implementations to retrieve data
- *termine.py*, *teilnehmer.py*, *protokoll.py*