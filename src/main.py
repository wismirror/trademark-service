from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from src.core.settings import local as settings
from src.db import db
from src.lib.ftp.ftp_parser import parse_ftp_server
from src.routers import router

app = FastAPI()
app.include_router(router=router)


@app.on_event("startup")
async def startup():
    await db.connect_to_database(connection_string=settings.MONGO_CONNECTION_STRING)
    await db.init_indexes()
    await db.delete_unparsed_files()


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


scheduler = AsyncIOScheduler()
scheduler.add_job(
    func=parse_ftp_server,
    trigger='interval',
    minutes=1,
    kwargs={
        'ftp_host': settings.FTP_HOST,
        'ftp_username': settings.FTP_USERNAME,
        'ftp_password': settings.FTP_PASSWORD,
        'ftp_root_folder': settings.FTP_ROOT_FOLDER,
        'save_trade_mark_method': db.save_trade_mark,
        'is_file_parsed_method': db.is_file_parsed,
        'save_parsed_file_method': db.save_parsed_file,
        'update_parsed_file_method': db.update_parsed_file
    }
)
scheduler.start()
