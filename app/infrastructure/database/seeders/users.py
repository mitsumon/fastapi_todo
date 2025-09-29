import asyncio

from sqlmodel import select

from app.core.dependencies import AsyncSessionLocal
from app.core.security import hash_password
from app.infrastructure.database.models.users import User


async def seed_users() -> None:
    """Seed the users table with initial data."""
    # Check if the table already has data
    async with AsyncSessionLocal() as session:
        statement = select(User).limit(1)
        first_user = await session.execute(statement)
        if first_user.first():
            print('Users table already seeded. Skipping...')
            return

        # Define seed data
        users = []
        password = hash_password('pAssw0rd')
        for i in range(1, 1001):
            print(f'Seeding user {i}/1000')
            username = f'User{i}'
            email = f'{username.lower()}@example.com'
            is_superuser = False
            if i == 1:
                is_superuser = True

            # users.append(
            #     User(
            #         username=username,
            #         email=email,
            #         password=password,
            #         is_active=True,
            #         is_superuser=is_superuser,
            #     ),
            # )
            # await asyncio.sleep(0.01)  # Simulate some delay
            session.add(
                User(
                    username=username,
                    email=email,
                    password=password,
                    is_active=True,
                    is_superuser=is_superuser,
                ),
            )
            # # Add users to the session
            # session.add_all(users)
            await session.commit()
        print('Seeded users table successfully!')


async def get_all_users() -> list[User]:
    """Retrieve all users from the database."""
    async with AsyncSessionLocal() as session:
        statement = select(User.id, User.username, User.email)
        # .where(
        #     User.username.like('Mitsuhito%'),
        # )
        result = await session.execute(statement)
        user_list = [
            {'id': user.id, 'username': user.username, 'email': user.email} for user in result.all()
        ]
        print(user_list)
        return user_list


if __name__ == '__main__':
    asyncio.run(seed_users())
