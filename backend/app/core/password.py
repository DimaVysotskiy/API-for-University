import bcrypt

async def hash_password(password: str) -> str:
    """
    Создает криптографический хеш для пароля.
    
    Аргумент:
        password (str): Пароль, который нужно хешировать.
        
    Возвращает:
        bytes: Байтовая строка с хешем, готовым для хранения в БД.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

async def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введенный пароль сохраненному хешу.
    
    Аргументы:
        password (str): Пароль, введенный пользователем при входе.
        hashed_password (str): Хеш пароля в виде строки, извлеченный из БД.
        
    Возвращает:
        bool: True, если пароли совпадают, иначе False.
    """
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)