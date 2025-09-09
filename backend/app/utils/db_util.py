from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings


class AsyncDatabase:
    """异步数据库连接工具类"""

    def __init__(self, db_url: str):
        """
        初始化数据库连接

        Args:
            db_url (str): 数据库连接字符串, 
                          传入格式为 "postgresql+psycopg_async://user:password@host:port/dbname"
        """

        # 创建异步数据库引擎
        self.engine = create_async_engine(
            db_url,
            echo=settings.database.echo,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_timeout=settings.database.pool_timeout,
            pool_recycle=settings.database.pool_recycle,
            pool_pre_ping=settings.database.pool_pre_ping,
        )

        # 创建会话工厂
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,       # 使用异步会话
            expire_on_commit=False,    # 提交后实例不过期
            autoflush=False,           # 关闭自动刷新
            autocommit=False           # 关闭自动提交
        )
    
    @asynccontextmanager
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """
        异步上下文管理器, 提供数据库会话
        """
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()    # 正常提交事务
            except Exception:
                await session.rollback()  # 异常回滚事务
                raise

# 全局变量, 初始化延迟
# TODO 考虑单独建立一个地方用于各种工具的初始化
db_instance: Optional[AsyncDatabase] = None

def init_database() -> AsyncDatabase:
    """初始化数据库连接, 在应用启动时调用"""
    global db_instance
    if db_instance is None:
        db_url = f"postgresql+psycopg_async://{settings.database.user}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.db}"
        db_instance = AsyncDatabase(db_url)

    return db_instance

def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    return db_instance.get_db()
