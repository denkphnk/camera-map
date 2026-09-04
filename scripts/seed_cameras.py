import os
import asyncio
import random
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from src.data.models.camera_model import DCamera

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL') 

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

STREETS = ["Ленина", "Мира", "Гагарина", "Пушкина", "Советская", "Лесная", "Новая", "Центральная"]
MODELS = ["Hikvision DS-2CD2043", "Dahua IPC-HFW1230", "Axis M3046", "Bosch NIN-51022"]
TYPES = ["IP", "AHD", "HD-SDI"]
CLASSES = ["Outdoor", "Indoor", "PTZ", "Dome"]

def generate_camera(index: int) -> dict:
    street = random.choice(STREETS)
    building = random.randint(1, 150)
    
    return {
        "camera_id": f"{index:05d}",
        "camera_name": f"Камера {street}, д. {building}",
        "camera_place": f"г. Москва, ул. {street}, д. {building}",
        "camera_latitude": random.uniform(55.60, 55.95),
        "camera_longitude": random.uniform(37.30, 37.90),
        "camera_type": random.choice(TYPES),
        "camera_type_cd": random.randint(1, 3),
        "camera_class": random.choice(CLASSES),
        "camera_class_cd": random.randint(1, 5),
        "camera_place_cd": random.randint(1, 100),
        "model": random.choice(MODELS),
        "serial_number": f"SN-{random.randint(100000, 999999)}",
        "azimuth": random.randint(0, 360),
        "archive": 0,
    }

async def seed_cameras(count: int = 100):
    async with async_session() as session:
        await session.execute(text("TRUNCATE TABLE d_camera CASCADE"))
        
        cameras = [DCamera(**generate_camera(i)) for i in range(1, count + 1)]
        session.add_all(cameras)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_cameras(100))