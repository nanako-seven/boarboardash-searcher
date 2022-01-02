import asyncio
from models import init_database

if __name__ == '__main__':
    asyncio.run(init_database())
