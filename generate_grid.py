import os
import re

# Correct path for Spy X Family chapters
path = r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\manga\Spy X Family'
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.startswith('chapter-')]

def sort_key(s):
    # Extract numbers and handle decimals
    match = re.search(r'chapter-(\d+\.?\d*)', s)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0

dirs.sort(key=sort_key, reverse=True)

html_output = ''
for d in dirs:
    num_str = d.replace('chapter-', '')
    # For display title, replace -Omake with [OMAKE] or just make it look good
    display_title = num_str.replace('-Omake', ' [SPECIAL MISSION]')
    display_title = display_title.replace('.5', '.5').replace('.1', '.1')
    
    # Extract the main number for the stamp
    main_num_match = re.search(r'(\d+)', num_str)
    main_num = main_num_match.group(1) if main_num_match else '000'
    
    html_output += f"""
                <div class="dossier-card-wrap">
                    <a href="manga/Spy X Family/{d}" class="dossier-card">
                        <div class="mission-stamp">MISSION_{main_num}</div>
                        <div class="dossier-id">ID: SF-{num_str}</div>
                        <h3 class="dossier-title">Mission {display_title}</h3>
                        <div class="dossier-meta">
                            <span>Status: <span style="color: #4CAF50;">ARCHIVED</span></span>
                            <span>Level: <span style="color: #E9D5CA;">SECURE</span></span>
                        </div>
                        <div class="dossier-arrow">→</div>
                    </a>
                </div>"""

# Write to the absolute path in artifacts for easy retrieval if needed, 
# but also we can just use the output.
with open('chapters_grid.txt', 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f"STRIX_GRID_GEN: Successfully compiled {len(dirs)} dossiers.")
