#!/usr/bin/env python3
"""
Test script to simulate exactly what Swagger UI does
"""
import asyncio
import httpx


async def test_swagger_style_auth():
    """Test authentication using form data like Swagger UI"""

    base_url = "http://localhost:8000"

    print("Testing authentication exactly like Swagger UI...")
    print()

    # Test with form data (application/x-www-form-urlencoded)
    form_data = {
        "username": "string",
        "password": "string",
        "grant_type": "password",  # This is what OAuth2PasswordRequestForm expects
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    try:
        async with httpx.AsyncClient() as client:
            # Test authentication with form data
            response = await client.post(
                f"{base_url}/api/v1/auth/token",
                data=form_data,  # Use data for form encoding
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print()

            if response.status_code == 200:
                token_data = response.json()
                print("✓ Authentication successful!")
                print(f"Access Token: {token_data.get('access_token', 'N/A')[:50]}...")
                print(
                    f"Refresh Token: {token_data.get('refresh_token', 'N/A')[:50]}..."
                )
                print(f"Token Type: {token_data.get('token_type', 'N/A')}")
                print(f"Expires In: {token_data.get('expires_in', 'N/A')} minutes")
                print(f"User ID: {token_data.get('user_id', 'N/A')}")
            else:
                print("✗ Authentication failed!")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data}")
                except Exception:
                    print(f"Error response: {response.text}")

    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

    print("\n" + "=" * 50)
    print("Testing with minimal form data...")

    # Test with minimal form data
    minimal_form_data = {"username": "string", "password": "string"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/v1/auth/token",
                data=minimal_form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            print(f"Response Status: {response.status_code}")

            if response.status_code == 200:
                token_data = response.json()
                print("✓ Authentication successful with minimal data!")
            else:
                print("✗ Authentication failed with minimal data!")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data}")
                except Exception:
                    print(f"Error response: {response.text}")

    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_swagger_style_auth())
