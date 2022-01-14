import databases
import sqlalchemy
import ormar
import datetime
from typing import Optional
import config

database = databases.Database(config.database_url)
metadata = sqlalchemy.MetaData()



class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Image(ormar.Model):
    class Meta(BaseMeta):
        tablename = "images"

    id: int = ormar.Integer(primary_key=True)
    url: str = ormar.Text()
    hash: bytes = ormar.LargeBinary(max_length=10000000)


async def init_database():
    engine = sqlalchemy.create_engine(config.database_url)
    metadata.drop_all(engine)
    metadata.create_all(engine)
