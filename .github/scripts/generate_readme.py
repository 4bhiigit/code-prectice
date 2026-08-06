import os
import re

def main():
    # Use current working directory as the repository root
    workspace_dir = os.getcwd()
    
    # List subdirectories, ignoring hidden ones and .github
    subdirs = [
        d for d in os.listdir(workspace_dir) 
        if os.path.isdir(os.path.join(workspace_dir, d)) 
        and not d.startswith('.') 
        and d != '.github'
    ]

    problems = []

    # Sort folders numerically by LeetCode problem ID if possible
    def get_sort_key(folder_name):
        match = re.match(r'^(\d+)', folder_name)
        if match:
            return int(match.group(1))
        return 999999

    for folder in sorted(subdirs, key=get_sort_key):
        folder_path = os.path.join(workspace_dir, folder)
        readme_path = os.path.join(folder_path, "README.md")
        
        title = folder.replace('-', ' ').title()
        link = ""
        difficulty = "Unknown"
        
        # Try parsing README.md if it exists
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Extract title and link
                    match_title = re.search(r'<h2><a href="([^"]+)">([^<]+)</a></h2>', content)
                    if match_title:
                        link = match_title.group(1)
                        title = match_title.group(2)
                    
                    # Extract difficulty
                    match_diff = re.search(r'Difficulty-([A-Za-z]+)-', content)
                    if match_diff:
                        difficulty = match_diff.group(1)
            except Exception as e:
                print(f"Error reading {readme_path}: {e}")
        
        # Find solution files in folder (any file that isn't README.md)
        try:
            sol_files = [f for f in os.listdir(folder_path) if f != "README.md"]
        except Exception as e:
            print(f"Error listing files in {folder_path}: {e}")
            sol_files = []
            
        sol_links = []
        for sf in sol_files:
            sol_links.append(f"[{sf}](./{folder}/{sf})")
            
        problems.append({
            "folder": folder,
            "title": title,
            "link": link,
            "difficulty": difficulty,
            "solutions": ", ".join(sol_links)
        })

    # Count difficulties
    easy_count = sum(1 for p in problems if p['difficulty'].lower() == 'easy')
    medium_count = sum(1 for p in problems if p['difficulty'].lower() == 'medium')
    hard_count = sum(1 for p in problems if p['difficulty'].lower() == 'hard')

    readme_content = f"""# Code Practice

Welcome to my personal code practice repository! This repository is a curated collection of my solutions to various algorithmic and data structure problems, primarily sourced from **LeetCode**. 

All solutions are implemented in **Python** with focus on correctness, optimal time & space complexity, and clean code principles.

## 📊 Repository Summary

- **Total Solved:** {len(problems)}
- 🟢 **Easy:** {easy_count}
- 🟡 **Medium:** {medium_count}
- 🔴 **Hard:** {hard_count}

---

## 📂 Solutions Index

Here is the list of problems solved in this repository:

| # | Problem | Difficulty | Solution |
|---|---|---|---|
"""

    for idx, p in enumerate(problems, 1):
        prob_cell = f"[{p['title']}]({p['link']})" if p['link'] else p['title']
        
        # Add badges for difficulty
        diff = p['difficulty']
        if diff.lower() == 'easy':
            diff_cell = f"🟢 Easy"
        elif diff.lower() == 'medium':
            diff_cell = f"🟡 Medium"
        elif diff.lower() == 'hard':
            diff_cell = f"🔴 Hard"
        else:
            diff_cell = diff
            
        readme_content += f"| {idx} | {prob_cell} | {diff_cell} | {p['solutions']} |\n"

    readme_content += """
---

## 🛠️ Tech Stack & Structure

- **Language:** Python 3.x
- **Structure:** Each problem has its own directory containing:
  - `README.md` - The problem description, examples, and constraints.
  - `<solution>.py` - The optimized python solution code.

## 🚀 How to Run Locally

To run or test any of the solutions locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/4bhiigit/code-prectice.git
   cd code-prectice
   ```

2. **Run a solution:**
   You can run the python files using your preferred environment or command line:
   ```bash
   python "10-regular-expression-matching/regular-expression-matching.py"
   ```

---
*Happy Coding! 💻*
"""

    output_readme_path = os.path.join(workspace_dir, "README.md")
    with open(output_readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md successfully updated at {output_readme_path}")

if __name__ == "__main__":
    main()
