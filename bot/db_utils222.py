import aiopg

db_config = {
    'database': 'bot_gpt',  # Название базы данных
    'user': 'postgres',     # Имя пользователя
    'password': '123',      # Пароль
    'host': 'localhost'     # Хост
}


async def get_db_connection():
    dsn = 'dbname=bot_gpt user=postgres password=123 host=localhost'.format(**db_config)
    conn = await aiopg.connect(dsn)
    return conn


async def user_exists(nickname_user):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE nickname_user = %s", (nickname_user,))
            return await cursor.fetchone() is not None


async def add_user_to_db(name_user, nickname_user, id_chat):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO users (name_user, nickname_user, id_chat) VALUES (%s, %s, %s)",
                                 (name_user, nickname_user, id_chat))
            await conn.commit()


async def set_user_role(chat_id, role_id):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE chat_roles SET id_roles = %s WHERE id_chat = %s",
                                 (role_id, chat_id))
            await conn.commit()


async def get_role_name(role_id):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT name_roles FROM roles WHERE id_roles = %s", (role_id,))
            role_name = await cursor.fetchone()
            return role_name[0] if role_name else None


async def get_user_tokens(chat_id):
    async with aiopg.create_pool() as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Получаем id пользователя из таблицы users
                await cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
                user_row = await cursor.fetchone()
                if user_row is None:
                    print("Пользователь не найден.")
                    return 0  # Если пользователь не найден, возвращаем 0 токенов

                user_id = user_row[0]

                # Получаем количество токенов пользователя из таблицы tokens
                await cursor.execute("SELECT token FROM tokens WHERE id_user = %s", (user_id,))
                token_row = await cursor.fetchone()

                if token_row is None:
                    print("Запись о токенах пользователя не найдена.")
                    return 0  # Если запись о токенах не найдена, возвращаем 0 токенов

                return token_row[0]


async def get_current_role(chat_id):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT r.name_roles FROM chat_roles cr JOIN roles r ON cr.id_roles = r.id_roles WHERE cr.id_chat = %s", (chat_id,))
            role_name = await cursor.fetchone()
            return role_name[0] if role_name else None


async def update_chat_role(chat_id, role_id):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("SELECT id FROM chat_roles WHERE id_chat = %s", (chat_id,))
                if await cursor.fetchone():
                    await cursor.execute("UPDATE chat_roles SET id_roles = %s WHERE id_chat = %s", (role_id, chat_id))
                else:
                    await cursor.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES (%s, %s)", (chat_id, role_id))
                await conn.commit()
            except Exception as e:
                print(f"Error: {e}")


async def update_user_tokens(chat_id, tokens_used):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            # Получаем id пользователя из таблицы users
            await cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
            user_row = await cursor.fetchone()
            if user_row is None:
                print("Пользователь не найден.")
                return  # Если пользователь не найден, завершаем функцию

            user_id = user_row[0]

            # Получаем текущее количество токенов
            await cursor.execute("SELECT token FROM tokens WHERE id_user = %s", (user_id,))
            token_row = await cursor.fetchone()
            if token_row is None:
                print("Запись о токенах пользователя не найдена.")
                return  # Если запись о токенах не найдена, завершаем функцию

            current_tokens = token_row[0]

            # Вычитаем потраченные токены и обновляем баланс в базе данных
            new_token_balance = current_tokens - tokens_used
            await cursor.execute("UPDATE tokens SET token = %s WHERE id_user = %s", (new_token_balance, user_id))
            await conn.commit()


async def update_user_tokens(chat_id, tokens_used):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE tokens SET token = token - %s FROM users WHERE tokens.id_user = users.id AND users.id_chat = %s", (tokens_used, chat_id))
            await conn.commit()


async def get_user_id_somehow(chat_id):
    async with await get_db_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
            result = await cursor.fetchone()
            return result[0] if result else None