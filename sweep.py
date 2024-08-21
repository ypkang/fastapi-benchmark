import os
import json
import time
import subprocess


def parse_ab_output(output):
    result = {}
    lines = output.splitlines()

    # Parse the relevant lines
    for line in lines:
        if line.startswith("Server Software:"):
            result["server_software"] = line.split(":")[1].strip()
        elif line.startswith("Server Hostname:"):
            result["server_hostname"] = line.split(":")[1].strip()
        elif line.startswith("Server Port:"):
            result["server_port"] = line.split(":")[1].strip()
        elif line.startswith("Document Path:"):
            result["document_path"] = line.split(":")[1].strip()
        elif line.startswith("Document Length:"):
            result["document_length"] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Concurrency Level:"):
            result["concurrency_level"] = line.split(":")[1].strip()
        elif line.startswith("Time taken for tests:"):
            result["time_taken"] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Complete requests:"):
            result["complete_requests"] = line.split(":")[1].strip()
        elif line.startswith("Failed requests:"):
            result["failed_requests"] = line.split(":")[1].strip()
        elif line.startswith("Total transferred:"):
            result["total_transferred"] = line.split(":")[1].strip().split()[0]
        elif line.startswith("HTML transferred:"):
            result["html_transferred"] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Requests per second:"):
            result["requests_per_second"] = line.split(":")[1].strip().split()[0]
        elif (
            line.startswith("Time per request:") and "across all concurrent" not in line
        ):
            result["time_per_request_ms"] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Transfer rate:"):
            result["transfer_rate"] = line.split(":")[1].strip().split()[0]

    return result


def run_ab_test(concurrency, url, requests=1000):
    print(f"Running ab test with concurrency {concurrency} and {requests} requests")
    # Run the ab command with the specified concurrency level
    command = f"ab -n {requests} -c {concurrency} {url}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Completed ab test with concurrency {concurrency} and {requests} requests")
    return result.stdout, parse_ab_output(result.stdout)


def start_server(mode, nworkers, nthreads=0):
    print("Starting server with", mode, nworkers, nthreads)
    # update json file and wait for 10 seconds for server to start
    with open("config.json", "wb") as f:
        f.write(
            json.dumps(
                {
                    "mode": mode,
                    "nworkers": nworkers,
                    "nthreads": nthreads,
                }
            ).encode()
        )
    time.sleep(20)


RESULTS_DIR = "results"
RAW_RESULTS_DIR = "raw_results"
SERVER_URL = "http://127.0.0.1:8000/read_and_write_item"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(RAW_RESULTS_DIR, exist_ok=True)


# Sweep sync threaded server
# for mode in ["threaded", "async"]:
for mode in ["default", "async"]:
    for nthreads in [0]:
        if nthreads == 0:
            nthreads = 1
        for nworkers in [1]:
            start_server(mode, nworkers, nthreads)
            results = {}
            raw_results = {}
            for concurrency in range(0, 1100, 100):
                if concurrency == 0:
                    concurrency = 1

                raw_res, res = run_ab_test(
                    concurrency, SERVER_URL, requests=1 * concurrency
                )

                results[concurrency] = res
                raw_results[concurrency] = raw_res

            results_file = os.path.join(
                RESULTS_DIR, f"{mode}_workers_{nworkers}_threads_{nthreads}.json"
            )
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)

            raw_results_file = os.path.join(
                RAW_RESULTS_DIR, f"{mode}_workers_{nworkers}_threads_{nthreads}.json"
            )
            with open(raw_results_file, "w") as f:
                json.dump(raw_results, f, indent=2)
