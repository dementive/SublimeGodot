# SublimeGodot

Adds syntax definitions for gdscript, GDExtension with C++, and markdown (to include gdscript).

Adds a new command that can be used to display Godot documentation inside of sublime in a new tab in markdown format.  For this to work you will need to set the GodotDocumentationPath setting in the plugin settings to be the full path on your system to the `godot/doc/classes` folder inside of the [godot repository](https://github.com/godotengine/godot/tree/master/doc/classes).

Just type in "Godot Documentation" into the command palette and select the command, it will pull up a fuzzy search with all of godot's classes, then just select a class to open it's documentation in sublime.

For the gdscript syntax it is just a updated version with the latest features of this one found here: https://github.com/beefsack/GDScript-sublime

For the C++ syntax I added all of the core godot Variant types to be highlighted by default just like other core C types are.