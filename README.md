# 🐧 Pingvin-Check

> A lightweight network connectivity checker.

Pingvin-Check verifies whether the internet is reachable using two methods: **ICMP ping** and **TCP connection** to multiple public DNS servers (Cloudflare, Google, Yandex, Quad9, OpenDNS). If ICMP is blocked by a firewall, the TCP fallback still gives you a reliable answer.

## Features

- **ICMP ping** — standard host reachability check
- **TCP connection check** — fallback across multiple public DNS servers
- **Latency measurement** — response time tracking in milliseconds
- **JSON output** — machine-readable output for use in scripts/pipelines
- **Logging** — internal debug logs showing which checks succeeded/failed
- **Tests** — unit tests covering success and failure scenarios (with mocking)

## Project structure## Installation

```bash
git clone https://github.com/pvyle0/pingvin-check.git
cd pingvin-check
pip install -e .
```

## Usage

```bash
python main.py
```

Check a specific host/port:

```bash
python main.py --host 1.1.1.1 --port 53
```

Get machine-readable JSON output:

```bash
python main.py --format json
```

### Options

| Flag       | Description             | Default    |
|------------|--------------------------|------------|
| `--host`   | Target host to check     | `8.8.8.8`  |
| `--port`   | TCP port to connect to   | `53`       |
| `--format` | Output format (`text`/`json`) | `text` |

## Running tests

```bash
pytest tests/ -v
```

## License

MIT
