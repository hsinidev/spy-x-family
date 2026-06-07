import os
import glob

# Search in all HTML files
for f in glob.glob('manga/Spy X Family/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace index.html#archive with index.html
    new_content = content.replace('index.html#archive', 'index.html')
    # Replace href="#" with href="/"
    new_content = new_content.replace('href="#"', 'href="/"')
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Cleaned: {f}")

# Also clean index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content.replace('href="#"', 'href="/"')
if new_content != content:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Cleaned: index.html")
