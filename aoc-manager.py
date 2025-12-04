# ---------------------------------------------------------------------
# Advent of Code Manager
# Author: Ciovino
# Description: Automates the AoC workflow: fetches inputs, parses HTML 
#              descriptions to Markdown, generates solution templates, 
#              executes logic, and submits answers via HTTP requests.
# ---------------------------------------------------------------------
import requests
import configparser
import os
import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag
import logging
import argparse
import subprocess

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8',
)

config = configparser.ConfigParser()
config.read('config.ini')

SESSION = config['AOC']['session']
USER_AGENT = config['AOC']['user_agent']
DATA_FOLDER = config['PATHS']['data_folder']

HEADERS = {
    "User-Agent": USER_AGENT,
    "Cookie": f"session={SESSION}"
}

def process_inline_elements(tag):
    """
    Manage inline formatting (bold, code, links, easter eggs)
    """
    text_parts = []
    
    for child in tag.children:
        if isinstance(child, NavigableString):
            text_parts.append(str(child))
        elif isinstance(child, Tag):
            # Recursion for inner tag
            inner_text = process_inline_elements(child)
            
            if child.name == 'code':
                text_parts.append(f"`{inner_text}`")
            elif child.name == 'em':
                text_parts.append(f"**{inner_text}**")
            elif child.name == 'a':
                href = child.get('href', '')
                text_parts.append(f"[{inner_text}]({href})")
            elif child.name == 'span' and child.get('title'):
                # EASTER EGG 🐰
                joke = child['title']
                text_parts.append(f"{inner_text} (🐰 {joke})")
                logging.info(f"Found Easter Egg: '{inner_text} (🐰 {joke})'")
            else:
                text_parts.append(inner_text)
                
    return "".join(text_parts)

def to_markdown(article_content: list[Tag]):
    """
    Prepare <article> HTML for a Markdown file, following a custom format
    """
    blocks = []
    
    for child in article_content:
        if isinstance(child, NavigableString):
            continue # Ignore whitespace
            
        if child.name == 'h2':
            text = child.get_text().replace("---", "").strip()
            if "Day" in text:
                # Ignore "Day" since it's manually done prior
                continue 
            blocks.append(('h2', f"## {text}"))
            
        elif child.name == 'p':
            text = process_inline_elements(child)
            blocks.append(('p', text))
            
        elif child.name == 'pre':
            # Code blocks
            code_tag = child.find('code')
            if code_tag:
                text = code_tag.get_text()
            else:
                text = child.get_text()
            blocks.append(('code', f"```\n{text}\n```"))
            
        elif child.name == 'ul':
            list_items = []
            for li in child.find_all('li'):
                li_text = process_inline_elements(li)
                list_items.append(f"* {li_text}")
            blocks.append(('ul', "\n".join(list_items)))

    # Custom format
    md_output = ""
    for i, (type_, content) in enumerate(blocks):
        md_output += content

        if i < len(blocks) - 1:
            next_type = blocks[i+1][0]
            
            if type_ == 'p' and next_type == 'ul':
                # Only 1 newline if the next block is a list
                md_output += "\n"
            else:
                md_output += "\n\n"
    return md_output

def get_page_data(year, day):
    base_url = f"https://adventofcode.com/{year}/day/{day}"
    logging.info(f"Fetching: {base_url}")
    
    resp_page = requests.get(base_url, headers=HEADERS)
    if resp_page.status_code != 200:
        logging.error(f"Error {resp_page.status_code}. Exiting...")
        sys.exit(1)
        
    soup = BeautifulSoup(resp_page.text, 'html.parser')
    
    # 1. Problem Title
    main_h2 = soup.find('h2').text
    match = re.search(r"--- Day \d+: (.+) ---", main_h2)
    title_clean = match.group(1) if match else "Unknown Problem"
    title_slug = title_clean.lower().replace(" ", "-")
    
    # 2. Parsing for Description file
    articles = soup.find_all('article', class_="day-desc")
    
    full_markdown = f"# Day {day}: {title_clean}\n"
    
    # Part 1
    if len(articles) > 0:
        full_markdown += "## Part One\n\n"
        full_markdown += to_markdown(articles[0].contents.copy())
    
    # Part 2 (if exists)
    if len(articles) > 1:
        full_markdown += "\n\n"
        full_markdown += to_markdown(articles[1].contents.copy())
    
    # 3. Status Check
    # TODO: Check if this is correct
    page_text = soup.get_text()
    if "Both parts of this puzzle are complete!" in page_text:
        status = "COMPLETED"
    elif "The first half of this puzzle is complete!" in page_text:
        status = "PART2"
    else:
        status = "PART1"
        
    # 4. Input Download
    input_data = ""
    input_filename = f"{year}-{day:02d}.in"
    input_path = os.path.join(DATA_FOLDER, input_filename)
    if not os.path.exists(input_path):
        input_url = f"{base_url}/input"
        resp_input = requests.get(input_url, headers=HEADERS)
        if resp_input.status_code == 200:
            input_data = resp_input.text

    return {
        "title_slug": title_slug,
        "title_clean": title_clean,
        "status": status,
        "description": full_markdown,
        "input_data": input_data
    }

