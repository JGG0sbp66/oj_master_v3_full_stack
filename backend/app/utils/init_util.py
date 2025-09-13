from app.utils.db_util import AsyncDatabase
from app.core.config import settings
from app.utils.logger_util import init_logger
import logging
from typing import Dict

class InitUtils:
    """工具类初始化管理"""

    def __init__(self):
        """初始化异步数据库实例"""
        self.db_instance: AsyncDatabase | None = None
        self.loggers: Dict[str, logging.Logger] = {}
    
    async def initialize(self):
        """异步初始化所有组件"""
        await self.init_loggers()
        await self.init_database()
    
    async def dispose(self):
        """异步释放所有组件"""
        if self.db_instance:
            await self.db_instance.dispose()

    async def init_loggers(self):
        """初始化所有 logger"""
        self.loggers['utils'] = init_logger('utils', 'utils.log', logging.INFO, is_console=True)

    async def init_database(self):
        """初始化数据库连接"""
        db_url = f"postgresql+psycopg_async://{settings.database.user}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.db}"
        self.db_instance = AsyncDatabase(db_url, self.loggers['utils'])


# 全局初始化实例
init_utils = InitUtils()
