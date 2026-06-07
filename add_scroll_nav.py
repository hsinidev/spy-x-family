import os
import re

def add_scroll_nav(directory):
    scroll_nav_html = """
    <!-- Fast Scroll Navigation -->
    <div class="scroll-nav">
        <button class="scroll-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Top Secret - Scroll Up">
            <i data-lucide="chevron-up"></i>
        </button>
        <button class="scroll-btn" onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})" title="Mission End - Scroll Down">
            <i data-lucide="chevron-down"></i>
        </button>
    </div>
"""
    
    lucide_script = '<script src="https://unpkg.com/lucide@latest"></script>'
    lucide_init = '<script>lucide.createIcons();</script>'

    for root, dirs, files in os.walk(directory):
        if 'index.html' in files:
            filepath = os.path.join(root, 'index.html')
            
            # Skip the root index.html if we already did it (though this script is for chapters)
            if root == directory:
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Add CSS reference if missing (should be there)
            # 2. Add Lucide if missing
            if 'lucide@latest' not in content:
                content = content.replace('</head>', f'    {lucide_script}\n</head>')

            # 3. Add Scroll Nav Before </body>
            if 'scroll-nav' not in content:
                content = content.replace('</body>', f'{scroll_nav_html}\n    {lucide_init}\n</body>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    manga_dir = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"
    add_scroll_nav(manga_dir)
    print("Fast Scroll Navigation added to all chapter pages.")
