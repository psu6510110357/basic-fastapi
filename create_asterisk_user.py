#!/usr/bin/env python3
"""
Create a test user with asterisk password for Swagger UI testing
"""
import asyncio
from app.core.database import init_db, get_session
from app.models.user_model import DBUser
import uuid


async def create_asterisk_user():
    """Create a user with asterisk password for testing Swagger UI"""

    await init_db()

    async for session in get_session():
        try:
            # Check if user already exists
            from sqlmodel import select

            result = await session.exec(
                select(DBUser).where(DBUser.username == "testuser")
            )
            existing_user = result.first()

            if existing_user:
                print("User 'testuser' already exists, updating password...")
                # Update the existing user's password to asterisks
                existing_user.password = await existing_user.get_encrypted_password(
                    "********"
                )
                session.add(existing_user)
                await session.commit()
                print("✓ Updated existing user password to '********'")
            else:
                # Create new user with asterisk password
                new_user = DBUser(
                    id=uuid.uuid4(),
                    email="test@swagger.com",
                    username="testuser",
                    first_name="Test",
                    last_name="User",
                    password="",  # Will be set below
                )

                # Set the password to asterisks
                new_user.password = await new_user.get_encrypted_password("********")

                session.add(new_user)
                await session.commit()
                print("✓ Created new user 'testuser' with password '********'")

            print("\nNow you can test in Swagger UI with:")
            print("Username: testuser")
            print("Password: ******** (8 asterisks)")

        except Exception as e:
            print(f"Error: {e}")
            await session.rollback()
        finally:
            break


if __name__ == "__main__":
    asyncio.run(create_asterisk_user())
