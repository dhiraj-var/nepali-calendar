import sys
from .app import NepaliCalendarApp


def main():
    app = NepaliCalendarApp()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
