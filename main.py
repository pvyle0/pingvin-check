import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

from pingvin.cli import main

if __name__ == "__main__":
    main()