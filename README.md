# alien_worlds_tools

This repository is a collection of python tools I wrote for myself to improve my Alien Worlds game experience. I offer no warranty on the tools provided here. If you find a bug or have an improvement, you're welcome to submit a pull request. Suggestions are also welcomed, please open an issue. I make not promises to implement every suggestion but will consider anything you may find helpful.

## Quickstart
Run the bootstrap script to pull down the required libraries and install the python environment. You must have pyenv and pip installed prior to running bootstrap.
```
script/bootstrap
```

## aw_reporter.py
This is a tool I use during contests to check information about my mining rig or those of my team mates to determine if changes need to be made.

## tool_efficiency.py
This tool accepts multiple different inputs, the end goal is to produce information about the mining efficiency of a number of different combinations of tools. See help message below for more information:
### Usage Examples:
#### Find most efficient combination assuming all common and epic tools are available
```
./tool_efficiency.py -r common -r epic
```
#### Find most efficient combination of a given set of tools:
```
./tool_efficiency.py -t basic_td -t lucky_drill -t rd9000_excavator -t waxtural_processor -t large_capacitor
```

For more options, use `--help`:
```
Usage: tool_efficiency.py [OPTIONS]

Options:
  -r, --rarity TEXT
  -m, --multiplier FLOAT
  --allow-duplicate
  --summary
  -t, --tool TEXT
  -s, --supply INTEGER
```
