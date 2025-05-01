from datetime import datetime

class Logger:

    __console_output = True

    @staticmethod
    def log(data):
        timestamp = datetime.now().isoformat()
        if Logger.__console_output:
            print(f"#> {data} ({timestamp})")

    @staticmethod
    def small_log(data):
        timestamp = datetime.now().isoformat()
        if Logger.__console_output:
            print(f"{data} ({timestamp})")

    def show_log_in_console(value):
        Logger.__console_output = True