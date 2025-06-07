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

## Godot LSP setup

I highly recommend setting up LSP. The LSP built into Godot can be hooked up to sublime and provides a lot of really nice features like error checking, auto complete, goto definition, hover documentation, and more.

First you'll need to install the [LSP](https://packagecontrol.io/packages/LSP) plugin for sublime. Then go to `Preferences->Package Settings->LSP->Settings` this will open up the `LSP.sublime-settings` file.

Next you need to add the Godot client to your LSP configuration, here is an example configuration:

```
{
    "clients": 
    {
        "gdscript-lsp":
        {
            "enabled": true,
            "command": [
                "~/.local/bin/godot",
                "--editor",
                "~/path_to_your_project/project.godot",
                "--quiet",
                "--headless"
            ],
            "selector": "source.gdscript",
            "tcp_port": 6005
        }
    }
}
```

Replace the first argument in the "command" array with the actual path to the godot binary on your system. You'll also need to replace the third argument with the path to your project.godot file since by default godot opens the project selection list, so for the LSP to run it needs to actually run your project.

This setup is nice if you only work on one project but if you often move between different projects you might want to use a simpler configuration instead:
```
{
    "clients": 
    {
        "gdscript-lsp":
        {
            "enabled": true,
            "selector": "source.gdscript",
            "tcp_port": 6005
        }
    }
}
```

With this config the LSP will only work when you have your godot project open in the editor because it can't start the server itself, but the configuration is simpler and easier to setup.


## Godot Debugger setup

The [SublimeDebugger](https://github.com/daveleroy/SublimeDebugger) plugin adds support for the Debug Adapter Protocol, however it does not have direct support for the gdscript debugger, it is possible but im not sure how to set it up and have just used the gdscript debugger in the godot editor instead.

If you are trying to debug C++ SublimeDebugger can use either lldb or gdb for debugging. To setup lldb follow the instructions in the SublimeDebugger readme to install the adaptor and then add the following to your .sublime-project file:

```
"debugger_configurations":
[
    {
        "args": ["scenes/main.tscn"], // godot command line args, path to main scene to run.
        "cwd": "<path/to/project.godot folder>",
        "expressions": "simple",
        "name": "lldb",
        "program": "<path/to/godot binary>",
        "request": "launch",
        "sourceLanguages": ["cpp"],
        "type": "lldb"
    }
],
```

## Screenshots

![Screenshot 1](/assets/1.png)

![Screenshot 2](/assets/2.png)