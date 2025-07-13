#!/usr/bin/env python3
"""
Debug script to test password hashing and verification
"""
import asyncio
from app.models.user_model import DBUser


async def test_password_verification():
    """Test password hashing and verification"""

    # Test with the password that was likely used when creating the user
    test_passwords = ["string", "password", "123456", "admin", "test"]

    # The stored hash from your logs
    stored_hash = "$2b$12$EODrBOBl1zgpFpceakATTu.xfdkgnlarp0gYAiiJv/v4MdyQNfP2q"

    print("Testing password verification...")
    print(f"Stored hash: {stored_hash}")
    print()

    # Create a test user instance
    user = DBUser(
        email="test@test.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        password=stored_hash,
    )

    for password in test_passwords:
        print(f"Testing password: '{password}'")
        try:
            result = await user.verify_password(password)
            print(f"  Result: {'✓ MATCH' if result else '✗ NO MATCH'}")
            if result:
                print(f"  SUCCESS! The correct password is: '{password}'")
                break
        except Exception as e:
            print(f"  Error: {e}")
        print()

    # Also test creating a new hash with "string" password
    print("\nTesting hash creation with 'string' password:")
    new_hash = await user.get_encrypted_password("string")
    print(f"New hash: {new_hash}")

    # Test if the new hash works
    user.password = new_hash
    result = await user.verify_password("string")
    print(
        f"New hash verification with 'string': {'✓ MATCH' if result else '✗ NO MATCH'}"
    )


if __name__ == "__main__":
    asyncio.run(test_password_verification())
