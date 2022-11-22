# sitegen

This repo is a command-line tool to generate static sites used by PageKey.

It keeps presentation of content separate from the content itself, and tries to abstract it a step further, making the same sitegen able to make multiple PageKey sites/blogs even if the content is in a different language / is a different subject area.

## Getting Started

1. `npm install`

2. `npm link`

3. `sitegen ./path/to/content`

## Debugging

1. Insert `debugger;` in code

2. Run `node inspect app/index.js ./test/sample/sitegen.json`

3. CTRL-C twice when done.
