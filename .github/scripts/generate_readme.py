import os
import re
from collections import Counter

# Language mapping based on file extension
LANG_MAP = {
    '.py': 'Python',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.c': 'C',
    '.java': 'Java',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.go': 'Go',
    '.rs': 'Rust',
    '.kt': 'Kotlin',
    '.swift': 'Swift',
    '.sql': 'SQL'
}

LANG_EMOJI = {
    'Python': '🐍',
    'C++': '⚡',
    'C': '🔹',
    'Java': '☕',
    'JavaScript': '📜',
    'TypeScript': '📘',
    'Go': '🐹',
    'Rust': '🦀',
    'Kotlin': '📱',
    'Swift': '🍏',
    'SQL': '🗄️'
}

def main():
    workspace_dir = os.getcwd()
    
    subdirs = [
        d for d in os.listdir(workspace_dir) 
        if os.path.isdir(os.path.join(workspace_dir, d)) 
        and not d.startswith('.') 
        and d != '.github'
    ]

    problems = []
    lang_counter = Counter()

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
        
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    match_title = re.search(r'<h2><a href="([^"]+)">([^<]+)</a></h2>', content)
                    if match_title:
                        link = match_title.group(1)
                        title = match_title.group(2)
                    
                    match_diff = re.search(r'Difficulty-([A-Za-z]+)-', content)
                    if match_diff:
                        difficulty = match_diff.group(1)
            except Exception as e:
                print(f"Error reading {readme_path}: {e}")
        
        try:
            sol_files = [f for f in os.listdir(folder_path) if f != "README.md"]
        except Exception as e:
            print(f"Error listing files in {folder_path}: {e}")
            sol_files = []
            
        sol_links = []
        for sf in sol_files:
            _, ext = os.path.splitext(sf)
            ext = ext.lower()
            if ext in LANG_MAP:
                lang_name = LANG_MAP[ext]
                lang_counter[lang_name] += 1
            sol_links.append(f"[{sf}](./{folder}/{sf})")
            
        problems.append({
            "folder": folder,
            "title": title,
            "link": link,
            "difficulty": difficulty,
            "solutions": ", ".join(sol_links)
        })

    easy_count = sum(1 for p in problems if p['difficulty'].lower() == 'easy')
    medium_count = sum(1 for p in problems if p['difficulty'].lower() == 'medium')
    hard_count = sum(1 for p in problems if p['difficulty'].lower() == 'hard')

    # Build language breakdown section
    lang_stats_str = ""
    if lang_counter:
        for lang, count in lang_counter.most_common():
            emoji = LANG_EMOJI.get(lang, '💻')
            lang_stats_str += f"- {emoji} **{lang}:** {count}\n"
    else:
        lang_stats_str = "- 💻 **Solutions available in repository**\n"

    readme_content = f"""# Code Practice

Welcome to my personal code practice repository! This repository is a curated collection of my solutions to various algorithmic and data structure problems, primarily sourced from **LeetCode**.

---

## 📊 Repository Summary

### 🎯 Difficulty Breakdown
- 🟢 **Easy:** {easy_count}
- 🟡 **Medium:** {medium_count}
- 🔴 **Hard:** {hard_count}
- 📈 **Total Solved:** {len(problems)}

### 💻 Languages Used
{lang_stats_str}
---

## 📂 Solutions Index

Here is the list of problems solved in this repository:

| # | Problem | Difficulty | Solution |
|---|---|---|---|
"""

    for idx, p in enumerate(problems, 1):
        prob_cell = f"[{p['title']}]({p['link']})" if p['link'] else p['title']
        
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

- **Structure:** Each problem has its own directory containing:
  - `README.md` - The problem description, examples, and constraints.
  - Solution file(s) (e.g. `.py`, `.cpp`, `.java`).

## 🚀 How to Run Locally

To run or test any of the solutions locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/4bhiigit/code-prectice.git
   cd code-prectice
   ```

2. **Run a solution:**
   ```bash
   # Example Python
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
