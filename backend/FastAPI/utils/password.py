import bcrypt

async def hash_password(password: str) -> str:
    """
    Создает криптографический хеш для пароля.
    
    Аргумент:
        password (str): Пароль, который нужно хешировать.
        
    Возвращает:
        bytes: Байтовая строка с хешем, готовым для хранения в БД.
    """
    # 1. Преобразуем строку пароля в байты
    password_bytes = password.encode('utf-8')
    
    # 2. Генерируем "соль" (salt) - случайную строку, которая делает хеш уникальным
    salt = bcrypt.gensalt()
    
    # 3. Хешируем пароль, используя соль
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    return hashed_password.decode('utf-8')

async def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введенный пароль сохраненному хешу.
    
    Аргументы:
        password (str): Пароль, введенный пользователем при входе.
        hashed_password (bytes): Хеш пароля, извлеченный из БД.
        
    Возвращает:
        bool: True, если пароли совпадают, иначе False.
    """
    # Преобразуем введенный пароль в байты
    password_bytes = password.encode('utf-8')
    
    # bcrypt автоматически извлекает соль из хеша и сравнивает его
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))