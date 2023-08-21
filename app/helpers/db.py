from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.engine.base import Connection

from app.db.base import get_session


def check_database_connect(connection: Connection = Depends(get_session)):
    is_database_connect = True
    output = 'Connect Database is ok'
    try:
        connection.execute(text('SELECT 1'))  # to check database we will execute raw query
    except Exception as e:
        output = str(e)
        is_database_connect = False
    return is_database_connect, output
