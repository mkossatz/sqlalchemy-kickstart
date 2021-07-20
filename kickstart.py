from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


class PostgresDB:

    Base = declarative_base()

    def __init__(
            self, host: str, port: str, username: str, password: str, database: str):
        self._engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
            username, password, host, port, database))
        self._Session = sessionmaker(bind=self._engine)

    @contextmanager
    def session_scope(self):
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def setup_database_tables(self):
        PostgresDB.Base.metadata.drop_all(self._engine)
        PostgresDB.Base.metadata.create_all(self._engine)


class UserEntry(PostgresDB.Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


class UsersRepository():

    def __init__(self, postgres_db: PostgresDB):
        self._postgres_db = postgres_db

    def add_user(self, name: str, age: str):
        with self._postgres_db.session_scope() as session:
            user_entry = UserEntry(name=name, age=age)
            session.add(user_entry)
