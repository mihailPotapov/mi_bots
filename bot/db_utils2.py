import asyncpg

# Конфигурация подключения к базе данных
db_config = {
    "user": "postgres",
    "password": "123",
    "database": "bot_gpt",
    "host": "localhost",
}

async def get_db_pool():
    return await asyncpg.create_pool(**db_config)
# async def get_db_connection():
#     return await asyncpg.db_pool(dsn='dbname=bot_gpt user=postgres password=123 host=localhost')


# Функции для работы с базой данных
async def user_exists(nickname_user, db_pool):
    async with db_pool.acquire() as connection:
        user = await connection.fetchval("SELECT id FROM users WHERE nickname_user = $1", nickname_user)
        return user is not None

async def add_user_to_db(name_user, nickname_user, id_chat, db_pool):
    async with db_pool.acquire() as connection:
        await connection.execute("INSERT INTO users (name_user, nickname_user, id_chat) VALUES ($1, $2, $3)",
                                 name_user, nickname_user, id_chat)

async def set_user_role(chat_id, role_id, db_pool):
    async with db_pool.acquire() as connection:
        await connection.execute("UPDATE chat_roles SET id_roles = $1 WHERE id_chat = $2",
                                 role_id, chat_id)

async def get_current_role(chat_id, db_pool):
    async with db_pool.acquire() as connection:
        role_name = await connection.fetchval("SELECT r.name_roles FROM chat_roles cr JOIN roles r ON cr.id_roles = r.id_roles WHERE cr.id_chat = $1", chat_id)
        return role_name

async def update_chat_role(chat_id, role_id, db_pool):
    async with db_pool.acquire() as connection:
        # Проверяем, существует ли уже запись для данного чата
        row = await connection.fetchrow("SELECT id FROM chat_roles WHERE id_chat = $1", chat_id)
        if row:
            # Обновляем существующую запись
            await connection.execute("UPDATE chat_roles SET id_roles = $1 WHERE id_chat = $2", role_id, chat_id)
        else:
            # Создаем новую запись
            await connection.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES ($1, $2)", chat_id, role_id)


async def get_role_name(role_id, db_pool):
    async with db_pool.acquire() as connection:
        role_name = await connection.fetchval("SELECT name_roles FROM roles WHERE id_roles = $1", role_id)
    return role_name if role_name else None


async def get_user_tokens(chat_id, db_pool):
    async with db_pool.acquire() as connection:
        # Получаем id пользователя из таблицы users
        user_id = await connection.fetchval("SELECT id FROM users WHERE id_chat = $1", chat_id)
        if user_id is None:
            print("Пользователь не найден.")
            return 0  # Если пользователь не найден, возвращаем 0 токенов

        # Получаем количество токенов пользователя из таблицы tokens
        token_count = await connection.fetchval("SELECT token FROM tokens WHERE id_user = $1", user_id)
        if token_count is None:
            print("Запись о токенах пользователя не найдена.")
            return 0  # Если запись о токенах не найдена, возвращаем 0 токенов

    return token_count


async def update_user_tokens(chat_id, tokens_used, db_pool):
    async with db_pool.acquire() as conn:
        # Получаем id пользователя из таблицы users
        user_row = await conn.fetchrow("SELECT id FROM users WHERE id_chat = $1", chat_id)
        if user_row is None:
            print("Пользователь не найден.")
            return  # Если пользователь не найден, завершаем функцию

        user_id = user_row['id']

        # Получаем текущее количество токенов
        token_row = await conn.fetchrow("SELECT token FROM tokens WHERE id_user = $1", user_id)
        if token_row is None:
            print("Запись о токенах пользователя не найдена.")
            return  # Если запись о токенах не найдена, завершаем функцию

        current_tokens = token_row['token']

        # Вычитаем потраченные токены и обновляем баланс в базе данных
        # старный глюк место вычитание складывание и наобород
        # (предположение что в tokens_used сразу передают отрицательное значение)
        new_token_balance = current_tokens + tokens_used
        print(f"ОТЛАДКА- Текущее количество токенов:{new_token_balance}")
        await conn.execute("UPDATE tokens SET token = $1 WHERE id_user = $2", new_token_balance, user_id)


async def get_user_id_somehow(chat_id, db_pool):
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow("SELECT id FROM users WHERE id_chat = $1", chat_id)
        if result:
            return result['id']  # Возвращаем id пользователя из таблицы users
        else:
            return None  # Пользователь не найден
