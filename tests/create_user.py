#!/usr/bin/env python3
"""
Script to create a test user for authentication testing
"""
import asyncio
import httpx


async def create_test_user():
    """Create a test user via the API"""
    
    base_url = "http://localhost:8000"
    
    # Test user data
    user_data = {
        "email": "test@example.com",
        "username": "string",
        "first_name": "Test",
        "last_name": "User",
        "password": "string"
    }
    
    print(f"Creating test user at {base_url}/api/v1/users/")
    print(f"User data: {user_data}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Create user
            response = await client.post(
                f"{base_url}/api/v1/users/",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Response Status: {response.status_code}")
            print()
            
            if response.status_code == 201:
                user_response = response.json()
                print("✓ User created successfully!")
                print(f"User ID: {user_response.get('id', 'N/A')}")
                print(f"Username: {user_response.get('username', 'N/A')}")
                print(f"Email: {user_response.get('email', 'N/A')}")
            elif response.status_code == 409:
                print("ℹ User already exists (this is fine for testing)")
                try:
                    error_data = response.json()
                    print(f"Details: {error_data.get('detail', 'N/A')}")
                except Exception:
                    print(f"Response: {response.text}")
            else:
                print("✗ User creation failed!")
                try:
                    error_data = response.json()
                    print(f"Error: {error_data}")
                except Exception:
                    print(f"Error response: {response.text}")
    
    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
        print("Make sure the FastAPI server is running on http://localhost:8000")


if __name__ == "__main__":
    asyncio.run(create_test_user())
