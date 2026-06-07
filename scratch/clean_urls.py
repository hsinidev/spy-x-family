import os
import re

root_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"
old_manga_dir = os.path.join(root_dir, "manga", "Spy X Family")
new_manga_dir = os.path.join(root_dir, "manga", "spy-x-family")

# Step 1: Rename the directory if it exists
if os.path.exists(old_manga_dir):
    try:
        os.rename(old_manga_dir, new_manga_dir)
        print(f"Renamed {old_manga_dir} to {new_manga_dir}")
    except Exception as e:
        print(f"Error renaming directory: {e}")
else:
    print("Directory already renamed or doesn't exist.")

# Step 2: Define the replacement logic
# We want to replace:
# 1. 'manga/Spy X Family/' -> 'manga/spy-x-family/'
# 2. 'manga/Spy%20X%20Family/' -> 'manga/spy-x-family/'
# 3. 'index.html' at the end of chapter URLs -> '' (clean URLs)

def clean_content(content):
    # Fix the folder name and remove %20
    content = content.replace("manga/Spy X Family/", "manga/spy-x-family/")
    content = content.replace("manga/Spy%20X%20Family/", "manga/spy-x-family/")
    content = content.replace("manga\\Spy X Family\\", "manga/spy-x-family/")
    
    # Optional: remove index.html from chapter links for cleaner URLs
    # Pattern: manga/spy-x-family/chapter-XXX/index.html -> manga/spy-x-family/chapter-XXX/
    content = re.sub(r'(manga/spy-x-family/chapter-[^/"]+)/index\.html', r'\1/', content)
    
    return content

# Files to update at root
root_files = ["index.html", "sitemap.xml", "script.js"]

for filename in root_files:
    filepath = os.path.join(root_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = clean_content(content)
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")

# Step 3: Update all chapter index.html files
manga_path = new_manga_dir if os.path.exists(new_manga_dir) else old_manga_dir

for chapter_folder in os.listdir(manga_path):
    chapter_path = os.path.join(manga_path, chapter_folder)
    if os.path.isdir(chapter_path):
        index_path = os.path.join(chapter_path, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # For chapter files, they might have relative links or absolute ones
            # Let's just apply the same logic
            new_content = clean_content(content)
            
            if new_content != content:
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                # print(f"Updated {chapter_folder}/index.html")

print("URL cleaning complete.")
