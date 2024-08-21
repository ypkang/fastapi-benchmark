#
# A helper script to restart a given process as part of a Live Update.
#
# Further reading:
# https://docs.tilt.dev/live_update_reference.html#restarting-your-process
#
# Usage:
#   Copy start.sh and restart.sh to your container working dir.
#
#   Make your container entrypoint:
#   ./start.sh path-to-binary [args]
#
#   To restart the container:
#   ./restart.sh

set -eu

process_id=""

trap quit TERM INT

quit() {
  if [ -n "$process_id" ]; then
    kill $process_id
  fi
}

MODE=$(jq -r ".mode" config.json)
NTHREADS=$(jq -r ".nthreads" config.json)
NWORKERS=$(jq -r ".nworkers" config.json)

while true; do
    rm -f restart.txt
    if [ $MODE = "default" ]; then
      echo "Start default server with uvicorn $NWORKERS"
      uvicorn sync_server:app --workers $NWORKERS &
    elif [ $MODE = "threaded" ]; then
      echo "Start sync threaded server $NWORKERS $NTHREADS"
      gunicorn -w $NWORKERS -k uvicorn_worker.UvicornWorker --threads $NTHREADS sync_server:app &
      # uvicorn sync_server:app &
    elif [ $MODE = "async" ]; then
      echo "Start async server $NWORKERS"
      uvicorn async_server:app --workers $NWORKERS &
    else
      echo "Invalid mode"
      exit 1
    fi  

    process_id=$!
    echo "$process_id" > process.txt
    set +e
    wait $process_id
    EXIT_CODE=$?
    set -e
    if [ ! -f restart.txt ]; then
        echo "Exiting with code $EXIT_CODE"
        exit $EXIT_CODE
    fi
    echo "Restarting"
done
