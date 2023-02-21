import os
import re
import shutil
import sys

import datetime
import frontmatter
import jinja2
import markdown
import yaml
from pygments.formatters import HtmlFormatter

from markdown_sitegen.lib import get_root_path


CONFIG_DIR = '.markdown-sitegen/'
BUILD_DIR = 'build'
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'web')
STATIC_DIR = os.path.join(TEMPLATE_DIR, 'static')

def print_usage():
    print("Usage:")
    print("  markdown-sitegen <DIRECTORY>: generate website from markdown in directory")


def cli_entry_point():
    if len(sys.argv) == 2:
        gen_dir = sys.argv[1]
        if os.path.exists(gen_dir) and os.path.isdir(gen_dir):
            # Compute files to render, taking into account .sitegenignore
            files_to_render = []
            image_files = []
            sitegenignore = []
            if os.path.exists(os.path.join(gen_dir, '.sitegenignore')):
                with open(os.path.join(gen_dir, '.sitegenignore')) as f:
                    sitegenignore = f.read().split('\n')
            for root, dirs, files in os.walk(gen_dir):
                if os.path.basename(root) in sitegenignore:
                    continue
                for filename in files:
                    full_path = os.path.join(root, filename)
                    # Add markdown files
                    if filename.lower().endswith('.md'):
                        files_to_render.append(full_path)
                    # Add image files
                    for image_type in ['.jpg', '.jpeg', '.png', '.gif']:
                        if filename.lower().endswith(image_type):
                            image_files.append(full_path)
            # Delete previous build dir
            if os.path.exists(BUILD_DIR):
                shutil.rmtree(BUILD_DIR)
            # Load config file
            config_file_path = os.path.join(gen_dir, CONFIG_DIR, 'config.yml')
            if not os.path.exists(config_file_path):
                config_file_path = os.path.join(TEMPLATE_DIR, 'default_config.yml')
            with open(config_file_path) as f:
                config = yaml.safe_load(f)
            # Load all posts and get metadata
            posts = []
            post_paths = {}
            for filename in files_to_render:
                with open(filename) as f:
                    post = frontmatter.load(f)
                    # Only publish the post if path specified
                    if 'date' in post:
                        post['date_parsed'] = datetime.datetime.strptime(post['date'], '%Y-%m-%d')
                        if 'path' in post:
                            if post['path'] in post_paths:
                                raise ValueError('Two posts with the same path: ', post['path'])
                            else:
                                post_paths[post['path']] = True
                            datetime_today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
                            date_in_future = post['date_parsed'] > datetime_today
                            if not date_in_future:
                                posts.append(post)
            # Render markdown to html
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
            post_template = env.get_template('post.html')
            # Sort the posts by date
            posts = sorted(posts, key=lambda x: x['date_parsed'], reverse=True)
            for i,post in enumerate(posts):
                # Init prev/next posts
                next_post = None
                if i < len(posts) - 1:
                    next_post = posts[i+1]
                prev_post = None
                if i > 0:
                    prev_post = posts[i-1]
                # Compute relative path to HTML file
                relpath = post['path'] + '/index.html'
                # Remove leading slash from path to HTML file
                if relpath.startswith('/'):
                    relpath = relpath[1:]
                out_filename = os.path.join(BUILD_DIR, relpath)
                os.makedirs(os.path.dirname(out_filename), exist_ok=True)
                root_path = get_root_path(relpath)
                # Render markdown to html
                post_content = post.content
                post_content = re.sub(r"\!\[(.+)\]\((.+)\)", f'![\\1]({os.path.dirname(os.path.dirname(root_path))}/static/img/\\2)', post_content)
                post['body'] = markdown.markdown(post_content, extensions=['fenced_code', 'codehilite'])
                # Add truncated body if present
                if '<!-- truncate -->' in post['body']:
                    idx = post['body'].index('<!-- truncate -->')
                    post['summary'] = post['body'][0:idx]
                # Render template
                content = post_template.render(
                    post=post,
                    body=post['body'],
                    root_path=root_path,
                    config=config,
                    next_post=next_post,
                    prev_post=prev_post,
                )
                with open(out_filename, 'w') as f:
                    f.write(content)
            # Render index
            index_template = env.get_template('index.html')
            content = index_template.render(
                posts=posts,
                config=config,
            )
            with open(os.path.join(BUILD_DIR, 'index.html'), 'w') as f:
                f.write(content)
            # Render archive
            archive_template = env.get_template('archive.html')
            content = archive_template.render(
                posts=posts,
                config=config,
                root_path='../'
            )
            os.makedirs(os.path.join(BUILD_DIR, 'archive'), exist_ok=True)
            with open(os.path.join(BUILD_DIR, 'archive', 'index.html'), 'w') as f:
                f.write(content)
            # Render blog
            PAGINATION = 10
            num_pages = len(posts) // PAGINATION + 1
            for i in range(num_pages):
                blog_template = env.get_template('blog.html')
                prev_idx = i-1
                next_idx = i+1
                blog_posts = posts[PAGINATION*i:PAGINATION*(i+1)]
                has_next = next_idx*PAGINATION < len(posts)
                has_prev = prev_idx*PAGINATION >= 0
                if i == 0:
                    root_path = '../'
                    blog_path = os.path.join(BUILD_DIR, 'blog')
                else:
                    root_path = '../../../'
                    blog_path = os.path.join(BUILD_DIR, 'blog', 'page', str(i+1))
                content = blog_template.render(
                    posts=blog_posts,
                    config=config,
                    root_path=root_path,
                    prev_idx=prev_idx+1,
                    next_idx=next_idx+1,
                    has_prev=has_prev,
                    has_next=has_next,
                    PAGINATION=PAGINATION,
                )
                os.makedirs(blog_path, exist_ok=True)
                with open(os.path.join(blog_path, 'index.html'), 'w') as f:
                    f.write(content)

            # Copy static files into place
            shutil.copytree(STATIC_DIR, os.path.join(BUILD_DIR, 'static'))
            # Copy images into static dir
            os.makedirs(os.path.join(STATIC_DIR, 'img'), exist_ok=True)
            images_copied = {}
            for image in image_files:
                # Make sure the image name is unique
                image_basename = os.path.basename(image)
                if image_basename in images_copied:
                    raise ValueError('Image names must be unique regardless of directory. Duplicate image found:', image_basename)
                else:
                    images_copied[image_basename] = True
                # Copy it
                shutil.copy(image, os.path.join(BUILD_DIR, 'static', 'img', image_basename))
            # Generate pygments CSS
            formatter = HtmlFormatter()
            code_highlight_css = formatter.get_style_defs()
            with open(os.path.join(BUILD_DIR, 'static', 'code-highlights.css'), 'w') as f:
                f.write(code_highlight_css)
        else:
            print("Error: not a directory - %s" % gen_dir)
    else:
        print_usage()
