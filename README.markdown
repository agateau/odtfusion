# Presentation

odtfusion lets you merge text files or fragment of text files in an
OpenDocument Text document.

To include files in a .odt:

- Create a .odt
- Add placeholders for the text files. Placeholders are paragraphs of the form:

    `${file.cpp}`

- Run odtfusion like this:

    `odtfusion.py input.odt output.odt dir-containing-text-files`

To include fragments of text files:

- Insert fragment delimiters in your text files. Fragment delimiters look like
  this:

    `/// my-fragment`

- In your odt-file, refer to the fragment by using a placeholder like this:

    `${file.cpp#my-fragment}`

# Future

I may add a way to specify custom placeholders in the future, as well as
content-specific fragment delimiters (for example using "### my-fragment" for
Python or shell scripts)

# Contact

- Mail: Aurélien Gâteau <aurelien.gateau@free.fr>
- github: <http://github.com/agateau/odtfusion>
