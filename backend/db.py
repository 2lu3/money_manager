import asyncio 
import asyncpg
from config import Settings

class DB:
    async def __init__(self):
        self.settings = Settings()
        self.conn = await asyncpg.connect(
            user=self.settings.supabase_user,
            password=self.settings.supabase_password,
            database=self.settings.supabase_database,
            host=self.settings.supabase_host,
            port=self.settings.supabase_port
        )