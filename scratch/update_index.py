import re

file_path = r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update card classes
content = content.replace('glass-card group block relative overflow-hidden rounded-3xl h-72 shadow-2xl', 
                          'dossier-card group block relative overflow-hidden h-96 shadow-2xl')

# Update image classes and opacity
content = content.replace('opacity-30 group-hover:scale-110 group-hover:opacity-100 transition-all duration-700" loading="lazy"',
                          'opacity-20 group-hover:scale-110 group-hover:opacity-40 transition-all duration-700 scan-img" loading="lazy"')

# Add paper-clip
content = re.sub(r'(<img[^>]+scan-img[^>]+>)', r'\1\n                        <div class="paper-clip"></div>', content)

# Update h3 classes and add subtitle
def update_h3(match):
    h3_text = match.group(1)
    # Capitalize first letter of chapter
    h3_text = h3_text.replace('chapter-', 'Chapter ')
    return f'<h3 class="text-4xl uppercase leading-none group-hover:translate-x-2 transition-transform tracking-tight">{h3_text}</h3>\n                            <span class="text-xs font-bold uppercase tracking-widest opacity-50 mt-2 block">Classified Document</span>'

content = re.sub(r'<h3 class="text-5xl bangers uppercase leading-none group-hover:translate-x-2 transition-transform tracking-tight">(.*?)</h3>', update_h3, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")
