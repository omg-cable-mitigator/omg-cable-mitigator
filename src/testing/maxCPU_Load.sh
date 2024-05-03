#!/bin/bash

num_processes=8
pids=() # Array to store process IDs

gen_cpu_load() {
    while true; do
        true
    done
}

# Start processes in background and store their process IDs
for ((i=1; i<$num_processes; i++)); do
    gen_cpu_load &
    pids+=($!) # Store the process ID of the background process
done

# Function to kill all background processes
kill_processes() {
    echo "Exiting..."
    for pid in "${pids[@]}"; do
        kill $pid
    done
    exit
}

# Trap Enter key signal (SIGINT) and call kill_processes function
trap 'kill_processes' SIGINT

echo "Processes generating HIGH CPU load. Press Enter to exit."
read

# Call kill_processes function when Enter key is pressed
kill_processes
