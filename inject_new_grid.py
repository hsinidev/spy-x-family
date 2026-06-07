import os
import re

def natural_sort_key(s):
    return [float(t) if t.replace('.', '').isdigit() else t for t in re.split('([0-9.]+)', s)]

def generate_grid_html():
    base_path = 'manga/Spy X Family'
    if not os.path.exists(base_path):
        return "ERROR: Path not found"
    
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    dirs.sort(key=natural_sort_key)
    
    total = len(dirs)
    html_chunks = []
    
    # Reverse to show latest first
    for i, d in enumerate(reversed(dirs)):
        mission_num = total - i
        mission_id = f"SF-{mission_num:03d}"
        chapter_title = d.replace('chapter-', '').replace('-', ' ').title()
        
        # Determine Threat Level and Clearance randomly for aesthetic or keep fixed
        threats = ["CONTROLLED", "UNSTABLE", "HIGH-RISK", "CRITICAL"]
        clearance = ["WISE-L1", "WISE-L2", "WISE-L3", "WISE-L4"]
        
        # Use a stable random based on mission_num
        import random
        random.seed(mission_num)
        threat = random.choice(threats)
        clr = random.choice(clearance)
        
        item_html = f"""
            <a href="manga/Spy X Family/{d}/index.html" class="dossier-card-wrap mission-item" data-id="{mission_num}" data-title="MISSION {mission_num}: {chapter_title}">
                <article class="dossier-card">
                    <div class="mission-stamp">CLASSIFIED</div>
                    <div class="dossier-id">MISSION_ID: {mission_id}</div>
                    <h3 class="dossier-title">MISSION {mission_num}</h3>
                    <div class="dossier-meta">
                        <span>STATUS: OPEN</span>
                        <span>THREAT LEVEL: {threat}</span>
                        <span>CLEARANCE: {clr}</span>
                    </div>
                    <div class="mission-brief">
                        Subject discovered in district {random.randint(1,99)}. Evidence collected and filed under Operation Strix.
                    </div>
                </article>
            </a>"""
        html_chunks.append(item_html)
    
    return "\n".join(html_chunks)

grid_html = generate_grid_html()

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the content within <main id="intelligence-grid">...</main>
start_tag = '<main class="intelligence-grid" id="intelligence-grid">'
end_tag = '</main>'

start_index = content.find(start_tag) + len(start_tag)
end_index = content.find(end_tag, start_index)

if start_index != -1 and end_index != -1:
    new_content = content[:start_index] + "\n" + grid_html + "\n" + content[end_index:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Grid injected")
else:
    print("ERROR: Grid markers not found")
