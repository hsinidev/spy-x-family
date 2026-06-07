import os
import re

chapters_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga\Spy X Family"

def fix_chapter_html(content):
    # Remove duplicated Archive Explorer buttons
    # The pattern is usually </div> <button class="dossier-tab-btn"> ... </button> </div>
    
    # First, let's find the first occurrence of the dossier-menu block
    menu_start = content.find('<div class="floating-dossier-nav">')
    if menu_start == -1:
        return content
    
    # Everything after the first valid dossier nav block
    # We want to keep:
    # <div class="floating-dossier-nav">
    #   <div class="dossier-menu">...</div>
    #   <button class="dossier-tab-btn">...</button>
    # </div>
    
    # Regex to catch the whole block
    pattern = re.compile(r'<div class="floating-dossier-nav">.*?</div>\s*</div>', re.DOTALL)
    match = pattern.search(content)
    if match:
        base_nav = match.group(0)
        # Remove ALL occurrences of floating-dossier-nav and replace with one
        content = pattern.sub('', content)
        # Also remove stray buttons/divs if any
        content = re.sub(r'<button class="dossier-tab-btn">.*?</button>\s*</div>', '', content, flags=re.DOTALL)
        
        # Add it back before </body>
        content = content.replace('</body>', base_nav + '\n</body>')
    
    # Clean up multiple </body> if any
    content = re.sub(r'(</body>\s*)+', '</body>\n', content)
    
    return content

for root, dirs, files in os.walk(chapters_dir):
    for file in files:
        if file == "index.html":
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = fix_chapter_html(content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {path}")

print("Done.")
