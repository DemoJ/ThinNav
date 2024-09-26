from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
# from backend.app.models import Base  # 测试环境
from app.models import Base  # 正式环境

# 获取 Alembic 配置
config = context.config

# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 获取模型元数据
target_metadata = Base.metadata

# 获取数据库 URL
db_url = config.get_main_option("sqlalchemy.url")
db_path = None

# 如果是 SQLite 数据库，获取数据库文件路径
if db_url.startswith("sqlite:///"):
    db_path = db_url.replace("sqlite:///", "")

# 离线模式迁移
def run_migrations_offline() -> None:
    """在 'offline' 模式下运行迁移."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# 在线模式迁移
def run_migrations_online() -> None:
    """在 'online' 模式下运行迁移."""

    # 检查并创建 SQLite 数据库文件及其父目录
    if db_path and not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在，正在创建...")
        # 创建父目录
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # 创建数据库文件
        open(db_path, 'w').close()

    # 创建数据库引擎
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# 判断是否为离线模式
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
