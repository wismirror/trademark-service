from typing import Callable, Any, Awaitable
from zipfile import ZipFile

import xmltodict

from src.lib.ftp.async_ftp_service import AsyncFTPService
from src.lib.ftp.utils import rename_dict_fields
from src.lib.ftp.ftp_client import FTPClient


async def parse_trade_marks_from_zip(
    zip_file: ZipFile,
    save_trade_mark_method: Callable[[dict], Awaitable[Any]]
) -> None:
    """Handles zip file and save trade mark data from .xml file into database"""

    for file_name in zip_file.namelist():
        if not file_name.endswith('.xml'):
            continue
        file_data = xmltodict.parse(zip_file.read(file_name))
        transaction_data = file_data.get('Transaction', {})
        if transaction_data \
                .get('TradeMarkTransactionBody', {}) \
                .get('TransactionContentDetails', {}) \
                .get('TransactionData', {}) \
                .get('TradeMarkDetails', {}) \
                .get('TradeMark', {}) \
                .get('MarkFeature') == 'Word':
            await save_trade_mark_method(rename_dict_fields(
                data=transaction_data,
                regex_expression='@|#|:'
            ))


async def parse_ftp_server(
    ftp_host: str,
    ftp_username: str,
    ftp_password: str,
    ftp_root_folder: str,
    save_trade_mark_method: Callable[[dict], Awaitable[Any]],
    is_file_parsed_method: Callable[[str], Awaitable[bool]],
    save_parsed_file_method: Callable[[str], Awaitable[Any]],
    update_parsed_file_method: Callable[[str], Awaitable[Any]]
) -> None:
    """Parses trade marks data from FTP server"""

    with FTPClient(host=ftp_host, username=ftp_username, password=ftp_password) as ftp_client:
        ftp_service = AsyncFTPService(ftp_client=ftp_client, root_folder=ftp_root_folder)
        for file_name in await ftp_service.get_file_names(
            file_extension='.zip'
        ):
            if await is_file_parsed_method(file_name):
                continue
            await save_parsed_file_method(file_name)
            zip_file = await ftp_service.get_zip_data(file_name=file_name)
            await parse_trade_marks_from_zip(
                zip_file=zip_file,
                save_trade_mark_method=save_trade_mark_method
            )
            await update_parsed_file_method(file_name)
