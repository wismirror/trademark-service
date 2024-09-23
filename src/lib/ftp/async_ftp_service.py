import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from ftplib import FTP
from zipfile import ZipFile

from src.lib.ftp.ftp_service import FTPService


class AsyncFTPService:
    """Service to handle FTP service functions in the asynchronous way"""

    EXECUTOR = ThreadPoolExecutor(max_workers=1)

    def __init__(self, ftp_client: FTP, root_folder: str) -> None:
        """Defines FTP service"""

        self.ftp_service = FTPService(ftp_client=ftp_client, root_folder=root_folder)

    async def get_file_names(self, *args, **kwargs) -> list[str]:
        """Async cover on function get_file_names from FTPService"""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor=self.EXECUTOR,
            func=functools.partial(
                self.ftp_service.get_file_names,
                *args,
                **kwargs
            )
        )

    async def get_zip_data(self, *args, **kwargs) -> ZipFile:
        """Async cover on function get_zip_data from FTPService"""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor=self.EXECUTOR,
            func=functools.partial(
                self.ftp_service.get_zip_data,
                *args,
                **kwargs
            )
        )
