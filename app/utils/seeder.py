import asyncio
from db_helper import connect_to_database
from models import User, EconomyFunction, Category
from werkzeug.security import generate_password_hash

async def create_sample_data():
    db = await connect_to_database()
    if db is None:
        print("Database connection failed. Cannot create sample data.")
        return

    # Create sample categories
    category1 = Category(name='Economics', description='Study of production, distribution, and consumption of goods and services')
    category1.save()

    category2 = Category(name='Game Theory', description='Study of strategic decision making')
    category2.save()

    # Create sample users
    user1 = User(username='user1', email='user1@example.com', password=generate_password_hash('password1'))
    user1.save()

    user2 = User(username='user2', email='user2@example.com', password=generate_password_hash('password2'))
    user2.save()

    # Create sample economy functions
    function1 = EconomyFunction(name='Function 1', path='path/to/function1', parameters={'param1': 'value1'}, category=category1)
    function1.save()

    function2 = EconomyFunction(name='Function 2', path='path/to/function2', parameters={'param2': 'value2'}, category=category2)
    function2.save()

    print("Sample data created successfully.")

if __name__ == '__main__':
    asyncio.run(create_sample_data())