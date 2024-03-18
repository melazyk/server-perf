# Server Performance Test

Scripts for server test and visualizing results


## yabs.sh

Performance testing scripts

[yabs.sh](https://github.com/masonr/yet-another-bench-script)

apps for testing 
- fio
- iperf3
- geekbench

Testing params
```
curl -sL yabs.sh | bash -s -- -i -n -w yabs.json
```
- Disable network test
- disable network information
- write output to json file for analyze

## Report

- Save json results to directories, each directory is a hoster
- I made more than one tests and get the best result
- 