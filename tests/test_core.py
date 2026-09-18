from pingvin.core import NetworkChecker, NetworkStatus
from unittest.mock import patch, MagicMock
import subprocess

def test_check_tcp_success():
    checker = NetworkChecker()
    with patch("socket.create_connection") as fake_connect:
        fake_connect.return_value.__enter__.return_value = MagicMock()
        result = checker.check_tcp("8.8.8.8", 53)

        assert result.available is True
        assert result.method == "tcp"
def test_check_tcp_failure():
    checker = NetworkChecker(timeout=1.0)
    with patch("socket.create_connection") as fake_connect:
        fake_connect.side_effect = OSError("Connection refused")
        result = checker.check_tcp("127.0.0.11", 53)

        assert result.available is False
        assert result.error is not None
        assert "Connection refused" in result.error


def test_check_ping_success():
    checker = NetworkChecker()
    with patch("subprocess.run") as fake_run:
        fake_run.return_value = MagicMock(returncode=0)
        result = checker.check_ping("8.8.8.8")

        assert isinstance(result, NetworkStatus)
        assert result.method == "ping"
        assert result.available is True
def test_check_ping_failure():
    checker = NetworkChecker()
    with patch("subprocess.run") as fake_run:
        fake_run.return_value = MagicMock(returncode=1)
        result = checker.check_ping("8.8.8.8")

        assert result.available is False
        assert result.error == "Return code: 1"


def test_check_ping_timeout():
    checker = NetworkChecker()
    with patch("subprocess.run") as fake_run:
        fake_run.side_effect = subprocess.TimeoutExpired(cmd="ping", timeout=3)
        result = checker.check_ping("8.8.8.8")

        assert result.available is False
        assert result.error is not None


def test_check_finds_connection_via_ping():
    checker = NetworkChecker()
    with patch.object(checker, "check_ping") as fake_ping:
        fake_ping.return_value = NetworkStatus(available=True, method="ping", latency_ms=10.0)
        result = checker.check()

        assert result.available is True
        assert result.method == "ping"

def test_check_falls_back_to_tcp():
    checker = NetworkChecker()
    with patch.object(checker, "check_ping") as fake_ping, \
         patch.object(checker, "check_tcp") as fake_tcp:
        fake_ping.return_value = NetworkStatus(available=False, method="ping", error="blocked")
        fake_tcp.return_value = NetworkStatus(available=True, method="tcp", latency_ms=20.0)
        result = checker.check()
        assert result.available is True
        assert result.method == "tcp"
        fake_tcp.assert_called_once()


def test_check_all_targets_fail():
    checker = NetworkChecker()
    with patch.object(checker, "check_ping") as fake_ping, \
         patch.object(checker, "check_tcp") as fake_tcp:
        fake_ping.return_value = NetworkStatus(available=False, method="ping", error="blocked")
        fake_tcp.return_value = NetworkStatus(available=False, method="tcp", error="refused")
        result = checker.check()
        assert result.available is False
        assert result.method == "all_failed"