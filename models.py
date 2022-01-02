import databases
import sqlalchemy
import ormar
import datetime
from typing import Optional
import config

database = databases.Database(config.database_url)
metadata = sqlalchemy.MetaData()


# note that this step is optional -> all ormar cares is a internal
# class with name Meta and proper parameters, but this way you do not
# have to repeat the same parameters if you use only one database
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
    # create the database
    # note that in production you should use migrations
    # note that this is not required if you connect to existing database
    engine = sqlalchemy.create_engine(config.database_url)
    # just to be sure we clear the db before
    metadata.drop_all(engine)
    metadata.create_all(engine)
