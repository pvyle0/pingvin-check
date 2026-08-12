from pingvin.core import NetworkChecker, NetworkStatus

def test_check_tcp_success():
    checker = NetworkChecker()
    result = checker.check_tcp("8.8.8.8", 53)
    assert result.available is True
    assert result.method == "tcp"

def test_check_tcp_failure():
    checker = NetworkChecker(timeout=1.0)
    result = checker.check_tcp("192.0.2.1", 53)
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