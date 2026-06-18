from datetime import datetime
import platform
import socket
import psutil

class SystemTool:

    @staticmethod
    def current_time():

        return datetime.now().strftime(
            "%I:%M:%S %p"
        )

    @staticmethod
    def current_date():

        return datetime.now().strftime(
            "%Y-%m-%d"
        )

    @staticmethod
    def hostname():

        return socket.gethostname()

    @staticmethod
    def os_info():

        return platform.platform()

    @staticmethod
    def cpu_usage():

        return psutil.cpu_percent()

    @staticmethod
    def ram_usage():

        return psutil.virtual_memory().percent