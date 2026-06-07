import os
import re

def clean_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove index.html from manga chapter links: e.g., "../chapter-131/index.html" -> "../chapter-131/"
    # We want to catch links that look like chapter-XXX/index.html
    new_content = re.sub(r'(chapter-[0-9.]+)/index\.html', r'\1/', content)
    
    # 2. Remove index.html from root links: e.g., "../../../index.html" -> "../../../"
    # But be careful not to break other things. Usually it's index.html in a href or link.
    new_content = re.sub(r'href="([^"]*?)index\.html"', r'href="\1"', new_content)
    
    # 3. Fix any remaining encoded spaces if they exist (though we renamed the dir, some hardcoded strings might remain)
    new_content = new_content.replace('Spy%20X%20Family', 'spy-x-family')
    new_content = new_content.replace('Spy_X_Family', 'spy-x-family')
    
    # 4. Clean up double slashes created by removing index.html (e.g., "manga/spy-x-family/chapter-129//")
    # This might happen if the original link was "chapter-129/index.html" and we just removed "index.html"
    # Actually my regex (chapter-[0-9.]+)/index\.html already handled the slash.
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"
    manga_dir = os.path.join(base_dir, "manga", "spy-x-family")
    
    # Files to process
    files_to_process = [
        os.path.join(base_dir, "index.html"),
        os.path.join(base_dir, "sitemap.xml"),
        os.path.join(base_dir, "script.js")
    ]
    
    # Process all index.html files in chapters
    if os.path.exists(manga_dir):
        for root, dirs, files in os.walk(manga_dir):
            for file in files:
                if file == "index.html":
                    files_to_process.append(os.path.join(root, file))
    
    updated_count = 0
    for filepath in files_to_process:
        if os.path.exists(filepath):
            if clean_file_content(filepath):
                updated_count += 1
                print(f"Cleaned: {filepath}")
    
    print(f"Task complete. Total files updated: {updated_count}")

if __name__ == "__main__":
    main()
