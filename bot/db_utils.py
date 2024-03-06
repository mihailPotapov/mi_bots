import psycopg2
# Конфигурация подключения к базе данных
db_config = {
    "host": "localhost",
    "database": "bot_gpt",
    "user": "postgres",
    "password": "123"
}


# Функции для работы с базой данных
def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn


def user_exists(nickname_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE nickname_user = %s", (nickname_user,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None


def add_user_to_db(name_user, nickname_user, id_chat):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name_user, nickname_user, id_chat) VALUES (%s, %s, %s)",
                   (name_user, nickname_user, id_chat))
    conn.commit()
    cursor.close()
    conn.close()


def set_user_role(chat_id, role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE chat_roles SET id_roles = %s WHERE id_chat = %s",
                   (role_id, chat_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_current_role(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT r.name_roles FROM chat_roles cr JOIN roles r ON cr.id_roles = r.id_roles WHERE cr.id_chat = %s", (chat_id,))
    role_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return role_name[0] if role_name else None


def update_chat_role(chat_id, role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Проверяем, существует ли уже запись для данного чата
        cursor.execute("SELECT id FROM chat_roles WHERE id_chat = %s", (chat_id,))
        if cursor.fetchone():
            # Обновляем существующую запись
            cursor.execute("UPDATE chat_roles SET id_roles = %s WHERE id_chat = %s", (role_id, chat_id))
        else:
            # Создаем новую запись
            cursor.execute("INSERT INTO chat_roles (id_chat, id_roles) VALUES (%s, %s)", (chat_id, role_id))

        conn.commit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()


def get_role_name(role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_roles FROM roles WHERE id_roles = %s", (role_id,))
    role_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return role_name[0] if role_name else None

# //////////
def get_user_tokens(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Получаем id пользователя из таблицы users
    cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
    user_row = cursor.fetchone()
    if user_row is None:
        print("Пользователь не найден.")
        return 0  # Если пользователь не найден, возвращаем 0 токенов

    user_id = user_row[0]

    # Получаем количество токенов пользователя из таблицы tokens
    cursor.execute("SELECT token FROM tokens WHERE id_user = %s", (user_id,))
    token_row = cursor.fetchone()
    cursor.close()
    conn.close()

    if token_row is None:
        print("Запись о токенах пользователя не найдена.")
        return 0  # Если запись о токенах не найдена, возвращаем 0 токенов

    return token_row[0]


def update_user_tokens(chat_id, tokens_used):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Получаем id пользователя из таблицы users
    cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
    user_row = cursor.fetchone()
    if user_row is None:
        print("Пользователь не найден.")
        cursor.close()
        conn.close()
        return  # Если пользователь не найден, завершаем функцию

    user_id = user_row[0]

    # Получаем текущее количество токенов
    cursor.execute("SELECT token FROM tokens WHERE id_user = %s", (user_id,))
    token_row = cursor.fetchone()
    if token_row is None:
        print("Запись о токенах пользователя не найдена.")
        cursor.close()
        conn.close()
        return  # Если запись о токенах не найдена, завершаем функцию

    current_tokens = token_row[0]

    # Вычитаем потраченные токены и обновляем баланс в базе данных
    new_token_balance = current_tokens - tokens_used
    cursor.execute("UPDATE tokens SET token = %s WHERE id_user = %s", (new_token_balance, user_id))
    conn.commit()

    cursor.close()
    conn.close()


def get_user_id_somehow(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id_chat = %s", (chat_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]  # Возвращаем id пользователя из таблицы users
    else:
        return None  # Пользователь не найден

