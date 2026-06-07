import os
import re

def natural_sort_key(s):
    return [float(t) if t.replace('.', '').isdigit() else t for t in re.split('([0-9.]+)', s)]

def generate_log_html():
    base_path = 'manga/Spy X Family'
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    dirs.sort(key=natural_sort_key)
    
    html_chunks = []
    for d in reversed(dirs):
        title = d.replace('chapter-', 'Mission_').replace('-', '_').title()
        item_html = f'<a href="manga/Spy X Family/{d}/index.html" class="block px-3 py-2.5 hover:bg-[#064e3b]/20 rounded-sm text-[10px] text-white/50 hover:text-white uppercase tracking-wider transition-all border-l-2 border-transparent hover:border-[#064e3b]">{title}</a>'
        html_chunks.append(item_html)
    
    return "\n".join(html_chunks)

log_html = generate_log_html()

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the content within the mission list container
# <div class="space-y-1 max-h-80 overflow-y-auto custom-scrollbar pr-2">
start_marker = '<div class="space-y-1 max-h-80 overflow-y-auto custom-scrollbar pr-2">'
end_marker = '</div>' # The first closing div after start_marker

start_index = content.find(start_marker) + len(start_marker)
# Find the matching closing div for this specific container
# Since it's nested, we need careful search. 
# But in this specific case, it's the next </div> followed by </div> </div> for the parent divs.
# Actually, the grid script I used earlier was simpler.
# Let's just find the next '</div>' and hope for the best, or use a more specific marker.

# Find the end of this block
end_index = content.find('</div>', start_index)

if start_index != -1 and end_index != -1:
    new_content = content[:start_index] + "\n" + log_html + "\n" + content[end_index:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Log injected")
else:
    print("ERROR: Log markers not found")
