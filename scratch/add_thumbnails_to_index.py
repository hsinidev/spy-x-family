import os
import re

# Paths
base_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"
index_path = os.path.join(base_dir, "index.html")

def add_thumbnails():
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find each mission item
    # <a href="manga/Spy X Family/chapter-131/index.html" class="dossier-card-wrap mission-item" data-id="184" data-title="MISSION 184: 131">
    # <article class="dossier-card">
    
    pattern = re.compile(r'(<a href="([^"]+)"[6^>]+class="dossier-card-wrap mission-item"[^>]*>.*?<article class="dossier-card">)', re.DOTALL)

    def replace_func(match):
        full_match = match.group(1)
        href = match.group(2)
        
        # Get the directory of the chapter
        chapter_dir = os.path.dirname(href)
        thumb_path = os.path.join(chapter_dir, "01.jpg").replace('\\', '/')
        
        # Check if thumbnail already exists in the content to avoid double adding
        if 'dossier-thumbnail' in full_match:
            return full_match
            
        # Insert thumbnail after the title or before the meta
        # Wait, let's look at the structure again
        # <div class="mission-stamp">CLASSIFIED</div>
        # <div class="dossier-id">MISSION_ID: SF-184</div>
        # <h3 class="dossier-title">MISSION 184</h3>
        
        insert_after = r'<h3 class="dossier-title">([^<]+)</h3>'
        replacement = r'<h3 class="dossier-title">\1</h3>\n                    <div class="dossier-thumbnail">\n                        <img src="' + thumb_path + r'" alt="Mission Briefing Image" loading="lazy" class="mission-thumb-img">\n                    </div>'
        
        new_full_match = re.sub(insert_after, replacement, full_match)
        return new_full_match

    # This regex is a bit complex for re.sub directly on match groups. 
    # Let's do a simpler approach: iterate over all found mission cards.
    
    new_content = content
    # Find all items
    items = re.findall(r'<a href="([^"]+)"[^>]+class="dossier-card-wrap mission-item".*?<article class="dossier-card">.*?</article>.*?</a>', content, re.DOTALL)
    
    for href in set(items):
        chapter_dir = os.path.dirname(href)
        thumb_path = os.path.join(chapter_dir, "01.jpg").replace('\\', '/')
        
        # Find the specific block for this href
        # We need to be careful with unique identification. href + metadata should be enough.
        
        # Let's try a safer replacement approach per block
        pass

    # Actually, a simple string replacement for the h3 tag inside the mission-item context might be easier.
    # But since all h3's look similar, I need to tie them to the href.
    
    lines = content.split('\n')
    updated_lines = []
    current_href = None
    in_article = False
    
    for line in lines:
        match_href = re.search(r'href="([^"]+)"[^>]+mission-item', line)
        if match_href:
            current_href = match_href.group(1)
            
        if '<article class="dossier-card">' in line:
            in_article = True
            
        if in_article and '<h3 class="dossier-title">' in line and 'dossier-thumbnail' not in content:
            # We found the title inside a mission item
            updated_lines.append(line)
            if current_href:
                chapter_dir = os.path.dirname(current_href)
                thumb_url = os.path.join(chapter_dir, "01.jpg").replace('\\', '/')
                updated_lines.append(f'                    <div class="dossier-thumbnail">')
                updated_lines.append(f'                        <img src="{thumb_url}" alt="Mission Scan" loading="lazy" class="mission-thumb-img">')
                updated_lines.append(f'                    </div>')
            continue
            
        if '</a>' in line:
            in_article = False
            current_href = None
            
        updated_lines.append(line)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines))
    
    print("Optimization complete: Thumbnails added to all dossier cards.")

if __name__ == "__main__":
    add_thumbnails()
