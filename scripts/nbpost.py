# This script is aim to automate the publications from
# notebooks to markdown. There is a big problem
# that usually happend to me when do it.
# I have to replace the origin of the images once it is transformed
# to a markdown and renaming the markdown itself.

import os
import re
from datetime import datetime
import argparse


# Define the parser
parser = argparse.ArgumentParser(description="Short parser")

# You need to provide this arguments
parser.add_argument("--notebook", action="store", dest="notebook")
parser.add_argument("--origin", action="store", dest="origin")

# Take the arguments from the parser
args = parser.parse_args()

# Date formatter
current_date = datetime.now().strftime("%Y-%m-%d")

# Each markdown follows the Y-m-d-<name>.md format
markdown_file_name = \
    current_date + "-" + args.notebook + ".md"

# Previous origin of the images
origin = args.origin if args.origin.endswith("/") else args.origin + "/"

# New origin of the images (following the project structure)
new_origin = f"./assets/img/{current_date}-{args.notebook}/"

# Convert notebook to Markdown
os.system(f"jupyter nbconvert --to markdown {args.notebook}.ipynb --output-dir='./post'")

# Rename the resulting markdown
os.system(f'mv ./post/{args.notebook}.md ./post/{markdown_file_name}')


def update_image_paths(md_file, old_path, new_path):
    """
    Inside the markdown text replace
    the root of the images to "/assets/img/".
    This is because all images are saved under that folder.
    """

    print(f"Parcing markdown: {md_file}... \nReplacing path {old_path} for {new_path}")

    with open(md_file, 'r') as file:
        content = file.read()

    # Replace old path with new path in Markdown
    content = re.sub(re.escape(old_path), new_path, content)

    with open(md_file, 'w') as file:
        file.write(content)


# Update paths in the generated Markdown file
update_image_paths(
    f"./post/{markdown_file_name}",
    origin,
    new_origin
)
