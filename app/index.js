#!/usr/bin/env node

const path = require('path');

function print_usage() {
    console.error('Usage: sitegen <content_dir>');
}

function main() {
    // note: eventually can use 'yargs' pkg to add more functionality / CLI options
    let args = process.argv.slice(2);
    
    if (args.length != 1) {
        print_usage();
        return;
    }

    let content_dir = path.resolve(args[0]);
    console.log(content_dir);
}
main();
