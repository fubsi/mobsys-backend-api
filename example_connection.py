#!/usr/bin/env python3
"""
Example script to connect to an Aiven database using environment variables.

This script demonstrates how to:
1. Load environment variables from a .env file
2. Establish a connection to an Aiven PostgreSQL database
3. Perform a simple query to verify the connection

Requirements:
    pip install python-dotenv psycopg2-binary

Usage:
    1. Copy .env.template to .env
    2. Fill in your actual Aiven database credentials in .env
    3. Run: python example_connection.py
"""

import os
import sys
from dotenv import load_dotenv

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None

# Load environment variables from .env file
load_dotenv()

# Get Aiven database credentials from environment variables
AIVEN_SERVICE_URI = os.getenv('AIVEN_SERVICE_URI')
AIVEN_DATABASE_NAME = os.getenv('AIVEN_DATABASE_NAME')
AIVEN_HOST = os.getenv('AIVEN_HOST')
AIVEN_PORT = os.getenv('AIVEN_PORT')
AIVEN_USER = os.getenv('AIVEN_USER')
AIVEN_PASSWORD = os.getenv('AIVEN_PASSWORD')


def validate_environment_variables():
    """
    Validate that all required environment variables are set.
    
    Returns:
        bool: True if all variables are set, False otherwise
    """
    required_vars = {
        'AIVEN_SERVICE_URI': AIVEN_SERVICE_URI,
        'AIVEN_DATABASE_NAME': AIVEN_DATABASE_NAME,
        'AIVEN_HOST': AIVEN_HOST,
        'AIVEN_PORT': AIVEN_PORT,
        'AIVEN_USER': AIVEN_USER,
        'AIVEN_PASSWORD': AIVEN_PASSWORD
    }
    
    missing_vars = [var_name for var_name, var_value in required_vars.items() if not var_value]
    
    if missing_vars:
        print("Error: The following environment variables are not set:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease ensure you have:")
        print("1. Copied .env.template to .env")
        print("2. Filled in your actual Aiven database credentials in .env")
        return False
    
    return True


def connect_using_uri():
    """
    Connect to Aiven database using the service URI.
    
    Returns:
        connection: Database connection object or None if connection fails
    """
    if not PSYCOPG2_AVAILABLE:
        print("Error: psycopg2 is not installed.")
        print("Install it using: pip install psycopg2-binary")
        return None
    
    try:
        print("Attempting to connect using AIVEN_SERVICE_URI...")
        connection = psycopg2.connect(AIVEN_SERVICE_URI)
        print("✓ Successfully connected to Aiven database using service URI!")
        return connection
    
    except Exception as e:
        print(f"Error connecting to database using URI: {e}")
        return None


def connect_using_parameters():
    """
    Connect to Aiven database using individual connection parameters.
    
    Returns:
        connection: Database connection object or None if connection fails
    """
    if not PSYCOPG2_AVAILABLE:
        print("Error: psycopg2 is not installed.")
        print("Install it using: pip install psycopg2-binary")
        return None
    
    try:
        print("Attempting to connect using individual parameters...")
        connection = psycopg2.connect(
            host=AIVEN_HOST,
            port=AIVEN_PORT,
            database=AIVEN_DATABASE_NAME,
            user=AIVEN_USER,
            password=AIVEN_PASSWORD,
            sslmode='require'  # Aiven requires SSL
        )
        print("✓ Successfully connected to Aiven database using individual parameters!")
        return connection
    
    except Exception as e:
        print(f"Error connecting to database using parameters: {e}")
        return None


def test_connection(connection):
    """
    Test the database connection by executing a simple query.
    
    Args:
        connection: Database connection object
    """
    try:
        cursor = connection.cursor()
        
        # Execute a simple query to verify the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("\nDatabase connection test successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        cursor.close()
    
    except Exception as e:
        print(f"Error testing connection: {e}")


def main():
    """
    Main function to demonstrate Aiven database connection.
    """
    print("=" * 70)
    print("Aiven Database Connection Example")
    print("=" * 70)
    print()
    
    # Validate environment variables
    if not validate_environment_variables():
        sys.exit(1)
    
    print("Environment variables loaded successfully!")
    print(f"  Database: {AIVEN_DATABASE_NAME}")
    print(f"  Host: {AIVEN_HOST}")
    print(f"  Port: {AIVEN_PORT}")
    print(f"  User: {AIVEN_USER}")
    print()
    
    # Try connecting using service URI
    connection = connect_using_uri()
    
    # If URI connection fails, try using individual parameters
    if not connection:
        print("\nTrying alternative connection method...")
        connection = connect_using_parameters()
    
    # Test the connection if successful
    if connection:
        test_connection(connection)
        
        # Close the connection
        connection.close()
        print("\n✓ Connection closed successfully.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n✗ Failed to establish connection to Aiven database.")
        print("Please check your credentials and network connectivity.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
