# Bulwark

An Nmap scan aggregation tool, soon to bring many more features.

### VERSION 1.0 RELEASE

We have the full release of this finally. This has been kinda burning in my pocket for the past year, and I'm so glad to finally be able to release it completely. Don't get me wrong, this is definitely a rough cut. There are a bunch of ~~issues~~ not-yet-perfect bits of code. Read below as to how to use it without it breaking.


**THERE IS NO ERROR HANDLING IF YOU MAKE AN ERROR THE PROGRAM WILL CRASH**


##### How does it work?

Essentially, you take nmap scans and output them as xml files. On startup, there is an interactive shell that you control with arrow keys and enter. First thing you do, make a database. If you don't plan on using multiple databases, just use the default name of "bulwark", because it is much faster to have it like that. I can have a whole list of things that will be updated. There should be a gif below or something here to kinda show. There's not a ton of big info to put in here.


##### Installing

Either there will be the portable .exe in releases, or you can download the source code and run it there. Make sure to "pip install -r requirements.txt" before you run it.


##### Example

![] (Readme_Resources/example.gif)
