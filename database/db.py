import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://root:password@localhost/dev_db'

if os.environ.get('SQL_DEBUG'):
    os.makedirs('logs', exist_ok=True)
    sql_handler = logging.FileHandler('logs/sql.log', mode='w')
    sql_handler.setFormatter(logging.Formatter('\n%(asctime)s\n%(message)s'))
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(sql_handler)

db_engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

session = SessionLocal()
