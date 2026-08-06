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

LANG_COLOR = {
    'Python': 'FFD700',
    'C++': 'FFB700',
    'Java': 'E5C158',
    'JavaScript': 'F7DF1E',
    'TypeScript': '3178C6',
    'Go': '00ADD8',
    'Rust': 'DEA584'
}

def auto_pad_folders(workspace_dir):
    """Automatically rename un-padded folders like '24-foo' to '0024-foo'."""
    subdirs = [
        d for d in os.listdir(workspace_dir) 
        if os.path.isdir(os.path.join(workspace_dir, d)) 
        and not d.startswith('.') 
        and d != '.github'
    ]

    for folder in subdirs:
        match = re.match(r'^(\d{1,3})-(.*)', folder)
        if match:
            num = int(match.group(1))
            rest = match.group(2)
            new_folder_name = f"{num:04d}-{rest}"
            if folder != new_folder_name:
                old_path = os.path.join(workspace_dir, folder)
                new_path = os.path.join(workspace_dir, new_folder_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Auto-padded folder: {folder} -> {new_folder_name}")
                except Exception as e:
                    print(f"Error auto-padding folder {folder}: {e}")

def main():
    workspace_dir = os.getcwd()
    
    # First, auto-pad any un-padded problem folders
    auto_pad_folders(workspace_dir)

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
        
        prob_id = get_sort_key(folder)
        title_raw = re.sub(r'^\d+-', '', folder).replace('-', ' ').title()
        title = title_raw
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
        for sf in sorted(sol_files):
            _, ext = os.path.splitext(sf)
            ext = ext.lower()
            if ext in LANG_MAP:
                lang_name = LANG_MAP[ext]
                lang_counter[lang_name] += 1
            sol_links.append(f"[{sf}](./{folder}/{sf})")
            
        problems.append({
            "id": prob_id,
            "folder": folder,
            "title": title,
            "link": link,
            "difficulty": difficulty,
            "solutions": ", ".join(sol_links)
        })

    easy_count = sum(1 for p in problems if p['difficulty'].lower() == 'easy')
    medium_count = sum(1 for p in problems if p['difficulty'].lower() == 'medium')
    hard_count = sum(1 for p in problems if p['difficulty'].lower() == 'hard')

    # Build language badges string
    lang_badges_list = []
    if lang_counter:
        for lang, count in lang_counter.most_common():
            color = LANG_COLOR.get(lang, 'FFD700')
            lang_badges_list.append(
                f"![{lang}](https://img.shields.io/badge/{lang}-{count}-{color}?style=for-the-badge&labelColor=11141A)"
            )
    lang_badges_str = " ".join(lang_badges_list)

    readme_content = f"""<div align="center">

![Header Banner](./.github/assets/header_banner.svg)

<br/>

### 🏆 Premium LeetCode Portfolio Summary

[![Total Solved](https://img.shields.io/badge/Total_Solved-{len(problems)}-FFD700?style=for-the-badge&logo=leetcode&logoColor=black&labelColor=11141A)](https://leetcode.com/u/4bhii/)
[![Easy](https://img.shields.io/badge/Easy-{easy_count}-00FF87?style=for-the-badge&labelColor=11141A)](https://leetcode.com/u/4bhii/)
[![Medium](https://img.shields.io/badge/Medium-{medium_count}-FFB700?style=for-the-badge&labelColor=11141A)](https://leetcode.com/u/4bhii/)
[![Hard](https://img.shields.io/badge/Hard-{hard_count}-FF4B4B?style=for-the-badge&labelColor=11141A)](https://leetcode.com/u/4bhii/)

<br/>

### 💻 Languages Breakdown

{lang_badges_str}

</div>

---

## 📂 Solutions Index

Here is the complete list of problems solved in this repository, ordered by **LeetCode Problem ID**:

| # | Problem | Difficulty | Solution |
|---|---|---|---|
"""

    for p in problems:
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
            
        readme_content += f"| {p['id']} | {prob_cell} | {diff_cell} | {p['solutions']} |\n"

    readme_content += """
---

## 🛠️ Tech Stack & Structure

- **Structure:** Each problem has its own directory formatted as `XXXX-problem-name` containing:
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
   python "0010-regular-expression-matching/regular-expression-matching.py"
   ```

---
<div align="center">
  <i>Happy Coding! 💻 • Designed with Premium Golden Bubble Theme</i>
</div>
"""

    output_readme_path = os.path.join(workspace_dir, "README.md")
    with open(output_readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md successfully updated at {output_readme_path}")

    # Write to GitHub Step Summary if running in GitHub Actions
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        summary_content = f"""## 🚀 Auto Update README Execution Summary

### 📊 Repository Statistics
- 🟢 **Easy:** {easy_count}
- 🟡 **Medium:** {medium_count}
- 🔴 **Hard:** {hard_count}
- 📈 **Total Solved:** {len(problems)}

### 💻 Languages Breakdown
- Python: {lang_counter.get('Python', 0)} | Java: {lang_counter.get('Java', 0)} | C++: {lang_counter.get('C++', 0)}

✅ **README.md was successfully updated with Premium Golden Theme!**
"""
        try:
            with open(summary_path, "a", encoding="utf-8") as sf:
                sf.write(summary_content)
            print("Successfully written to GITHUB_STEP_SUMMARY.")
        except Exception as e:
            print(f"Failed to write to GITHUB_STEP_SUMMARY: {e}")

if __name__ == "__main__":
    main()
