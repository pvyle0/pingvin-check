# 🐧 Pingvin-Check

> A lightweight network connectivity checker.

Pingvin-Check verifies whether the internet is reachable using two methods: **ICMP ping** and **TCP connection** to DNS servers (e.g. `8.8.8.8:53`). If ICMP is blocked by a firewall, the TCP check still gives you a reliable answer.

> **Status: early development.** Core logic is being built incrementally, feature by feature.

## Features

- **ICMP ping** — standard host reachability check
- **TCP connection check** — fallback method for environments where ICMP is blocked
- **Latency measurement** — response time tracking

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

## License

MIT
