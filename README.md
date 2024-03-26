# Server Performance Test

This repository contains scripts for testing server performance and visualizing the results.

## yabs.sh

This script utilizes [yabs.sh](https://github.com/masonr/yet-another-bench-script) for performance testing and includes the following apps for testing:
- fio
- iperf3
- geekbench

The testing parameters used are:
```
curl -sL yabs.sh | bash -s -- -i -n -w yabs.json
```
This command disables the network test, network information, and writes the output to a json file for analysis.

## Report

Keep in mind, it's a dirty test enough

### Input Data

The json results are saved to the result directory. Each subdirectory represents a hoster, and each file in the subdirectory represents a VPS or a real computer. Multiple tests are conducted, and the best result is selected.

### Logic for Visualization

- For "multi" CPU tests, the value is divided by the CPU count.
- For "Speed" and "IOps" tests, the best result across all tests for all block sizes is retained for visualization.