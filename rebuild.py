import sys, traceback
with open('/home/clocky/.config/Code/User/History/10c04ec7/vs4u.html', 'r', encoding='utf-8') as f:
    content = f.read()
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

scripts = [
    'patch_v18.py', 'update_css_and_layout.py', 'patch_js_and_delete.py',
    'patch_bottomsheet.py', 'update_content.py', 'add_loader.py', 'update_loader.py',
    'update_loader_delay.py', 'fix_index.py', 'update_html_models.py',
    'add_code_studio.py', 'add_install_modal.py', 'patch_clockwork_install.py',
    'patch_v2.py'
]

for s in scripts:
    print(f"Running {s}...")
    try:
        exec(open(s).read())
    except Exception as e:
        print(f"Error in {s}:")
        traceback.print_exc()

with open('index.html', 'r', encoding='utf-8') as f:
    final_content = f.read()
print(f"Final size: {len(final_content)} bytes")
