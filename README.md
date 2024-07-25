# SublimeGodot

Lightweight Sublime Text plugin adding some nice features to help with Godot game development.

## Features

- Syntax definitions for GDscript, GDExtension with C++, and markdown (to include GDscript).

- A command that can be used to display Godot documentation inside of sublime in a new tab in markdown format.  For this to work you will need to set the GodotDocumentationPath setting in the plugin settings to be the full path on your system to the `godot/doc/classes` folder inside of the [Godot repository](https://github.com/godotengine/godot/tree/master/doc/classes). You can also use the `godot --doctool [<path>]` command to generate the XML docs and save them to a path if you don't want to clone the Godot repository. To use type "Godot: Documentation" into the command palette and select the command, it will pull up a fuzzy search with all of Godot's classes, then just select a class to open it's documentation in sublime.

For the GDscript syntax it is just a updated version with the latest features of this one found here: https://github.com/beefsack/GDScript-sublime. You can also configure the LSP sublime plugin to use Godot's GDscript LSP in sublime for autocomplete, error checking and more nice features.

For the C++ syntax I added all of the core Godot Variant types to be highlighted by default just like other core C types are. You can also use the clangd LSP plugin alongside this to get all the C++ LSP features.

The way I convert the XML docs to markdown is super lazy and definitely not perfect so there may be some formatting issues or things that don't work like they should (like links to other documentation). If you notice any specific problems open an issue and I'll try to work it out.

Should work with any version of Godot.

## How to Install

Run the following script in the Sublime Text terminal ```(ctrl+` )``` which utilizes git clone for easy installation:
```
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/SublimeGodot', 'SublimeGodot'], 'working_dir': path})
```

Alternatively you can download the zip file from github and put the SublimeGodot folder (make sure it is named SublimeGodot) in the packages folder.
The packages folder can easily be found by going to ```preferences``` in the main menu and selecting ```Browse Packages```. The full path to the plugin should look like this:
```
C:\Users\YOURUSERNAME\AppData\Roaming\Sublime Text 3\Packages\SublimeGodot
```

## Other plugins
If you are going to do any kind of scripting in sublime I highly recommend installing and setting up these plugins:

- [Terminus](https://packagecontrol.io/packages/Terminus) - Fully working terminal directly in sublime text. Very useful for managing, running, or compiling your Godot project from directly in sublime.
- [LSP](https://packagecontrol.io/packages/LSP) - Language Server support that turns sublime into a full feature IDE for GDscript, C++, CSharp, or any other language.

## Screenshots

![Screenshot 1](/assets/1.png)

![Screenshot 2](/assets/2.png)