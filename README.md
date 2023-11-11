# BetterDirectGui
Project to make it easier to work with DirectGui in Panda3d.

Right now only keyboard navigation and themability is implemented, but some other features are planed.

# Usage:
## Keyboard Navigation:
To use the keyboard navigation call `BetterDirectGui.init()` after initializing `Showbase`.
Then you can create your gui using the classes in `BetterDirectGui.DirectGui`.

```
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui

# import the DirectGui classes that you need from BetterDirectGui.DirectGui
# (the normal DirectGui classes will not work with keyboard navigation)
from BetterDirectGui import DirectGui


ShowBase()  # ShowBase must be initialized before BetterDirectGui
BetterDirectGui.init()  # initialize BetterDirectGui before creating any guis

# create some gui
b1 = DirectGui.DirectButton(text="button1", scale=0.2, pos=(-0.4, 0, 0.4))
b2 = DirectGui.DirectButton(text="button2", scale=0.2, pos=(0.4, 0, 0.4))
b3 = DirectGui.DirectButton(text="button3", scale=0.2, pos=(-0.4, 0, 0))
b4 = DirectGui.DirectButton(text="button4", scale=0.2, pos=(0.4, 0, 0))

base.run()
```
By default, BetterDirectGui will use the scene-graph to infer the jump order for keyboard navigation.

Use tab and shift-tab to cycle through all elements in the gui.
The arrow keys arrow_left and arrow_right will cycle through the elements at that level in the scene-graph.
The arrow keys arrow_up and arrow_down will move up or down the scene-graph (to the parent or child of the selected element).

To change how inputs are handled, you need to override the `key_map` in the `GuiController`.
By default, the `key_map` is:
```
self.key_map = {
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
self.update_key_map({
    "f": ("some_key", some_func),
    "b": False
    }
)
```
This will change the specified directions and leave all other directions unaltered.

To change how a specific gui element is handled, 
change its `navigationMap` (accessed with `your_gui["navigationMap"]`) which by default is defined as:
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
False for disabled.
To specify a jump explicitly, pass the object that should be jumped to.

## Themability:
A global theme is best set at init time:
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

To specify a theme for some gui elements, use the method:
`some_element.set_theme(theme, 1)`
Where the second parameter is a priority value used to decide if the new theme will override the old theme or not.

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

One limitation of changing the theme on some element after it was created is that any init options specified in the theme will not be changed. 
However, if you for example set a global theme and then create some element all parameters set in the theme should be set for the element.

To remove a theme globally or from a specific element, use `base.gui_controller.clear_theme()` or `some_element.clear_theme()` respectively.
Just like `set_theme` this will propagate down the scene-graph.

# Requirements:

* Panda3d
