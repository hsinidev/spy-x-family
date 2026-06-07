
with open(r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the duplicated footer area
# We want to remove the redundant footer tags and merge them.
# The mess looks like:
# line 1740: <footer class="py-20 px-6 text-center border-t border-white/5 bg-black">
# line 1741: ...
# line 1745: <footer class="py-24 border-t border-white/5 bg-black/20 backdrop-blur-3xl text-center">

new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'footer class="py-20 px-6' in line:
        skip = True
    if 'footer class="py-24 border-t' in line and skip:
        skip = False
    
    if not skip:
        new_lines.append(line)

with open(r'c:\Users\hsini\Desktop\website manga projects\Spy X Family\index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
