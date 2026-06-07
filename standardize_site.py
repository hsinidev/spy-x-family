import os
import re

# Set the base directory to the project root
BASE_DIR = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"

def get_master_components():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract nav
    nav_match = re.search(r'(<nav class="fixed.*?">.*?</nav>)', content, re.DOTALL)
    nav_html = nav_match.group(1) if nav_match else ""
    
    # Extract footer
    footer_match = re.search(r'(<footer.*?>.*?</footer>)', content, re.DOTALL)
    footer_html = footer_match.group(1) if footer_match else ""
    
    # Extract mobile app shell
    mobile_nav_match = re.search(r'(<nav class="mobile-app-shell">.*?</nav>)', content, re.DOTALL)
    mobile_nav_html = mobile_nav_match.group(1) if mobile_nav_match else ""
    
    # Extract scroll-nav (FABs)
    scroll_nav_match = re.search(r'(<div class="scroll-nav">.*?</div>)', content, re.DOTALL)
    scroll_nav_html = scroll_nav_match.group(1) if scroll_nav_match else ""
    
    return nav_html, footer_html, mobile_nav_html, scroll_nav_html

def fix_paths(html, depth):
    prefix = "../" * depth if depth > 0 else "./"
    
    # Fix CSS and JS paths
    html = re.sub(r'href="index\.css"', f'href="{prefix}index.css"', html)
    html = re.sub(r'src="script\.js"', f'src="{prefix}script.js"', html)
    
    # Fix links
    if depth > 0:
        # If we are in a chapter page (depth=3 typically: manga/spy-x-family/chapter-xxx/index.html)
        # We need to change manga/spy-x-family/chapter-xxx/ to ../chapter-xxx/
        html = html.replace('href="manga/spy-x-family/', 'href="../')
        # Also fix home link
        html = html.replace('href="/"', f'href="{prefix}index.html"')
        html = html.replace('href="index.html"', f'href="{prefix}index.html"')
    else:
        # We are at root
        html = html.replace('href="/"', 'href="./index.html"')

    # Fix legal pages
    pages = ["about.html", "privacy.html", "terms.html", "contact.html", "dmca.html", "cookies.html", "disclaimer.html"]
    for page in pages:
        html = html.replace(f'href="./{page}"', f'href="{prefix}{page}"')
        html = html.replace(f'href="{page}"', f'href="{prefix}{page}"')
    
    return html

def process_file(file_path, nav, footer, mobile_nav, scroll_nav):
    # Don't process the master index itself as it might lead to weird loop issues if not careful
    if file_path.lower() == os.path.join(BASE_DIR, "index.html").lower():
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    rel_path = os.path.relpath(file_path, BASE_DIR)
    # Check depth: e.g. manga/spy-x-family/chapter-1/index.html has depth 3
    # Wait, relpath is manga\spy-x-family\chapter-1\index.html
    # split by os.sep -> ['manga', 'spy-x-family', 'chapter-1', 'index.html']
    # Length is 4. Depth should be 3.
    parts = rel_path.split(os.sep)
    depth = len(parts) - 1
    
    processed_nav = fix_paths(nav, depth)
    processed_footer = fix_paths(footer, depth)
    processed_mobile_nav = fix_paths(mobile_nav, depth)
    processed_scroll_nav = fix_paths(scroll_nav, depth)
    
    # Replace Nav
    content = re.sub(r'<nav class="fixed.*?">.*?</nav>', processed_nav, content, flags=re.DOTALL)
    
    # Replace Footer
    content = re.sub(r'<footer.*?>.*?</footer>', processed_footer, content, flags=re.DOTALL)
    
    # Replace Mobile Nav
    if '<nav class="mobile-app-shell">' in content:
        content = re.sub(r'<nav class="mobile-app-shell">.*?</nav>', processed_mobile_nav, content, flags=re.DOTALL)
    else:
        content = content.replace('</body>', processed_mobile_nav + '\n</body>')
        
    # Replace Scroll Nav (FABs)
    if '<div class="scroll-nav">' in content:
        content = re.sub(r'<div class="scroll-nav">.*?</div>', processed_scroll_nav, content, flags=re.DOTALL)
    elif '<div class="tactical-fab">' in content:
        content = re.sub(r'<div class="tactical-fab">.*?</div>', processed_scroll_nav, content, flags=re.DOTALL)
    else:
        # Inject before mobile nav
        content = content.replace('<nav class="mobile-app-shell">', processed_scroll_nav + '\n<nav class="mobile-app-shell">')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("Extracting master components from index.html...")
    nav, footer, mobile_nav, scroll_nav = get_master_components()
    
    # Find all .html files
    for root, dirs, files in os.walk(BASE_DIR):
        if any(d in root for d in ['node_modules', '.git', '. gemini']): continue
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(f"Standardizing: {file_path}")
                process_file(file_path, nav, footer, mobile_nav, scroll_nav)

if __name__ == "__main__":
    main()
