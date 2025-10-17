import speedtest
from datetime import datetime
import csv
import os


FILENAME = "test_results.csv"
FIELD_NAMES = ["timestamp", "download", "upload", "ping", "server", "host", "country"]


def get_speedtest_results():
    """
    Runs an internet speed test and returns download, upload, ping, server name, host name, country
    :return:
    """
    speed = speedtest.Speedtest()
    best_server = speed.get_best_server()

    print("Checking download speed...\n")
    download_speed = speed.download() / 1_000_000  # Megabits

    print("Checking upload speed...\n")
    upload_speed = speed.upload() / 1_000_000  # Megabits

    print("Checking ping...\n")
    ping_result = speed.results.ping
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "download": f"{download_speed:.2f}",
        "upload": f"{upload_speed:.2f}",
        "ping": f"{ping_result:.2f}",
        "server": best_server['name'],
        "host": best_server['host'],
        'country': best_server['country'],
    }


def save_results(filename, results):
    """
    Appends a speed test results to a CSV file.
    """
    file_exits = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        if not file_exits:
            writer.writeheader()
        writer.writerow(results)


def main():
    """
    Main function to run the internet speed test and save the results
    """
    results = get_speedtest_results()
    save_results(FILENAME, results)
    print(f"Internet speed test completed successfully! Results saved to '{FILENAME}'.")


if __name__ == "__main__":
    print("Testing Internet Speed...\n")
    main()
