# templates

The base template is directly in the templates directory.
To keep the others organized, the templates for a blueprint will be placed in a directory with the same name as the blueprint.

In Flask, Jinja is configured to autoescape any data that is rendered in HTML templates.
This means that it’s safe to render user input; any characters they’ve entered that could
mess with the HTML, such as < and > will be escaped with safe values that look the same in
the browser but don’t cause unwanted effects.

Special delimiters are used to distinguish Jinja syntax from the static data in the template.
Anything between {{ and }} is an expression that will be output to the final document.
{% and %} denotes a control flow statement like if and for.
