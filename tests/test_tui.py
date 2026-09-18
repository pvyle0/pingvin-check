import pytest
from unittest.mock import patch
from pingvin.tui import PingvinApp
from pingvin.core import NetworkStatus

@pytest.mark.asyncio
async def test_run_checks_populates_table():
    app = PingvinApp()
    with patch("pingvin.tui.NetworkChecker") as MockChecker:
        instance = MockChecker.return_value
        instance.check_ping.return_value = NetworkStatus(available=True, method="ping", latency_ms=15.0)
        instance.check_tcp.return_value = NetworkStatus(available=True, method="tcp", latency_ms=20.0)

        async with app.run_test() as pilot:
            target_input = app.query_one("#target-input")
            target_input.value = "example.com"
            await pilot.press("enter")
            await pilot.pause()
            table = app.query_one("#results-table")
            assert table.row_count == 4  #пинг и еще 3 порта


@pytest.mark.asyncio
async def test_portscan_invalid_range_shows_error():
    app = PingvinApp()
    async with app.run_test() as pilot:
        target_input = app.query_one("#target-input")
        target_input.value = "example.com"
        scan_input = app.query_one("#portscan-input")
        scan_input.value = "not-a-range"
        scan_input.focus()

        await pilot.press("enter")
        await pilot.pause()
        status = app.query_one("#result-status")
        assert "Invalid port range" in str(status.render())