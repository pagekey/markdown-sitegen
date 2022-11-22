var React = require('react');

module.exports = function(props) {
    console.log(props,'oi');
    return (
        <div>
            <h1>props.title! {props.title}</h1>
            <p>Here is a paragraph about it</p>
        </div>
    );
}
