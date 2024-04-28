block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def type_heading(block):
    pattern = r'^#{1,6}\s+(.+)'
    match = re.match(pattern, block)
    if match:
        return True     
    
    return False

def type_code(block):
    lines = block.split("\n")
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")

def type_quote(block):
    lines = block.split("\n")
    for line in lines:
        if line[0] != '>': return False
    return True


def type_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- ") and not line.startswith("* "): return False
    return True

def type_ordered_list(block):
    lines = block.split("\n")
    list_start = 1
    for line in lines:
        if not line.startswith(f'{list_start}. '): return False
        list_start += 1
    return True

def block_to_block_type(block):
    if type_heading(block): return block_type_heading
    elif type_code(block): return block_type_code
    elif type_quote(block): return block_type_quote
    elif type_unordered_list(block): return block_type_unordered_list
    elif type_ordered_list(block): return block_type_ordered_list
    else: return block_type_paragraph

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    filtered_blocks = []
    
    # Process each major block
    for block in blocks:
        if not block.strip():
            continue  # Skip empty blocks

        # Normalize the block by handling explicit line breaks
        lines = block.split("\n")
        processed_block = []

        for line in lines:
            if line.strip() == "":
                continue  # Skip empty lines within a block
            # Add processed lines back to the list
            processed_block.append(line.strip())

        # Join lines that are not separate list items or explicitly separated
        filtered_block = '\n'.join(processed_block)
        filtered_blocks.append(filtered_block)
    
    return filtered_blocks

def convert_q_block_to_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    mod_lines = " ".join(new_lines)
    children_nodes = text_to_children(mod_lines)
    return ParentNode("blockquote", children_nodes)

def convert_ul_block_to_node(block):
    items = block.split("\n")
    new_items = []
    for item in items:
        text = item[2:]
        children_nodes = text_to_children(text)
        new_items.append(ParentNode("li", children_nodes))
    return ParentNode("ul", new_items)

def convert_ol_block_to_node(block):
    items = block.split("\n")
    new_items = []
    for item in items:
        text = item[3:]
        children_nodes = text_to_children(text)
        new_items.append(ParentNode("li", children_nodes))
    return ParentNode("ol", new_items)

def convert_c_block_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children_nodes = text_to_children(text)
    return ParentNode("pre", [ParentNode("code", children_nodes)])

def convert_h_block_to_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def convert_p_block_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children_nodes = text_to_children(paragraph)
    return ParentNode("p", children_nodes)

def text_to_children(text):
    text_node = text_to_textnodes(text)
    children_nodes = []
    for node in text_node:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # add all children -> all blocks as children to this root_node
    children_nodes = []
    for block in blocks:
        if block_to_block_type(block) == block_type_quote:
            children_nodes.append(convert_q_block_to_node(block))
        if block_to_block_type(block) == block_type_unordered_list:
            children_nodes.append(convert_ul_block_to_node(block))
        if block_to_block_type(block) == block_type_ordered_list:
            children_nodes.append(convert_ol_block_to_node(block))
        if block_to_block_type(block) == block_type_code:
            children_nodes.append(convert_c_block_to_node(block))
        if block_to_block_type(block) == block_type_heading:
            children_nodes.append(convert_h_block_to_node(block))
        if block_to_block_type(block) == block_type_paragraph:
            children_nodes.append(convert_p_block_to_node(block))
            
    return ParentNode("div", children_nodes, None)


