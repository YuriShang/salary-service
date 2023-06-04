from datetime import datetime
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound
from salary_service.db.database import engine
from salary_service.db.models import users_table, salaries_table
from salary_service.schemas.schemas import UserCreate, LoggedInUser, RegisteredUser, TokenSchema, SalaryData
from salary_service.utils.utils import get_hashed_password, verify_password, create_access_token, get_current_user

app = FastAPI()


# Регистрация нового пользователя
@app.post('/signup', summary="Create new user", response_model=RegisteredUser)
async def create_user(data: UserCreate):
    async with engine.begin() as conn:
        try:
            username = await conn.execute(select(users_table.c.username).where(users_table.c.username == data.username))
            username = username.scalar_one()
        except NoResultFound:
            # В данном случае обработка исключения не требуется,
            pass

        if username == data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exist"
            )
    user = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'username': data.username,
        'password': get_hashed_password(data.password),
    }
    async with engine.begin() as conn:
        await conn.execute(insert(users_table).values(**user))
        await conn.execute(insert(salaries_table).values(username=data.username))
    return user


# Авторизация
@app.post('/login', summary="Create access token for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with engine.begin() as conn:
        try:
            username = await conn.execute(
                select(users_table.c.username).where(users_table.c.username == form_data.username))
            username = username.scalar_one()
        except NoResultFound:
            # В данном случае обработка исключения не требуется
            pass

        if username != form_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect login or password"
            )

        # Верифицируем ранее захэшированный пароль
        hashed_pass = await conn.execute(
            select(users_table.c.password).where(users_table.c.username == form_data.username))
        password = verify_password(form_data.password, hashed_pass.scalar_one())
        if not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect login or password"
            )

    token = {
        "access_token": create_access_token(username),
    }
    return token


@app.post('/set_salary_info', summary="Set salary for user", response_model=SalaryData)
async def set_salary_info(data: SalaryData):
    username = data.username
    salary = data.salary
    async with engine.begin() as conn:
        await conn.execute(update(salaries_table).where(
            salaries_table.c.username == username).values(salary=salary,
                                                          next_increase_date=data.next_increase_date))
    return data


# Получаем инфу о зп и дате следующего повышения.
# Защищенный маршрут, доступен только авторизованным пользователям.
@app.get('/get_salary', summary="Get salary info of currently logged in user", response_model=SalaryData)
async def get_salary(user_data: LoggedInUser = Depends(get_current_user)):
    username = user_data["username"]
    async with engine.begin() as conn:
        salary_data = await conn.execute(select(salaries_table.c.salary, salaries_table.c.next_increase_date).where(
            salaries_table.c.username == username))
        salary, next_increase_date = salary_data.fetchall()[0]

    data = {
        "username": username,
        "salary": salary,
        "next_increase_date": next_increase_date
    }
    return data
