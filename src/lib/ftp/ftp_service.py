from ftplib import FTP, error_perm
from io import BytesIO
from zipfile import ZipFile


class FTPService:
    """Service to handle FTP connection function"""

    def __init__(self, ftp_client: FTP, root_folder: str) -> None:
        """Defines FTP client and goes to root_folder"""

        self.ftp_client = ftp_client
        self.root_folder = root_folder
        self.ftp_client.cwd(self.root_folder)

    def get_file_names(self, folder_name: str = None, file_extension: str = '') -> list[str]:
        """Returns all files or files with defined extension from root folder or provided folder"""

        try:
            files = self.ftp_client.nlst(folder_name or '')
        except error_perm as resp:
            if str(resp) == "550 No files found":
                files = []
            else:
                raise resp
        files = filter(lambda folder_item: folder_item.endswith(file_extension), files)
        return list(files)

    def get_zip_data(self, file_name: str) -> ZipFile:
        """Returns ZipFile object with data from provided file"""

        buffer = BytesIO()
        self.ftp_client.retrbinary(f'RETR {file_name}', buffer.write)
        buffer.seek(0)
        return ZipFile(buffer)
