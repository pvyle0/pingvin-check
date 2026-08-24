import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Button, Static
from textual.binding import Binding

from pingvin.core import NetworkChecker
class StatusDisplay(Static):
    pass
    
class PingvinApp(App):
    CSS = """
    #status-box {
        height: auto;
        padding: 2;
        border: solid $accent;
        margin: 1;
    }
    """
    BINDINGS = [
        Binding("ctrl+r", "run_check", "Check now", show=True)
    ]
    TITLE = "Pingvin-Check"
    SUB_TITLE = "Network connectivity monitor"
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="status-box"):
            yield StatusDisplay("Press 'Check now' or CTRL+R to run a check", id="status-display")
            yield Button("check now", id="check-btn", variant="success")
        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "check-btn":
            self.run_worker(self.action_run_check())


    async def action_run_check(self):
        display = self.query_one("#status-display", StatusDisplay)
        display.update("[yellow]Checking...[/yellow]")

        checker = NetworkChecker()
        result = await asyncio.to_thread(checker.check)
        if result.available:
            display.update(f"[green]ONLINE[/green] via {result.method} ({result.latency_ms:.1f}ms)")
        else:
            display.update(f"[red]OFFLINE[/red] - {result.error}")

if __name__ == "__main__":
    app = PingvinApp()
    app.run()