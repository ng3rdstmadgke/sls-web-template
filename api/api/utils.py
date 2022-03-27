import time

class Utils:
    @staticmethod
    def get_ttl_hash(seconds: int = 3600) -> int:
        """Return the same value withing `seconds` time period"""
        return round(time.time() / seconds)