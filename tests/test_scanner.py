from pingvin.scanner import PortScanner
from pingvin.core import NetworkStatus
from unittest.mock import patch

def test_scan_open():
    scanner = PortScanner()
    with patch.object(scanner.checker, "check_tcp") as fake_check:
        def side_effect(host, port):
            available = port == 80
            return NetworkStatus(available=available, method="tcp", host=f"{host}:{port}")
        fake_check.side_effect = side_effect
        results = scanner.scan("example.com", 79, 81)

        assert len(results) == 1
        assert results[0].host == "example.com:80"


def test_scan_emp_ran_returns_emp_list():
    scanner = PortScanner()
    with patch.object(scanner.checker, "check_tcp") as fake_check:
        fake_check.return_value = NetworkStatus(available=False, method="tcp")
        results = scanner.scan("example.com", 1, 5)
        assert results == []