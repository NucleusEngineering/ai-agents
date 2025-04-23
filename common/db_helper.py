# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
import logging

def init_db():
    dbConnection = "dbname='"+os.environ.get("DB_DATABASE", "ai_agent")+"' user='"+os.environ.get("DB_USER", "postgres")+"' host='"+os.environ.get("DB_HOST", "localhost")+"' password='"+os.environ.get("DB_PASSWORD", "postgres")+"'"

    # pool define with 10 live connections
    connection_pool = SimpleConnectionPool(1,10,dsn=dbConnection)
    return connection_pool

@contextmanager
def getcursor(connection_pool):
    con = connection_pool.getconn()
    try:
        yield con.cursor(cursor_factory=RealDictCursor)
    finally:
        connection_pool.putconn(con)

def commit(connection_pool):
    con = connection_pool.getconn()
    try:
        con.commit()
    except Exception as e:
        logging.error("Cannot commit a transacation! Exception: %s", e)
