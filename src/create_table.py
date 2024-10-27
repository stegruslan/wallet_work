from database import Base, engine, session_factory
from models import *


# Создание сессии базы данных
with session_factory() as session:
    # Создание всех таблиц, определенных в моделях,
    # и привязка их к механизму (engine) базы данных.
    Base.metadata.create_all(bind=engine)
    # Коммит изменений в сессию базы данных.
    session.commit()
