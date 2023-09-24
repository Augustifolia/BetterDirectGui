from __future__ import annotations
import direct.gui.DirectGuiBase as DirectGuiBase
from direct.showbase.ShowBase import ShowBase

base: ShowBase


class DirectGuiWidget(DirectGuiBase.DirectGuiWidget):
    """Subclass of DirectGuiWidget with keyboard navigation support."""

    def __init__(self, parent=None, **kw):
        # True for default implementation (using node-graph to infer jump order)
        # False for disabled
        # To specify a jump explicitly, pass the object that should be jumped to
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

        optiondefs = (
            ('selectable',     False,         None),
            ('selected',       False,         self.set_selected),
            ('navigationMap',  navigationMap, None)
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGuiBase.DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectGuiWidget)

        base.gui_controller.guiItems[self.guiId] = self

    def destroy(self) -> None:
        super().destroy()
        base.gui_controller.guiItems.pop(self.guiId)

    def navigate_next(self, direction: str = "f"):
        option = self["navigationMap"][direction]
        if option is False:
            return

        if option is True:
            base.gui_controller.default_implemetation(direction)
            return

        base.gui_controller.current_selection = option

    def override_navigation_map(self, direction: str, key: str = None, next_item: DirectGuiWidget = None):
        nav_map = self["navigationMap"]
        nav_map[direction] = (
            key if key is not None else nav_map[direction][0],
            next_item if next_item is not None else nav_map[direction][1]
        )

    def set_selected(self):
        if self["selected"]:
            self.activate()

        else:
            self.deactivate()

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")

    def highlight(self):
        self.setColorScale(.5, 1, .5, 1)

    def unhighlight(self):
        self.setColorScale(1, 1, 1, 1)
