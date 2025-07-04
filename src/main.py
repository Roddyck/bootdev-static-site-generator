import os
import shutil

from block_markdown import markdown_to_html_node


def copy_from_dir(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    else:
        for file in os.listdir(dst):
            file_path = os.path.join(dst, file)
            if os.path.isfile(file_path):
                print(f"Removing file: {file_path}")
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"Removing directory: {file_path}")
                shutil.rmtree(file_path)

    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        if os.path.isfile(file_path):
            print(f"Copying file: {file_path} to {dst}")
            shutil.copy(file_path, dst)
        elif os.path.isdir(file_path):
            print(f"Copying dir: {file_path} to {dst}")
            copy_from_dir(file_path, os.path.join(dst, file))


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            title = line[1:].strip()
            break

    if title is None:
        raise Exception("No title found")
    return title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page: {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
        html = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

        with open(template_path, "r") as template_file:
            template = template_file.read()
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)

            if not os.path.dirname(dest_path):
                os.mkdir(os.path.dirname(dest_path))
            with open(dest_path, "w") as f:
                f.write(template)


def generate_pages_recursively(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for file in os.listdir(dir_path_content):
        new_file = os.path.join(dir_path_content, file)
        filename_without_extension = os.path.splitext(file)[0]
        if os.path.isdir(new_file):
            generate_pages_recursively(
                new_file, template_path, os.path.join(dest_dir_path, file)
            )
        else:
            generate_page(
                new_file,
                template_path,
                os.path.join(dest_dir_path, filename_without_extension + ".html"),
            )


def main():
    copy_from_dir("static", "public")
    generate_pages_recursively("content", "template.html", "public")


if __name__ == "__main__":
    main()
