import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Button, Static, Input, DataTable
from textual.binding import Binding
from pingvin.core import NetworkChecker
from pingvin.scanner import PortScanner

class PingvinApp(App):
    CSS = """
    #target-input {
        margin: 1;
    }
    DataTable {
        height: 1fr;
        margin: 1;
    }
    #result-status {
        height: auto;
        padding: 1;
        margin: 1;
        border: solid $accent;
    }
    """
    BINDINGS = [
        Binding("ctrl+r", "run_checks", "Run Checks", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+s", "run_portscan", "Port Scan", show=True),
    ]
    TITLE = "Pingvin-Check"
    SUB_TITLE = "Network Connectivity Monitor"
    PORTS_TO_CHECK = [(22, "SSH"), (80, "HTTP"), (443, "HTTPS")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter target host (e.g. example.com)", id="target-input")
        yield DataTable(id="results-table")
        yield Input(placeholder="Port range, e.g. 1-1024", id="portscan-input")
        yield DataTable(id="portscan-table")
        yield Static("Status: —", id="result-status")
        yield Footer()


    def on_mount(self):
        table = self.query_one("#results-table", DataTable)
        table.add_columns("Check", "Status", "Latency")
        
        scan_table = self.query_one("#portscan-table", DataTable)
        scan_table.add_columns("Port", "Status", "Latency")
        
    def on_button_pressed(self, event):
        pass

    def on_input_submitted(self, event):
        if event.input.id == "target-input":
            self.run_worker(self.action_run_checks())
        elif event.input.id == "portscan-input":
            self.run_worker(self.action_run_portscan())

    async def action_run_checks(self):
        target_input = self.query_one("#target-input", Input)
        target = target_input.value.strip()
        if not target:
            return
        table = self.query_one("#results-table", DataTable)
        table.clear()
        checker = NetworkChecker()
        results = []

        # \\ ICMP ping
        ping_result = await asyncio.to_thread(checker.check_ping, target)
        status_icon = "[green]✓[/green]" if ping_result.available else "[red]✗[/red]"
        latency = f"{ping_result.latency_ms:.1f} ms" if ping_result.available else "timeout"
        table.add_row("ICMP Ping", status_icon, latency)
        results.append(ping_result.available)


        # \\ TCP
        for port, name in self.PORTS_TO_CHECK:
            port_result = await asyncio.to_thread(checker.check_tcp, target, port)
            status_icon = "[green]✓[/green]" if port_result.available else "[red]✗[/red]"
            latency = f"{port_result.latency_ms:.1f} ms" if port_result.available else "timeout"
            table.add_row(f"Port {port} ({name})", status_icon, latency)
            results.append(port_result.available)

    async def action_run_portscan(self):
        range_input = self.query_one("#portscan-input", Input)
        range_text = range_input.value.strip()
        status_widget = self.query_one("#result-status", Static)

        if not range_text or "-" not in range_text:
            status_widget.update("Status: [red]Invalid port range (use format: 20-25)[/red]")
            return
        start_str, end_str = range_text.split("-")
        start_port = int(start_str)
        end_port = int(end_str)

        target_input = self.query_one("#target-input", Input)
        target = target_input.value.strip()
        if not target:
            return


        scan_table = self.query_one("#portscan-table", DataTable)
        scan_table.clear()
        scanner = PortScanner()
        results = await asyncio.to_thread(scanner.scan, target, start_port, end_port)
        for result in results:
            scan_table.add_row(result.host, "[green]✓[/green]", f"{result.latency_ms:.1f} ms")

        status_widget = self.query_one("#result-status", Static)
        if results:
            status_widget.update(f"Status: [green]Found {len(results)} open port(s)[/green]")
        else:
            status_widget.update("Status: [yellow]No open ports found in range[/yellow]")
if __name__ == "__main__":
    app = PingvinApp()
    app.run()