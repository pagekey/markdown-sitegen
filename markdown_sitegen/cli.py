import glob
import os
import sys

import frontmatter
import markdown


def print_usage():
    print("Usage:")
    print("  markdown-sitegen <DIRECTORY>: generate website from markdown in directory")


def cli_entry_point():
    if len(sys.argv) == 2:
        gen_dir = sys.argv[1]
        if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
            files_to_render = []
            sitegenignore = []
            if os.path.exists(os.path.join(gen_dir, '.sitegenignore')):
                with open(os.path.join(gen_dir, '.sitegenignore')) as f:
                    sitegenignore = f.read().split('\n')
            for root, dirs, files in os.walk(gen_dir):
                if os.path.basename(root) in sitegenignore:
                    continue
                for filename in files:
                    if filename.lower().endswith('.md'):
                        files_to_render.append(os.path.join(root, filename))
            # Render markdown to html
            for filename in files_to_render:
                with open(filename) as f:
                    post = frontmatter.load(f)
                    html = markdown.markdown(post.content)
                    out_filename = os.path.join('build', filename.replace(gen_dir, '').replace('.md', '.html'))
                    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
                    with open(out_filename, 'w') as f:
                        f.write(html)
        else:
            print("Error: not a directory - %s" % gen_dir)
    else:
        print_usage()
