#!/usr/bin/env node

require('babel-register')({
    presets: ['react'],
});

const fs = require('fs');
const path = require('path');
const React = require('react');
const ReactDomServer = require('react-dom/server');
const Home = require('./web/Home');

function print_usage() {
    console.error('Usage: sitegen <content_dir>');
}

function main() {
    // note: eventually can use 'yargs' pkg to add more functionality / CLI options
    let args = process.argv.slice(2);
    
    if (args.length != 1) {
        print_usage();
        return 1;
    }

    let content_dir = path.resolve(args[0]);
    if (!fs.lstatSync(content_dir).isDirectory()) {
        console.error('Error: not a directory - ' + content_dir);
        return 1;
    }

    // Gather all markdown file paths
    let markdown_files = [];
    const handleDir = (directory, fileList) => {
        fs.readdirSync(directory).forEach((filename) => {
            full_filename = path.join(directory, filename);
            if (fs.lstatSync(full_filename).isDirectory()) {
                console.log('whoa');
            } else {
                if (full_filename.endsWith('.md')) {
                    console.log('ha! found one')
                    fileList.push(full_filename);
                }
            }
        });
        return fileList;
    }
    handleDir(content_dir, markdown_files);
    console.log(markdown_files);

    // Remove build dir
    let build_dir = './build';
    if (fs.existsSync(build_dir)) {
        fs.rmdirSync(build_dir, { recursive: true });
    }
    fs.mkdirSync(build_dir);

    let index_content = ReactDomServer.renderToString(
        React.createElement(Home, {})
    );
    fs.writeFileSync(path.join(build_dir, 'index.html'), index_content);

    return 0;
}
process.exit(main());
