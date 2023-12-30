"""Module with subclass of DirectGuiWidget that implements keyboard navigation."""
from __future__ import annotations
import direct.gui.DirectGuiBase as DirectGuiBase
import direct.gui.DirectGuiGlobals as DGG
import panda3d.core as p3d

from typing import Any

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
            # Is this element able to be selected, or is it skipped when navigating with keyboard
            ('selectable',     False,         None),
            # Is this element the currently selected element (activates when user presses "enter")
            ('selected',       False,         self.set_selected),
            # if user should be able to exit this element with some key from "allowed_directions_while_selected" while this element is selected
            ('allowExit',      True,          None),
            # map to specify explicitly how to navigate from this element
            ('navigationMap',  navigationMap, None)
        )

        if base.gui_controller.no_initopts:
            optiondefs += (
                ('pos', None, self._set_pos),
                ('hpr', None, self._set_hpr),
                ('scale', None, self._set_scale),
                ('color', None, self._set_color),
                ('transparency', None, self._set_transparency),
                # Do events pass through this widget?
                ('suppressMouse', 1, self._suppress_mouse_and_keys),
                ('suppressKeys', 0, self._suppress_mouse_and_keys),
                ('enableEdit', 1, self._enable_edit),
            )

        # Do not override if it already exists
        if not hasattr(self, "_kw"):
            self._kw = {}
        if not hasattr(self, "_theme"):
            self._theme: dict[str, Any] | None = None
            self._theme_priority = -1

        # Merge keyword options with theme from gui_controller
        kw = self.add_theming_options(kw, parent)

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGuiBase.DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectGuiWidget)

        # make sure to update stuff for keyboard navigation when self is pressed with the mouse.
        self.bind(DGG.B1PRESS, self._set_active)

    def _set_pos(self):
        if self['pos']:
            self.setPos(self['pos'])

    def _set_hpr(self):
        if self['hpr']:
            self.setHpr(self['hpr'])

    def _set_scale(self):
        if self['scale']:
            self.setScale(self['scale'])

    def _set_color(self):
        if self['color']:
            self.setColor(self['color'])

    def _set_transparency(self):
        if self["transparency"] is not None:
            self.setTransparency(self["transparency"])

    def _enable_edit(self):
        # Is drag and drop enabled?
        if self['enableEdit'] and self.guiEdit:
            self.enableEdit()
        else:
            self.disableEdit()

    def _suppress_mouse_and_keys(self):
        # Set up event handling
        suppressFlags = 0
        if self['suppressMouse']:
            suppressFlags |= p3d.MouseWatcherRegion.SFMouseButton
            suppressFlags |= p3d.MouseWatcherRegion.SFMousePosition
        if self['suppressKeys']:
            suppressFlags |= p3d.MouseWatcherRegion.SFOtherButton
        self.guiItem.setSuppressFlags(suppressFlags)

    def set_theme(self, theme: dict, priority=0, clear_old_theme=True):
        """Set theme of this element and its children to the specified theme.

        :param theme: The new theme.
        :param priority: Requires a higher value than the current themes priority to override.
        :param clear_old_theme: Option to reset all options set by the old theme before setting the new one.
        """
        if priority <= self._theme_priority:
            return

        if clear_old_theme:
            self.clear_theme()

        self._theme_priority = priority
        self._theme = theme
        if type(self).__name__ in theme:
            gui_theme = theme[type(self).__name__]
            for key, value in gui_theme.items():
                if key in self._kw:
                    continue

                self[key] = value

        children = base.gui_controller._get_gui_children(self)
        for child in children:
            child.set_theme(theme, priority)

    def clear_theme(self):
        """Remove the theming options from this element and its children."""
        if self._theme is None:
            return

        for name, default, func in self.options():
            if name in self._theme[type(self).__name__] and name not in self._kw:
                self[name] = default

        self._theme_priority = -1
        self._theme = None

        children = base.gui_controller._get_gui_children(self)
        for child in children:
            child.clear_theme()

    def add_theming_options(self, kw: dict, parent: DirectGuiWidget | None):
        """Merge kw with the theming specified in guiController.

        :param parent: The parent element of self
        :param kw: The keywords given by the user.
        :return: kw
        """
        if not hasattr(self, "_kw"):
            self._kw = kw.copy()

        if not base.gui_controller._do_theming:
            return kw

        name = type(self).__name__
        if base.gui_controller._is_gui(parent) and parent._theme is not None:
            themes = parent._theme
            self._theme = themes
            self._theme_priority = parent._theme_priority

        elif base.gui_controller.gui_themes is not None and name in base.gui_controller.gui_themes:
            themes = base.gui_controller.gui_themes
            self._theme = themes
            self._theme_priority = base.gui_controller.gui_theme_priority

        else:
            return kw

        theme = {}
        if name in themes:
            theme = themes[name]

        kwargs = kw.copy()
        for key, value in theme.items():
            if key not in kwargs:
                kwargs[key] = value

        return kwargs

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

    def _set_active(self, event, skip_activate=True):
        if not base.gui_controller.do_keyboard_navigation:
            return

        if self["selectable"]:
            if base.gui_controller.current_selection is not None and base.gui_controller.current_selection is not self:
                base.gui_controller.current_selection["selected"] = False

            base.gui_controller.current_selection = self
            if skip_activate:
                base.gui_controller._skip_activate = True
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

        base.gui_controller.current_selection = option

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
            if not base.gui_controller._skip_activate:
                self.click()
            self.activate()
        else:
            if not base.gui_controller._skip_activate:
                self.unclick()
            self.deactivate()

    def click(self):
        """Do the stuff that would normally happen when element is clicked.
        Is only called when navigating with keyboard.
        """
        self.show_click()

    def show_click(self):
        """Show that the element is selected by changing its scale."""
        self._scale = self.get_scale()
        self.set_scale(self._scale * 0.98)

    def unclick(self):
        """Do stuff that would normally happen when user clicks away from element.
        Is only called when navigating with keyboard.
        """
        self.show_unclick()

    def show_unclick(self):
        """Reset the scale changed in show_click."""
        if hasattr(self, "_scale"):
            self.do_method_later(0.1, self.set_scale, "unclick", [self._scale])

    def activate(self):
        """Do the stuff that need to happen for element to be selected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        # print("activate")
        pass

    def deactivate(self):
        """Do the stuff that need to happen for element to be deselected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        # print("deactivate")
        pass

    def highlight(self):
        """Method to be called when element is the "current_selection"
        (not selected, just the current node for the GuiController) to highlight it."""
        self._color_scale = p3d.LVecBase4(self.getColorScale())
        self.setColorScale(*base.gui_controller.highlight_color)

    def unhighlight(self):
        """Method to be called when element is no longer the "current_selection"
        (not selected, just the current node for the GuiController) to unhighlight it."""
        if hasattr(self, "_color_scale"):
            self.set_color_scale(self._color_scale)
        else:
            self.setColorScale(1, 1, 1, 1)
