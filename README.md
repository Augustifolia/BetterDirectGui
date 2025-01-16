# BetterDirectGui
Project to make it easier to work with DirectGui in Panda3d.
It supports keyboard navigation, themability, makes all INITOPT:s editable after widget creation and fixes some other minor issues.

# Usage:
## General:
To enable BetterDirectGui, call `BetterDirectGui.init()` after initializing `Showbase`.
Then you can create your gui using the classes in `BetterDirectGui.DirectGui`.

The example program below illustrates some of the stuff that can be done with BetterDirectGui.
```
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui

# import the DirectGui classes that you need from BetterDirectGui.DirectGui
# do not use the DirectGui classes from direct
from BetterDirectGui import DirectGui


ShowBase()  # ShowBase must be initialized before BetterDirectGui
BetterDirectGui.init()  # initialize BetterDirectGui before creating any guis

# create some gui
b1 = DirectGui.DirectButton(text="button1", scale=0.2, pos=(-0.4, 0, 0.4))
b2 = DirectGui.DirectButton(text="button2", scale=0.2, pos=(0.4, 0, 0.4))
b3 = DirectGui.DirectButton(text="button3", scale=0.2, pos=(-0.4, 0, 0))
b4 = DirectGui.DirectButton(text="button4", scale=0.2, pos=(0.4, 0, 0))

# any INITOPT:s can be set after creation:
b4["pos"] = (0.1, 0, 0.1)

# including some options that could not be set at all before:
b4["transparency"] = 1

# a theme can also be applied to some node:
theme = {
    "DirectButton": dict(
        borderWidth=(0.2, 0.2),
        pad=(0.2, 0.2),
        hpr=(0, 0, 30),
    ),
}
b3.set_theme(theme, 1)

# just press tab or shift-tab to jump between the elements. 
# press enter to "click" on the currently selected element.

base.run()
```

`BetterDirectGui.init()` also has some options that changes how BetterDirectGui works. By default, all features are enabled.

| Option Name            | Description                                                                                                                                                                          | Default value |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| do_keyboard_navigation | Toggle to disable keyboard navigation                                                                                                                                                | True          |   
| base_np                | The base node-path that keyboard navigation and global theming will "start" from. In other words: global themes and keyboard navigation will only affect the children of the base_np | aspect2d      |   
| respect_sortOrder      | This specifies whether keyboard navigation will sort elements according to their sortOrder, or if the order from np.getChildren() will be used                                       | False         |
| theme                  | A dict with the global theme to use                                                                                                                                                  | None          |
| no_initopts            | Setting to make (almost) all INITOPT:s editable after widget creation. It also affects some other options that did not have any affect when changed after widget creation            | True          |
| do_bug_fixes           | Is intended to fix some minor issues                                                                                                                                                 | True          |

## Keyboard Navigation:
By default, BetterDirectGui will use the scene-graph to infer the jump order for keyboard navigation.
This means that you do not have to do anything else to make keyboard navigation work. 
However, how you structure your scene-graph and the order that elements are created affects which order they will be jumped to.
For elements with the same parent node, the jump order will be determined by the order the elements was created in. 
So an easy way to change the order that they are jumped to is to just create them in that order.

If you want more control over the jump order. You can specify, per element, what elements should come after it.
In order to do that, 
change the elements `navigationMap` (accessed with `your_gui["navigationMap"]`) which by default is defined as:
```
navigationMap = {
    "u": True,  # 'up' move upward (by default upwards in the node-graph)
    "d": True,  # 'down' inverse of 'up'
    "l": True,  # 'left' move left (to next gui node at the current level of the node-graph)
    "r": True,  # 'right' inverse of 'left'
    "i": False,  # 'inward'
    "o": False,  # 'outward'

    "f": True,  # 'forward' move to next item (to next gui node in the node-graph)
    "b": True  # 'backward' inverse of 'forward' (backward in the node-graph)
}
```

True for default implementation (using the node-graph to infer jump order).
False for disabled (nothing happens if the user tries to navigate in that direction).
To specify a jump explicitly, pass the object that should be jumped to.

The default controls for navigation is as follows.
Use tab and shift-tab to cycle through all elements in the gui.
The arrow keys arrow_left and arrow_right will cycle through the elements at that level in the scene-graph.
The arrow keys arrow_up and arrow_down will move up or down the scene-graph (to the parent or child of the selected element).

