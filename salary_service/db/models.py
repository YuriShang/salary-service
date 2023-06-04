from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import MetaData

# Метаданные
metadata = MetaData()

# Модель таблицы пользователей
users_table = Table('users_data', metadata,
                    Column('user_id', Integer, unique=True, primary_key=True, autoincrement=True),
                    Column('first_name', String(length=255), nullable=False),
                    Column('last_name', String(length=255), nullable=False),
                    Column('username', String(length=255), unique=True, nullable=False),
                    Column('password', String(length=255), nullable=False),
                    )

# Модель таблицы зарплат
salaries_table = Table('salaries_data', metadata,
                       Column('user_id', Integer, ForeignKey("users_data.user_id", ondelete="CASCADE"),
                              primary_key=True, unique=True, nullable=False, autoincrement=True),
                       Column('username', String(length=255), unique=True, nullable=False),
                       Column('salary', Integer),
                       Column('next_increase_date', DateTime),
                       )
