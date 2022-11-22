#!/usr/bin/env node

require('babel-register')({
    presets: ['react'],
});

const ejs = require('ejs');
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
    let config_path = path.join(content_dir, 'sitegen.json');
    if (!fs.existsSync(config_path)) {
        console.error('Config file not found: ' + config_path);
        return 1;
    }
    let config_str = fs.readFileSync(config_path);
    let config = JSON.parse(config_str);
    console.log(config);

    // Remove build dir
    let build_dir = './build';
    if (fs.existsSync(build_dir)) {
        fs.rmdirSync(build_dir, { recursive: true });
    }
    fs.mkdirSync(build_dir);

    let web_dir = path.join(__dirname, 'web');
    let index_content_raw = fs.readFileSync(path.join(web_dir, 'index.ejs')).toString();
    // let index_content = ejs.render(index_content_raw, {...config});
    let index_content = ReactDomServer.renderToString(
        React.createElement(Home)
    );
    fs.writeFileSync(path.join(build_dir, 'index.html'), index_content);

    return 0;
}
process.exit(main());
