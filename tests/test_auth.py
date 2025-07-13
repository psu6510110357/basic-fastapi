#!/usr/bin/env python3
"""
Test script to verify authentication endpoint
"""
import asyncio
import httpx


async def test_authentication():
    """Test the authentication endpoint"""
    
    base_url = "http://localhost:8000"
    
    # Test data
    test_credentials = {
        "username": "string",
        "password": "string"
    }
    
    print(f"Testing authentication endpoint at {base_url}/api/v1/auth/token")
    print(f"Using credentials: username='{test_credentials['username']}', password='{test_credentials['password']}'")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Test authentication
            response = await client.post(
                f"{base_url}/api/v1/auth/token",
                data=test_credentials,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print()
            
            if response.status_code == 200:
                token_data = response.json()
                print("✓ Authentication successful!")
                print(f"Access Token: {token_data.get('access_token', 'N/A')[:50]}...")
                print(f"Refresh Token: {token_data.get('refresh_token', 'N/A')[:50]}...")
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


if __name__ == "__main__":
    asyncio.run(test_authentication())
