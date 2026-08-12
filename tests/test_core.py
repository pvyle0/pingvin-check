from pingvin.core import NetworkChecker, NetworkStatus
from unittest.mock import patch, MagicMock

def test_check_tcp_success():
    checker = NetworkChecker()
    with patch("socket.create_connection") as fake_connect:
        fake_connect.return_value.__enter__.return_value = MagicMock()
        result = checker.check_tcp("8.8.8.8", 53)

        assert result.available is True
        assert result.method == "tcp"
# \\ сделал мок версию можно потом остальное тоже так сделать

def test_check_tcp_failure():
    checker = NetworkChecker(timeout=1.0)
    result = checker.check_tcp("127.0.0.11", 53) # 100.64.0.1
    assert result.available is False
    assert result.error is not None

def test_check_ping_returns_status():
    checker = NetworkChecker()
    result = checker.check_ping("8.8.8.8")
    assert isinstance(result, NetworkStatus)
    assert result.method == "ping"

def test_check_finds_connection():
    checker = NetworkChecker()
    result = checker.check()
    assert result.available is True