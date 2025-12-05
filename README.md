# Advent of Code - Solutions & Automation

This repository contains my personal solutions for the [Advent of Code](https://adventofcode.com/) challenges, along with a custom Python automation tool to streamline the process.

## AoC Automation Manager

Included in this repo is `aoc-manager.py`, a CLI tool designed to automate the interaction with the Advent of Code servers.

### Features
* **Automatic Setup**: Fetches the daily puzzle input and saves it to a shared `data/` directory.
* **Smart Parsing**: Downloads the problem description (HTML) and converts it into a clean, readable Markdown file (`.md`), preserving code blocks, emphasis, and even hidden Easter eggs.
* **Templating**: Generates a Python solution script with boilerplate code ready for logic implementation.
* **Auto-Submission**: Runs the solution, captures the output, and submits the answer to the AoC API. It handles Part 1/Part 2 detection and server cooldowns automatically.

### Configuration
To use the manager, create a `config.ini` file in the root directory:

```ini
[AOC]
# Your session cookie from browser DevTools (Storage -> Cookies)
session = ... 
# Required by AoC author
user_agent = [github.com/Ciovino/advent-of-code](https://github.com/Ciovino/advent-of-code) by your-email@example.com

[PATHS]
data_folder = data
```

## Installation & Requirements

It is recommended to use a **virtual environment** to keep dependencies isolated.
1. **Create the virtual environment:**
```bash
python -m venv venv
```
2. **Activate the environment:**
   - *Windows (Powershell):* `.\venv\Scripts\Activate.ps1`
   - *Windows (Command Prompt):* `.\venv\Scripts\activate.bat`
   - *macOS/Linux:* `source venv/bin/activate`
3. **Install dependencies:** Once the environment is active, install the required libraries: `pip install -r requirements.txt`

## Usage Workflow
1. **Setup the Day:** Download input and generate files for a specific day (e.g., Year 2025, Day 1):
```bash
python aoc-manager.py 2025 1
```
2. **Solve:** Open the generated script (e.g., `2025/01-secret-entrance.py`). The script expects the solution to be printed to `stdout` using a specific format:
```python
# ... logic ...
print(f"AOC_SOL_1={part_1_result}")
print(f"AOC_SOL_2={part_2_result}")
```
3. **Submit** Run the manager with the `--submit` flag. It will execute your script, parse the output, and send the correct part to the server:
```bash
python aoc-manager.py 2025 1 --submit
```

## Disclaimer and Responsability
This tool automates requests to the Advent of Code website. Please use it **responsibly and be aware** of the potential impact on the server. The creator of AoC, *Eric Wastl*, has explicitly requested caution with automated requests, as the infrastructure is personally managed and has limited capacity. It is highly recommended that you:
- **Avoid excessive and repetitive requests** (`setup_files` or `submit`) when not strictly necessary, especially outside of your personal workflow.
- **Do not ignore "cooldown" messages** received from the server during submission, which the script handles automatically.
- **Keep your `user_agent` updated in `config.ini`** with your contact information to allow the server to identify your requests in case of issues.

The enjoyment of *Advent of Code* relies on everyone's participation; consideration is essential to ensure the experience remains smooth for the entire community.

## Repository Structure
The project is organized by year, with inputs stored centrally.
```
├── aoc-manager.py        # The automation CLI v1.0.1
├── requirements.txt      # Requirements for the manager
├── config.ini            # Configuration (Ignored by Git)
├── data/                 # Shared input files
│   ├── 2025-01.in
│   └── ...
├── 2025/                 # Solutions for 2025
│   ├── 01-secret-entrance.py             # Solution Script
│   ├── 01-secret-entrance-description.md # Parsed Problem
│   └── ...
└── README.md
```

## About Advent of Code
The **Advent of Code** (AoC) is a series of short programming puzzles released daily from December 1st to 25th. The event provides a festive, story-driven way to sharpen algorithmic thinking and coding skills.