from dataclasses import dataclass
from typing import Optional
import socket
import time
import subprocess
import platform

@dataclass
class NetworkStatus:
    available: bool
    method: str
    latency_ms: Optional[float] = None
    host: Optional[str] = None
    error: Optional[str] = None


class NetworkChecker:
    DEFAULT_TARGETS = [
        ("8.8.8.8", 53),
        ("1.1.1.1", 53),
    ]
    def __init__(self, timeout: float = 2.0):
        self.timeout = timeout

    def check_tcp(self, host: str, port: int) -> NetworkStatus:
        start = time.time()
        try:
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                elapsed = (time.time() - start) * 1000
            return NetworkStatus(available=True, method="tcp", latency_ms=elapsed, host=f"{host}:{port}")
        except Exception as err:
            return NetworkStatus(available=False, method="tcp", host=f"{host}:{port}", error=str(err))
        
    def check_ping(self, host: str = "8.8.8.8") -> NetworkStatus:
        start = time.time()

        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "2000", host]
            else:
                cmd = ["ping", "-c", "1", "-W", "2", host]
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout + 1
        )
            if result.returncode == 0:
                elapsed = (time.time() - start) * 1000
                return NetworkStatus(available=True, method="ping", latency_ms=elapsed, host=host)
            else:
                return NetworkStatus(available=False, method="ping", host=host, error=f"Return code: {result.returncode}")
        except Exception as err:
            return NetworkStatus(available=False, method="ping", host=host, error=str(err))
        
    def check(self) -> NetworkStatus:
        result = self.check_ping()
        if result.available:
            return result
        for host, port in self.DEFAULT_TARGETS:
            result = self.check_tcp(host, port)
            if result.available:
                return result
        return NetworkStatus(available=False, method="all_failed", error="All checks failed")
    