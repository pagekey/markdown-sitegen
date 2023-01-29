#!/usr/bin/env node

import * as ReactDOMServer from 'react-dom/server';
import * as fs from 'fs';
import * as path from 'path';
import {evaluateSync} from '@mdx-js/mdx';
import * as runtime from 'react/jsx-runtime'

// import * as Home from './web/Home';

// const React = require('react');
// const mdx = require('@mdx-js/mdx');

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

    // Get .sitegenignore path
    let sitegenignore = [];
    const sitegenignore_path = path.join(content_dir, '.sitegenignore');
    if (fs.existsSync(sitegenignore_path)) {
        sitegenignore = fs.readFileSync(sitegenignore_path, 'utf-8').split('\n');
    }

    // Gather all markdown file paths
    let markdown_files = [];
    const handleDir = (directory, fileList) => {
        fs.readdirSync(directory).forEach((filename) => {
            if (sitegenignore.includes(filename)) {
                return; // skip
            }
            let full_filename = path.join(directory, filename);
            if (fs.lstatSync(full_filename).isDirectory()) {
                handleDir(full_filename, fileList);
            } else {
                if (full_filename.endsWith('.md')) {
                    fileList.push(full_filename);
                }
            }
        });
    }
    handleDir(content_dir, markdown_files);
    markdown_files.forEach((filename) => {
        console.log(filename);
        const body = fs.readFileSync(filename);
        const out = evaluateSync(body, {
            ...runtime,
        }).default;
        console.log(out);
    });

    // Remove build dir
    let build_dir = './build';
    if (fs.existsSync(build_dir)) {
        fs.rmdirSync(build_dir, { recursive: true });
    }
    fs.mkdirSync(build_dir);

    // let index_content = ReactDOMServer.renderToString(
    //     React.createElement(Home, {})
    // );
    // fs.writeFileSync(path.join(build_dir, 'index.html'), index_content);

    return 0;
}
process.exit(main());