def setup_files(year, day):
    data = get_page_data(year, day)
    
    # Make directories
    os.makedirs(DATA_FOLDER, exist_ok=True)
    day_folder = str(year)
    os.makedirs(day_folder, exist_ok=True)
    
    # --- 1. Save Input File ---
    if data["input_data"]:
        input_path = os.path.join(DATA_FOLDER, f"{year}-{day:02d}.in")
        with open(input_path, "w") as f:
            f.write(data["input_data"])
        logging.info(f"Saved input file to '{input_path}'")

    # File prefix for description and python script
    file_prefix = f"{day:02d}-{data['title_slug']}"
    base_path = os.path.join(day_folder, file_prefix)

    # --- 2. Description ---
    desc_path = f"{base_path}-description.md"
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write(data["description"])
    logging.info(f"Description updated, at '{desc_path}'")

    # --- 3. Create Python Template ---
    py_path = f"{base_path}.py"
    if not os.path.exists(py_path):
        input_name = f"{year}-{day:02d}.in"
        template = \
f"""# ---------------------------------------------------------------------
# Advent of Code {year} - Day {day:02} - {data['title_clean'].title()}
# Problem: See .\\{desc_path} for full details
# Author: Ciovino
# ---------------------------------------------------------------------
import os

# Parse the input
with open(os.path.join('{DATA_FOLDER}', '{input_name}'), 'r') as f:
    # TODO: Implement the logic based on the input
    pass

# --- SOLVE ---
part1_solution = 0
part2_solution = 0

# --- PRINT ---
print(f"AOC_SOL_1={{part1_solution}}")
print(f"AOC_SOL_2={{part2_solution}}")
"""
        with open(py_path, "w") as f:
            f.write(template)
        logging.info(f"Created python template at: '{py_path}'")
    else:
        logging.warning(f"Python template already exists, at: '{py_path}'")

    return py_path, data["status"]

def submit_answer(year, day, level, answer):
    """Invia la soluzione al server e parsa la risposta."""
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    payload = {
        "level": level,
        "answer": answer
    }
    
    logging.info(f"Submitting Level {level}: {answer}")
    
    resp = requests.post(url, data=payload, headers=HEADERS)
    
    if resp.status_code != 200:
        logging.error(f"HTTP Error {resp.status_code} during submission.")
        return False
    
    # Check what the server responded
    soup = BeautifulSoup(resp.text, 'html.parser')
    article = soup.find('article')
    text = article.get_text()
    
    if "That's the right answer" in text:
        logging.info(f"Correct answer! Level {level} completed.")
        return True
    elif "not the right answer" in text:
        if "too high" in text:
            logging.warning("Wrong: Answer is too high.")
        elif "too low" in text:
            logging.warning("Wrong: Answer is too low.")
        else:
            logging.warning("Wrrong: Answer.")
    elif "You gave an answer too recently" in text:
        wait_match = re.search(r"You have (?:(\d+)m )?(\d+)s left to wait", text)
        if wait_match:
            mins = wait_match.group(1) if wait_match.group(1) else "0"
            secs = wait_match.group(2)
            logging.warning(f"Cooldown: Need to wait {mins}m {secs}s before sumbitting again.")
        else:
            logging.warning("Cooldown: Try again later")
    elif "You don't seem to be solving the right level" in text:
        logging.warning(f"Level {level} already solved or locked.")
        return False
    else:
        logging.error(f"Unknown responses: {text}")
    return False # Fallback

def run_and_submit(year, day):
    # 1. Run the setup to check if file exists, and also get the problem status
    script_path, status = setup_files(year, day)
    
    if status == "COMPLETED":
        logging.info("Problem already fully completed! No submission needed.")
        return

    logging.info(f"Running solution script: {script_path}")
    
    # 2. Run the python script
    try:
        result = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Script failed with error:\n{e.stderr}")
        return

    # 3. Get the solutions
    output = result.stdout
    sol1_match = re.search(r"AOC_SOL_1=(.+)", output)
    sol2_match = re.search(r"AOC_SOL_2=(.+)", output)
    
    sol1 = sol1_match.group(1).strip() if sol1_match else None
    sol2 = sol2_match.group(1).strip() if sol2_match else None

    if not sol1 and not sol2:
        logging.warning("No solution markers found in stdout (AOC_SOL_x).")
        logging.info("Stdout was:\n" + output)
        return

    logging.info(f"Found Solutions => Part 1: {sol1}, Part 2: {sol2}")

    # 4. Send solution based on the challenge status
    if status == "PART1":
        success = submit_answer(year, day, 1, sol1)
        if success:
            logging.info("Fetching Part 2 description...")
            setup_files(year, day) 
    elif status == "PART2":
        submit_answer(year, day, 2, sol2)
    else:
        logging.error(f"Unknown status: {status}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code Manager")
    
    parser.add_argument("year", type=int, help="Year of the event (e.g., 2023)")
    parser.add_argument("day", type=int, help="Day of the problem (1-25)")
    parser.add_argument("--submit", action="store_true", help="Run the solution and submit the answer")

    args = parser.parse_args()

    # Basic input validation
    if not (1 <= args.day <= 25):
        logging.error("Day must be between 1 and 25.")
        sys.exit(1)
    
    if args.year < 2015:
        logging.error("Advent of Code started in 2015.")
        sys.exit(1)

    logging.info(f"--- AoC Manager: Day {args.day} Year {args.year} ---")
    
    if args.submit:
        run_and_submit(args.year, args.day)
    else:
        setup_files(args.year, args.day)