# 这里用于存放配置相关的代码
from .config_manage import settings

# 通过 __init__.py 暴露 settings 对象，方便其他模块导入
__all__ = ['settings']