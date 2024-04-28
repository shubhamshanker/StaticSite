from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)
import re

    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    mod_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            mod_nodes.append(node)
        else:
            text_block = node.text
            potential_nodes = text_block.split(delimiter)
            if len(potential_nodes) % 2 == 0:
                raise ValueError("Invalid Markdown Sequence")
            for i in range(len(potential_nodes)):
                if potential_nodes[i] == "":
                    continue
                if i%2 == 0:
                    node = TextNode(potential_nodes[i], text_type_text)
                else: node = TextNode(potential_nodes[i], text_type)
                mod_nodes.append(node)
    return mod_nodes


def split_nodes_image(old_nodes):
    mod_nodes = []
    for node in old_nodes:
        original_text = node.text
        images_list = extract_markdown_images(original_text)
        if len(images_list) == 0:
            mod_nodes.append(node)
            continue
        for image in images_list:
            potential_nodes = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if potential_nodes[0] != "":
                node1 = TextNode(potential_nodes[0], text_type_text)
                mod_nodes.append(node1)
            node2_img = TextNode(image[0], text_type_image, image[1])
            mod_nodes.append(node2_img)
            original_text = potential_nodes[1]
        if original_text != "":
            node3 =  TextNode(original_text, text_type_text)
            mod_nodes.append(node3)
    return mod_nodes

def split_nodes_link(old_nodes):
    mod_nodes = []
    for node in old_nodes:
        original_text = node.text
        links_list = extract_markdown_links(original_text)
        if len(links_list) == 0:
            mod_nodes.append(node)
            continue
        for link in links_list:
            potential_nodes = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if potential_nodes[0] != "":
                node1 = TextNode(potential_nodes[0], text_type_text)
                mod_nodes.append(node1)
            node2_link = TextNode(link[0], text_type_link, link[1])
            mod_nodes.append(node2_link)
            original_text = potential_nodes[1]
        if original_text != "":
            node3 =  TextNode(original_text, text_type_text)
            mod_nodes.append(node3)
    return mod_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
