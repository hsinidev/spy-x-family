import os
import re

base_path = r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga\Spy X Family'
chapters = sorted([d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])

tailwind_cdn = """
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#064e3b',
                        secondary: '#fef3c7',
                        accent: '#991b1b',
                    }
                }
            }
        }
    </script>
"""

new_footer = """
    <footer class="py-24 border-t border-white/5 bg-black/20 backdrop-blur-3xl text-center">
        <div class="flex flex-wrap justify-center gap-10 mb-12">
            <a href="../../../index.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Privacy Policy</a>
            <a href="../../../index.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Terms of Service</a>
            <a href="../../../index.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">DMCA Report</a>
            <a href="../../../index.html" class="redacted text-xs uppercase tracking-[0.3em] font-bold">Intelligence Contact</a>
        </div>
        <p class="text-[10px] uppercase tracking-[0.6em] text-white/10 mb-2">Subject: Unauthorized Access to Archive is Prohibited</p>
        <p class="text-[10px] uppercase tracking-[0.4em] text-white/20">© 2026 WISE Intelligence Agency Portal. Operation Strix Active.</p>
    </footer>
"""

progress_bar = '<div class="read-progress-container"><div class="read-progress-bar"></div></div>'

dossier_links = []
for ch in chapters:
    display_name = ch.replace('-', ' ').title()
    dossier_links.append(f'<a href="../{ch}/index.html" class="dossier-link"><span>{display_name}</span><span class="text-[var(--accent)]">>></span></a>')

dossier_menu = f"""
    <div class="floating-dossier-nav">
        <div class="dossier-menu">
            <h4 class="text-[10px] uppercase tracking-widest text-white/30 mb-4 border-b border-white/10 pb-2">Intelligence Archive</h4>
            <div class="max-h-[60vh] overflow-y-auto pr-2">
                {''.join(dossier_links)}
            </div>
        </div>
        <button class="dossier-tab-btn">
            <span class="text-xs">Archive Explorer</span>
        </button>
    </div>
"""

for chapter in chapters:
    file_path = os.path.join(base_path, chapter, 'index.html')
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add Tailwind CDN if missing
    if 'cdn.tailwindcss.com' not in content:
        content = content.replace('</head>', tailwind_cdn + '</head>')
    
    # 2. Add/Refresh Progress Bar
    if '<div class="read-progress-container">' in content:
        content = re.sub(r'<div class="read-progress-container">.*?</div></div>', progress_bar, content, flags=re.DOTALL)
    else:
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + progress_bar, content)
    
    # 3. Refresh Footer
    if '<footer' in content:
        content = re.sub(r'<footer.*?</footer>', new_footer, content, flags=re.DOTALL)
    else:
        content = content.replace('</body>', new_footer + '\n</body>')
    
    # 4. Refresh Floating Menu
    if '<div class="floating-dossier-nav">' in content:
        content = re.sub(r'<div class="floating-dossier-nav">.*?</div>\n\s*</div>', dossier_menu, content, flags=re.DOTALL)
    else:
        content = content.replace('</body>', dossier_menu + '\n</body>')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Successfully synchronized {len(chapters)} chapter pages with Tailwind and Footer updates.")
