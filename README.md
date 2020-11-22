# CS50w 2020 - Project 1 - Wiki
https://cs50.harvard.edu/web/2020/projects/1/wiki/

Design a Wikipedia-like online encyclopedia.
Background

Wikipedia is a free online encyclopedia that consists of a number of encyclopedia entries on various topics.

Each encyclopedia entry can be viewed by visiting that entry’s page. Visiting https://en.wikipedia.org/wiki/HTML, for example, shows the Wikipedia entry for HTML. Notice that the name of the requested page (HTML) is specified in the route /wiki/HTML. Recognize too, that the page’s content must just be HTML that your browser renders.

In practice, it would start to get tedious if every page on Wikipedia had to be written in HTML. Instead, it can be helpful to store encyclopedia entries using a lighter-weight human-friendly markup language. Wikipedia happens to use a markup language called Wikitext, but for this project we’ll store encyclopedia entries using a markup language called Markdown.

Read through GitHub’s Markdown guide to get an understanding for how Markdown’s syntax works. Pay attention in particular to what Markdown syntax looks like for headings, bold text, links, and lists.

By having one Markdown file represent each encyclopedia entry, we can make our entries more human-friendly to write and edit. When a user views our encyclopedia entry, though, we’ll need to convert that Markdown into HTML before displaying it to the user.