To change how inputs are handled, you need to override the `key_map` in the `GuiController`.
By default, the `key_map` is:
```
base.gui_controller.key_map = {
    "u": ("arrow_up", self.parent_selectable_gui),  # 'up' move upward (by default upwards in the node-graph)
    "d": ("arrow_down", self.child_selectable_gui),  # 'down' inverse of 'up'
    "l": ("arrow_left", self.move_previous_current_level),  # 'left' move left (to next gui node at the current level of the node-graph)
    "r": ("arrow_right", self.move_next_current_level),  # 'right' inverse of 'left'
    "i": False,  # 'inward'
    "o": False,  # 'outward'

    "f": ("tab", self.next_selectable_gui),  # 'forward' move to next item (to next gui node in the node-graph)
    "b": ("shift-tab", self.previous_selectable_gui)  # 'backward' inverse of 'forward' (backward in the node-graph)
}
```
Where `False` means that the specified direction is disabled.
If a direction is enabled, 
it should have a tuple with a key to bind and the default function to call when that key is pressed.

To override the `key_map` use:

```
base.gui_controller.update_key_map({
    "f": ("some_key", some_func),
    "b": False
    }
)
```
This will change the specified directions and leave all other directions unaltered.

## Themability:
Theming makes it easier to customize the look of a GUI without having to set options for each element individually.
You can just set a theme at one time and all elements already created and any future elements created will follow that theme.
A global theme can be set at init time:
```
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui

# import the DirectGui classes that you need from BetterDirectGui.DirectGui
# (the normal DirectGui classes will not work with keyboard navigation or themability)
from BetterDirectGui import DirectGui

# An example of how to define a theme
theme = {
    "DirectButton": dict(
        borderWidth=(0.2, 0.2),
        pad=(0.2, 0.2),
        pos=(0, 0, 0),
        hpr=(0, 0, 30),
        scale=(0.1, 0.1, 0.1),
        text='button',
    ),
    "DirectFrame": dict(
        frameSize=(-1, 1, -0.5, 0.5),
        text="frame"
    )
}

ShowBase()  # ShowBase must be initialized before BetterDirectGui
BetterDirectGui.init(theme=theme)  # initialize BetterDirectGui before creating any guis

# create some gui, all parameters set in the theme will now be set for the created elements
b1 = DirectGui.DirectButton(text="button1", scale=0.2, pos=(-0.4, 0, 0.4))
f1 = DirectGui.DirectFrame(text="some text")  # setting some parameter explicitly will override the theme

base.run()
```
A global theme will apply to the entire scene-graph underneath the base-nodePath specified in `BetterDirectGui.init()` (by default this is aspect2d).

To specify a theme for some gui elements, use the method:
`some_element.set_theme(theme, 1)`
Where the second parameter is a priority value used to decide if the new theme will override the old theme or not.
This allows different themes on different parts of the scene-graph.

If you want to change the global theme at some later time, you can use:
`base.gui_controller.set_theme(theme, 1)`
Where `theme` would be defined as a dict with the element name as key and a dict of the options to set for that element type as the corresponding values.
```
# An example of how to define a theme
theme = {
    "DirectButton": dict(
        borderWidth=(0.2, 0.2),
        pad=(0.2, 0.2),
        pos=(0, 0, 0),
        hpr=(0, 0, 30),
        scale=(0.1, 0.1, 0.1),
        text='button',
    ),
    "DirectFrame": dict(
        frameSize=(-1, 1, -0.5, 0.5),
        text="frame"
    )
}
```
When a theme is set on some element, that theme will propagate down the scene-graph and set the theme for the children of the element (and their children and so on recursively).
When a theme is set globally, that theme will be set for all children of the base_np (specified in `BetterDirectGui.init`) recursively.

Themability relies on that all options for the gui-objects are editable after created. 
Otherwise, that option will not be set in the theme.
Therefore, it is recommended to keep the option `no_initopts` to True.

To remove a theme globally or from a specific element, use `base.gui_controller.clear_theme()` or `some_element.clear_theme()` respectively.
Just like `set_theme` this will propagate down the scene-graph.

# Requirements:

* Panda3d

# Building distributable with BetterDirectGui

To be able to use the default themes from `GuiTools.Themes.py`, you have to include the necessary assets. 
To do this, add 
```
'package_data_dirs': {"BetterDirectGui": [('BetterDirectGui/assets/*', 'BetterDirectGui/assets', {})]}
``` 
to your `setup.py` file.
