from pingvin.core import NetworkChecker
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

    def scan(self, host, start_port, end_port):
        results = []
        for port in range(start_port, end_port + 1):
            result = self.checker.check_tcp(host, port)
            if result.available:
                results.append(result)
        return results