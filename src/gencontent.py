import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    print(f"Generating : {from_path} -> {dest_path}")
    markdown_file = open(from_path, 'r')
    markdown_content = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, 'r')
    template_content = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    print(f'Dest Dir Path : {dest_dir_path}')
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template_content)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        to_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path) and from_path[-3:] == '.md':
            to_path = Path(to_path).with_suffix(".html")
            generate_page(from_path, template_path, to_path)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, to_path)