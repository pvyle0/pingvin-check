import argparse
from pingvin.core import NetworkChecker

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Network connectivity")
    parser.add_argument("--host", default="8.8.8.8", help="HOst to check")
    parser.add_argument("--port", type=int, default=53, help="Port to check")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    checker = NetworkChecker()
    status = checker.check_tcp(args.host, args.port)

    if args.format == "json":
        import json
        from dataclasses import asdict
        print(json.dumps(asdict(status)))
    else:
        if status.available:
            print(f"ONLINE via {status.method} ({status.latency_ms:.1f}ms)")
        else:
            print(f"OFFLINE: {status.error}")

if __name__ == "__main__":
    main()