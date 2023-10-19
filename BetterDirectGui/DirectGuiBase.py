"""Module with subclass of DirectGuiWidget that implements keyboard navigation."""
from __future__ import annotations
import direct.gui.DirectGuiBase as DirectGuiBase
import direct.gui.DirectGuiGlobals as DGG

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
    base: ShowBase

__all__ = ["DirectGuiWidget"]


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

        self.bind(DGG.B1PRESS, self._set_active)

    def bind(self, event, command, extraArgs=[]):
        """Bind the command (which should expect one arg) to the specified
        event (such as ENTER, EXIT, B1PRESS, B1CLICK, etc.)
        See DirectGuiGlobals for possible events
        """
        if event == DGG.B1PRESS:  # Make sure _set_active still is bound
            def func(*args, **kwargs):
                if command != self._set_active:
                    command(*args, **kwargs)
                self._set_active(*args, **kwargs)
        else:
            func = command

        super().bind(event, func, extraArgs)

    def unbind(self, event):
        """Unbind the specified event"""
        super().unbind(event)
        if event == DGG.B1PRESS:  # Make sure _set_active is still bound
            self.bind(DGG.B1PRESS, self._set_active)

    def destroy(self):
        super().destroy()
        self["navigationMap"] = None

    def _set_active(self, event, skip_activate=True):
        print(event)
        print(base.gui_controller.current_selection)
        if self["selectable"]:
            if base.gui_controller.current_selection is not None and base.gui_controller.current_selection is not self:
                base.gui_controller.current_selection["selected"] = False

            base.gui_controller.current_selection = self
            if skip_activate:
                base.gui_controller._skip_activate = True
                print("call activate")
                base.gui_controller._activate()
                base.gui_controller._skip_activate = False
            else:
                base.gui_controller._activate()

    def navigate_next(self, direction: str = "f"):
        """Navigate to next gui element in 'direction'.
        If that element is not specified in navigationMap use default implementation to find the next element.

        :param direction: A string matching a key from the navigationMap dict (i.e. "f", "b", "i", "o").
        """
        option = self["navigationMap"][direction]
        if option is False:
            return

        if option is True:
            base.gui_controller._default_implementation(direction)
            return

        base.gui_controller.current_selection = option  # todo make sure this works (not tested)

    def override_navigation_map(self, direction: str, next_item: DirectGuiWidget):
        """Change keys and values in the navigationMap.

        :param direction: The direction to alter.
        :param next_item: The element to select when navigating in that direction.
        """
        nav_map = self["navigationMap"]
        nav_map[direction] = next_item
        opposite_direction = base.gui_controller.get_opposite_direction(direction)
        next_item["navigationMap"][opposite_direction] = self

    def set_selected(self):
        """Handle the state of self when selected/deselected."""
        if self["selected"]:
            self.activate()
            if not base.gui_controller._skip_activate:
                self.click()
        else:
            self.deactivate()
            if not base.gui_controller._skip_activate:
                self.unclick()

    def click(self):  # todo change name
        """Do the stuff that would normally happen when element is clicked.
        Is only called when navigating with keyboard.
        """
        print("click")

    def unclick(self):  # todo change name
        """Do stuff that would normally happen when user clicks away from element.
        Is only called when navigating with keyboard.
        """
        print("unclick")

    def activate(self):
        """Do the stuff that need to happen for element to be selected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        print("activate")

    def deactivate(self):
        """Do the stuff that need to happen for element to be deselected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        print("deactivate")

    def highlight(self):
        """Method to be called when element is selected to highlight it."""
        self.setColorScale(.5, 1, .5, 1)

    def unhighlight(self):
        """Method to be called when element is deselected to unhighlight it."""
        self.setColorScale(1, 1, 1, 1)
