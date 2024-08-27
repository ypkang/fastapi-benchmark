import json
import matplotlib

RESULTS_DIR = "results/"

results = {}

for mode in ["default", "threaded", "async"]:
    if mode not in results:
        results[mode] = {}
    for nworkers in [1, 4, 8]:
        if nworkers not in results[mode]:
            results[mode][nworkers] = {}
        for nthreads in [1]:
            if nthreads not in results[mode][nworkers]:
                results[mode][nworkers][nthreads] = {}
            res = json.load(
                open(RESULTS_DIR + f"{mode}_workers_{nworkers}_threads_{nthreads}.json")
            )
            rps = []
            lats = []
            for concurrency in range(0, 200, 50):
                if concurrency == 0:
                    concurrency = 1
                rps.append(res[str(concurrency)]["requests_per_second"])
                lats.append(res[str(concurrency)]["time_per_request_ms"])

            results[mode][nworkers][nthreads][nworkers] = {"rps": rps, "lats": lats}

with open(f"{RESULTS_DIR}/full_results.json", "w") as f:
    json.dump(results, f, indent=2)
