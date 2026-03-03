from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from rich.panel import Panel
from rich.align import Align
from collections import defaultdict

# -----------------------
# Logs Data
# -----------------------
logs = [
    {"user": "ali", "ip_address": "192.168.1.10", "country": "EG", "status": "failed"},
    {"user": "ali", "ip_address": "192.168.1.10", "country": "EG", "status": "failed"},
    {"user": "ali", "ip_address": "192.168.1.10", "country": "EG", "status": "failed"},
    {"user": "ali", "ip_address": "192.168.1.10", "country": "EG", "status": "failed"},
    {"user": "ali", "ip_address": "192.168.1.10", "country": "EG", "status": "success"},

    {"user": "sara", "ip_address": "10.0.0.5", "country": "US", "status": "success"},
    {"user": "sara", "ip_address": "10.0.0.5", "country": "US", "status": "failed"},
    {"user": "sara", "ip_address": "10.0.0.5", "country": "US", "status": "failed"},

    {"user": "omar", "ip_address": "172.16.0.3", "country": "UK", "status": "failed"},
    {"user": "omar", "ip_address": "172.16.0.3", "country": "UK", "status": "failed"},
    {"user": "omar", "ip_address": "172.16.0.3", "country": "UK", "status": "failed"},
    {"user": "omar", "ip_address": "172.16.0.3", "country": "UK", "status": "failed"},
    {"user": "omar", "ip_address": "172.16.0.3", "country": "UK", "status": "failed"},

    {"user": "lina", "ip_address": "8.8.8.8", "country": "DE", "status": "success"},
    {"user": "lina", "ip_address": "8.8.8.8", "country": "DE", "status": "success"},

    {"user": "youssef", "ip_address": "203.0.113.5", "country": "FR", "status": "failed"},
    {"user": "youssef", "ip_address": "203.0.113.5", "country": "FR", "status": "failed"},
    {"user": "youssef", "ip_address": "203.0.113.5", "country": "FR", "status": "failed"},
]

# -----------------------
# Analysis
# -----------------------
def analyze_logs(logs):
    failed = defaultdict(int)
    success = defaultdict(int)
    ips = defaultdict(set)

    for entry in logs:
        user = entry["user"]
        ip = entry["ip_address"]
        status = entry["status"]

        ips[user].add(ip)

        if status == "failed":
            failed[user] += 1
        elif status == "success":
            success[user] += 1

    return failed, success, ips


def calculate_risk(failed_count):
    risk_levels = {}
    for user, count in failed_count.items():
        if count >= 5:
            risk_levels[user] = ("HIGH", "red")
        elif count >= 3:
            risk_levels[user] = ("MEDIUM", "yellow")
        else:
            risk_levels[user] = ("LOW", "green")
    return risk_levels


# -----------------------
# Dashboard
# -----------------------
class SOCDashboard(App):

    CSS = """
    Screen {
        background: #0f111a;
    }

    DataTable {
        height: 75%;
        border: round #ff00ff;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        title = Panel(
            Align.center("[bold magenta]💻 SOC LOGIN ANALYSIS DASHBOARD 💻[/bold magenta]"),
            border_style="magenta",
        )

        author = Panel(
            Align.center("[bold cyan]👩🏻‍💻 Developed by Cybersecurity Engineer | ESRAA AHMED AWAD]"),
            border_style="bright_cyan",
        )

        yield Static(title)
        yield Static(author)
        yield DataTable(id="table")
        yield Footer()

    def on_mount(self):

        failed, success, ips = analyze_logs(logs)
        risk = calculate_risk(failed)

        table = self.query_one("#table", DataTable)

        table.add_columns(
            "User",
            "Failed",
            "Success",
            "Unique IPs",
            "Risk",
            "Failed Bar"
        )

        all_users = set(list(failed.keys()) + list(success.keys()))

        for user in all_users:
            f = failed.get(user, 0)
            s = success.get(user, 0)
            unique_ips = len(ips[user])
            level, color = risk.get(user, ("LOW", "green"))

            bar = f"[{color}]" + "█" * min(f, 20) + "[/]"

            table.add_row(
                user,
                str(f),
                str(s),
                str(unique_ips),
                f"[bold {color}]{level}[/]",
                bar
            )

        table.zebra_stripes = True
        table.cursor_type = "row"
        table.focus()


if __name__ == "__main__":
    SOCDashboard().run()