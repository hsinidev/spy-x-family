import os
import re

root_dir = r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga'

def update_chapter_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine depth for relative path
    # manga/Spy X Family/chapter-131/index.html -> ../../../
    rel_path = "../../../"

    # Extract chapter name
    chapter_match = re.search(r'<title>Read Spy X Family - (.*?) Online', content)
    chapter_name = chapter_match.group(1) if chapter_match else "Chapter Archive"
    
    # Clean chapter name (remove 'chapter-')
    chapter_display = chapter_name.replace('chapter-', 'Chapter ')

    # Extract prev/next links if possible
    prev_match = re.search(r'href="(\.\.\/chapter-.*?\/index\.html)" class="[^"]*">PREV</a>', content)
    prev_link = prev_match.group(1) if prev_match else "#"
    
    # New Head
    new_head = f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Read Spy X Family - {chapter_display} | Classified Archive</title>
    <link rel="stylesheet" href="{rel_path}index.css">
    <script src="{rel_path}script.js" defer></script>
    <meta name="geo.region" content="US, FR, JP" />
    <meta name="geo.placename" content="Global" />
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NXKN3VT9XD"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-NXKN3VT9XD');
    </script>
</head>"""

    content = re.sub(r'<head>.*?</head>', new_head, content, flags=re.DOTALL)

    # New Nav
    new_nav = f"""<nav class="fixed top-0 w-full z-[100] px-6 py-4 flex justify-between items-center backdrop-blur-3xl bg-black/60 border-b border-white/5">
        <a href="{rel_path}index.html" class="text-2xl heading uppercase text-[var(--secondary)]">Spy X Family</a>
        <div class="flex items-center gap-6">
            <span class="text-xs font-bold uppercase tracking-widest text-[var(--secondary)]/60">{chapter_display}</span>
            <a href="{rel_path}index.html#archive" class="px-4 py-2 border border-[var(--secondary)]/20 text-[10px] uppercase tracking-widest hover:bg-[var(--secondary)] hover:text-black transition">Archive</a>
        </div>
    </nav>"""

    # Look for the header or nav and replace it
    if '<header class="fixed-nav">' in content:
        content = re.sub(r'<header class="fixed-nav">.*?</header>', new_nav, content, flags=re.DOTALL)
    elif '<nav' in content:
        content = re.sub(r'<nav.*?</nav>', new_nav, content, flags=re.DOTALL)
    else:
        # If no nav found, prepend to body
        content = content.replace('<body>', '<body>\n' + new_nav)

    # New Footer
    new_footer = f"""<footer class="py-20 flex flex-col items-center gap-8 bg-[var(--dark-bg)]">
        <div class="flex gap-4">
            <a href="{prev_link}" class="px-12 py-4 border border-[var(--secondary)]/20 text-xs uppercase tracking-widest hover:bg-[var(--secondary)] hover:text-black transition">Previous Chapter</a>
            <a href="{rel_path}index.html#archive" class="px-12 py-4 bg-[var(--accent)] text-white text-xs uppercase tracking-widest hover:scale-105 transition">Return to Archive</a>
        </div>
        <p class="text-[10px] uppercase tracking-[0.5em] text-white/20">Classified Forger Records - Operation Strix</p>
    </footer>"""

    if '<footer' in content:
        content = re.sub(r'<footer.*?</footer>', new_footer, content, flags=re.DOTALL)
    else:
        # Prepend to end of main if no footer
        content = content.replace('</main>', '</main>\n' + new_footer)

    # Remove inline script at the bottom
    content = re.sub(r'<script>\s*window\.addEventListener\(\'scroll\'.*?</script>', '', content, flags=re.DOTALL)

    # Clean body tags (remove progress div if exists)
    content = content.replace('<div class="progress-line" id="progress"></div>', '')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'index.html':
            update_chapter_file(os.path.join(root, file))

print("All chapter pages updated.")
