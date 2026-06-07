import os
import re

# Operational Directory
BASE_DIR = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga\spy-x-family"
TEMPLATE_FILE = os.path.join(BASE_DIR, "chapter-001", "index.html")

def get_block(content, start_marker, end_marker):
    start = content.find(start_marker)
    if start == -1: return None
    end = content.find(end_marker, start)
    if end == -1: return None
    return content[start:end + len(end_marker)]

def update_chapter(file_path, head_block, nav_block, app_shell_block, footer_block, scroll_nav_block):
    if not os.path.exists(file_path):
        return

    folder_name = os.path.basename(os.path.dirname(file_path))
    ch_num = folder_name.replace("chapter-", "")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update Head (SEO & PWA)
    current_title = re.search(r"<title>(.*?)</title>", content)
    
    # 1. Replace Head
    old_head = get_block(content, "<head>", "</head>")
    if old_head:
        # Before replacing, let's prepare the template head with correct chapter info
        new_head = head_block
        if current_title:
             new_head = re.sub(r"<title>.*?</title>", current_title.group(0), new_head)
        
        # Add chapter-specific canonical
        canonical_url = f'https://readspyxfamily.org/manga/spy-x-family/{folder_name}/'
        if '<link rel="canonical"' in new_head:
            new_head = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{canonical_url}" />', new_head)
        else:
            new_head = new_head.replace("</head>", f'    <link rel="canonical" href="{canonical_url}" />\n</head>')
        
        content = content.replace(old_head, new_head)

    # 2. Replace Floating Nav
    # We look for the start of the div and find its closing tag or another marker
    nav_start = content.find('<div class="floating-dossier-nav">')
    if nav_start != -1:
        # Find the next section or something to identify the end
        # In our files it usually ends before the main or header
        nav_end = content.find('</nav>', nav_start) # This might be wrong if there are nested navs
        # Better: find the end of the dossier-nav container
        # Actually, let's look for the specific comment if available
        marker = '<!-- end dossier nav -->'
        nav_end = content.find(marker, nav_start)
        if nav_end != -1:
             content = content[:nav_start] + nav_block + content[nav_end + len(marker):]
        else:
             # Fallback: finding the next top level tag
             pass

    # 3. Replace Footer
    old_footer = get_block(content, '<footer', '</footer>')
    if old_footer:
        content = content.replace(old_footer, footer_block)

    # 4. Replace App Shell
    old_shell = get_block(content, '<nav class="mobile-app-shell">', '</nav>')
    if old_shell:
        content = content.replace(old_shell, app_shell_block)
    else:
        # Add it if missing, before </body>
        content = content.replace("</body>", app_shell_block + "\n</body>")

    # 5. Replace/Add Scroll Nav
    if '<div class="scroll-nav">' in content:
        old_scroll = get_block(content, '<div class="scroll-nav">', '</div>')
        if old_scroll:
            content = content.replace(old_scroll, scroll_nav_block)
    else:
        content = content.replace("</body>", scroll_nav_block + "\n</body>")

    # Final Script Checks
    if 'script.js' not in content:
        content = content.replace("</body>", '<script src="../../../script.js" defer></script>\n</body>')
    
    if 'lucide.createIcons()' not in content:
        content = content.replace("</body>", "<script>lucide.createIcons();</script>\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    head_block = get_block(template, "<head>", "</head>")
    # We'll mark the blocks in chapter-001 first for easier extraction
    
    # Actually, I'll just use the blocks I know are there
    nav_block = get_block(template, '<div class="floating-dossier-nav">', '</div>\n\n<header')
    if not nav_block:
         nav_block = get_block(template, '<div class="floating-dossier-nav">', '</header>') # Slightly broader
    
    footer_block = get_block(template, '<footer', '</footer>')
    app_shell_block = get_block(template, '<nav class="mobile-app-shell">', '</nav>')
    scroll_nav_block = get_block(template, '<div class="scroll-nav">', '</div>')

    print(f"Syncing intelligence dossiers across the network...")
    
    for folder in os.listdir(BASE_DIR):
        if folder.startswith("chapter-"):
            file_path = os.path.join(BASE_DIR, folder, "index.html")
            if os.path.exists(file_path):
                print(f"Processing {folder}...")
                update_chapter(file_path, head_block, nav_block, app_shell_block, footer_block, scroll_nav_block)

if __name__ == "__main__":
    main()
