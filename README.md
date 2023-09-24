# BetterDirectGui
Project to make it easier to work with DirectGui in Panda3d.

Right now only keyboard navigation is implemented. 
It is still early in development and not meant for production use yet.

# Usage:
To use the keyboard navigation call `BetterDirectGui.init()` after initializing `Showbase`.
Then you can create your gui using the classes in `BetterDirectGui.DirectGui`.

```
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui

# import the DirectGui classes that you need from BetterDirectGui.DirectGui
# (the normal DirectGui classes will not work with keyboard navigation)
from BetterDirectGui import DirectGui


base = ShowBase()  # ShowBase must be initialized before BetterDirectGui
BetterDirectGui.init()  # initialize BetterDirectGui before creating any guis

# create some gui
b1 = DirectGui.DirectButton(text="button1", scale=0.2, pos=(-0.4, 0, 0.4))
b2 = DirectGui.DirectButton(text="button2", scale=0.2, pos=(0.4, 0, 0.4))
b3 = DirectGui.DirectButton(text="button3", scale=0.2, pos=(-0.4, 0, 0))
b4 = DirectGui.DirectButton(text="button4", scale=0.2, pos=(0.4, 0, 0))

base.run()
```

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

# Requirements:

* Panda3d
