import os
import re

chapters_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga\Spy X Family"

BUTTON_HTML = """
    <button class="dossier-tab-btn" onclick="toggleDossier()">
        <span class="dossier-tab-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </span>
        <span class="dossier-tab-text">Archive Explorer</span>
    </button>
"""

def fix_chapter_html(content):
    # 1. Standardize Footer Links
    content = content.replace('href="../../../index.html" class="redacted', 'class="redacted') # Temp remove href
    content = content.replace('Privacy Policy</a>', '<a href="../../../privacy-policy.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Privacy Policy</a>')
    content = content.replace('Terms of Service</a>', '<a href="../../../terms-of-service.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Terms of Service</a>')
    content = content.replace('DMCA Report</a>', '<a href="../../../dmca.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">DMCA Report</a>')
    content = content.replace('Intelligence Contact</a>', '<a href="mailto:contact@spyxfamilymanga.com" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Intelligence Contact</a>')
    # Cleanup any weird duplication from my previous run
    content = re.sub(r'<(a href="\.\./\.\./\.\./index\.html" )+class="redacted', '<a href="../../../index.html" class="redacted', content)

    # 2. Fix the Dossier Nav (Remove duplicates and ensure button exists)
    # Find the menu links part to preserve them
    links_match = re.search(r'<div class="max-h-\[60vh\].*?</div>', content, re.DOTALL)
    if links_match:
        links_html = links_match.group(0)
        
        # New clean nav block
        new_nav = f"""
<div class="floating-dossier-nav">
    <div class="dossier-menu" id="dossierMenu">
        <h4 class="text-[10px] uppercase tracking-widest text-white/30 mb-4 border-b border-white/10 pb-2">Intelligence Archive</h4>
        {links_html}
    </div>
    {BUTTON_HTML}
</div>
"""
        # Remove any existing nav blocks
        content = re.sub(r'<div class="floating-dossier-nav">.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="floating-dossier-nav">.*?</body>', '</body>', content, flags=re.DOTALL)
        
        # Insert new nav before </body>
        content = content.replace('</body>', new_nav + '\n</body>')

    # 3. Remove /# from URLs (specifically placeholder links)
    content = content.replace('/#', '/')
    
    # Ensure only one valid body/html end
    content = re.sub(r'(</body>\s*)+', '</body>\n', content)
    content = re.sub(r'(</html>\s*)+', '</html>\n', content)

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
                print(f"Refined {path}")

print("Done.")
