from ftplib import FTP


class FTPClient:
    """Context manager class for FTP protocol client"""

    def __init__(self, host: str, username: str, password: str) -> None:
        """Creates connection to the FTP server with passed host, username, password"""

        self.ftp_client = FTP(host)
        self.ftp_client.login(
            user=username,
            passwd=password
        )

    def __enter__(self) -> FTP:
        """Returns FTP connection"""

        return self.ftp_client

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection with FTP server"""

        self.ftp_client.quit()
