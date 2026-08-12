# 🐧 Pingvin-Check

> A lightweight network connectivity checker.

Pingvin-Check verifies whether the internet is reachable using two methods: **ICMP ping** and **TCP connection** to multiple DNS servers (Cloudflare, Google, Yandex, Quad9, OpenDNS). If ICMP is blocked by a firewall, the TCP fallback still gives you a reliable answer.

> **Status: early development.** Core logic is being built incrementally, feature by feature.

## Features

- **ICMP ping** — standard host reachability check
- **TCP connection check** — fallback across multiple public DNS servers
- **Latency measurement** — response time tracking in milliseconds
- **Logging** — internal debug logs showing which checks succeeded/failed
- **Tests** — unit tests covering both success and failure scenarios (with mocking)

## Project structure

pingvin-check/
├── pingvin/
│ ├── core.py # NetworkChecker logic (ping + TCP fallback)
│ └── cli.py # Command-line interface
├── tests/
│ └── test_core.py # Unit tests
├── main.py # Entry point


## Installation

```bash
git clone https://github.com/pvyle0/pingvin-check.git
cd pingvin-check
pip install -e .
```

## Usage

```bash
python main.py
```

Or check a specific host/port:

```bash
python main.py --host 1.1.1.1 --port 53
```

### Options

| Flag     | Description             | Default    |
|----------|--------------------------|------------|
| `--host` | Target host to check     | `8.8.8.8`  |
| `--port` | TCP port to connect to   | `53`       |

## Running tests

```bash
pytest tests/ -v
```

## License

MIT
