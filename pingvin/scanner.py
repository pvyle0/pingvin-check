from pingvin.core import NetworkChecker
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
}
class PortScanner:
    def __init__(self, timeout: float = 1.0):
        self.checker = NetworkChecker(timeout=timeout)

    def scan(self, host, start_port, end_port, max_workers=50):
        results = []
        ports = range(start_port, end_port + 1)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.checker.check_tcp, host, port): port for port in ports}
            for future in futures:
                result = future.result()
                if result.available:
                    results.append(result)
        return results