import os
import re
from datetime import datetime

import argparse

# Define the parser
parser = argparse.ArgumentParser(description="Short parser")
parser.add_argument("--notebook", action="store", dest="notebook")

# Take the arguments from the parser
args = parser.parse_args()


def update_image_paths(md_file, old_path, new_path):
    with open(md_file, 'r') as file:
        content = file.read()

    # Replace old path with new path in Markdown
    content = re.sub(re.escape(old_path), new_path, content)

    with open(md_file, 'w') as file:
        file.write(content)


current_date_formatted = datetime.now().strftime("%Y-%m-%d")
markdown_name_formatted =  \
    current_date_formatted + "-" + args.notebook + ".md"
image_path_origin = f'./assets/{args.notebook}/'
image_path_destination = f"./assets/{current_date_formatted}-{args.notebook}/"
image_path_formatted =  \
    "/assets/img/" + current_date_formatted + "-" + args.notebook + "/"

# Convert notebook to Markdown
os.system(f'jupyter nbconvert --to markdown {args.notebook}.ipynb')

# Rename the resulting markdown
os.system(f'mv {args.notebook}.md {markdown_name_formatted}')

# Rename the folder of images if it exists

if os.path.exists(image_path_origin):
    os.system(f'mv {image_path_origin} {image_path_destination}')

print(image_path_origin, image_path_formatted)

# Update paths in the generated Markdown file
update_image_paths(
    markdown_name_formatted,
    image_path_origin,
    image_path_formatted
)
