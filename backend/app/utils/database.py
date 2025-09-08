from contextlib import asynccontextmanager
from typing import AsyncGenerator
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