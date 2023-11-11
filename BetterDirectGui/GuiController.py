"""Module for handling the added gui functionality."""
from __future__ import annotations

from direct.showbase.DirectObject import DirectObject
import panda3d.core as p3d
from BetterDirectGui import DirectGuiBase

from collections.abc import Iterable, Callable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
    base: ShowBase

__all__ = ["GuiController"]


class GuiController(DirectObject):
    """Class for handling the added gui functionality.

    :param base_np: The NodePath that keyboard navigation should start from.
    :param respect_sortOrder: If True: navigation will take into account the sort order of the gui elements
     when selecting the next element to jump to.
    :param do_bug_fixes: Changes some buggy behaviour in DirectGui.
    :param theme: The global theme used by all elements that are children of base_np.
    :param do_keyboard_navigation: Chose weather keyboard navigation is enabled.
    """

    # An example theme (useful for testing)
    gui_themes_ = {
        "DirectButton": dict(
            borderWidth=(0.2, 0.2),
            # frameColor=(.2, 1.0, 1.0, 1.0),
            pad=(0.2, 0.2),
            pos=(0, 0, 0),
            hpr=(0, 0, 30),
            scale=(0.1, 0.1, 0.1),
            text='button',
        ),
        "DirectFrame": dict(
            # frameSize=(-1, 1, -0.5, 0.5),
            text="frame"
        )
    }
    gui_themes = None  # By default, no theme
    gui_theme_priority = -1

    def __init__(self, base_np: p3d.NodePath = None, respect_sortOrder=True,
                 do_bug_fixes=False, theme=None, do_keyboard_navigation=True):
        super().__init__()
        base.gui_controller = self
        self._respect_sortOrder = respect_sortOrder
        self._guiItems = DirectGuiBase.DirectGuiWidget.guiDict
        self._do_bug_fixes = do_bug_fixes
        self._do_theming = True
        if theme is not None:
            self.set_theme(theme)

        self._skip_activate = False

        if base_np is None:
            base_np = base.aspect2d
        self._base_np = base_np
        self._current_selection: DirectGuiBase.DirectGuiWidget | None = None
        self._current_pos: DirectGuiBase.DirectGuiWidget | None = None

        self._key_map = {
            "u": ("arrow_up", self._parent_selectable_gui),  # 'up' move upward (by default upwards in the node-graph)
            "d": ("arrow_down", self._child_selectable_gui),  # 'down' inverse of 'up'
            "l": ("arrow_left", self._move_previous_current_level),  # 'left' move left (to next gui node at the current level of the node-graph)
            "r": ("arrow_right", self._move_next_current_level),  # 'right' inverse of 'left'
            "i": False,  # 'inward'
            "o": False,  # 'outward'

            "f": ("tab", self._next_selectable_gui),  # 'forward' move to next item (to next gui node in the node-graph)
            "b": ("shift-tab", self._previous_selectable_gui)  # 'backward' inverse of 'forward' (backward in the node-graph)
        }
        self._do_keyboard_navigation = do_keyboard_navigation

        if do_keyboard_navigation:
            self.activate_keys()
            self.accept("enter", self._activate)

        self.highlight_color = (0.7, 0.7, 0.7, 1)

    def set_theme(self, theme: dict, priority: int = 0):
        """Set the global theme. Theme is set for all DirectGui objects that are children of 'self.base_np'.

        :param theme: The new theme to set.
        :param priority: Priority value to override previous theme.
        """
        self.gui_themes = theme
        self.gui_theme_priority = priority
        children = self._get_gui_children(self._base_np)
        for child in children:
            child.set_theme(theme, priority)

    def clear_theme(self):
        """Clear the global theme."""
        self.gui_themes = None
        self.gui_theme_priority = -1
        children = self._get_gui_children(self._base_np)
        for child in children:
            child.clear_theme()

    @property
    def key_map(self):
        """The map used to decide what keyboard keys will activate which functions when navigating the gui."""
        return self._key_map

    @property
    def respect_sortOrder(self):
        """If True: navigation will take into account the sort order of the gui elements
        when selecting the next element to jump to.
        """
        return self._respect_sortOrder

    @property
    def do_bug_fixes(self):
        """Changes some buggy behaviour in DirectGui."""
        return self._do_bug_fixes

    @property
    def base_np(self):
        """The base nodepath for keyboard navigation and global theming. By default, it is aspect2d."""
        return self._base_np

    @property
    def do_keyboard_navigation(self):
        """Bool for if keyboard navigation is enabled."""
        return self._do_keyboard_navigation

    def get_opposite_direction(self, direction: str) -> str:
        """Get the opposite direction to the direction specified.
        For example "f" returns "b" and "u" would return "d".
        """
        string_list = [key for key in self._key_map]
        for index, value in enumerate(string_list):
            string = value[0]
            if direction != string:
                continue

            if index % 2 == 0:
                return string_list[index + 1]

            else:
                return string_list[index - 1]

    def _test(self):
        print(self._guiItems, "\n", DirectGuiBase.DirectGuiWidget.guiDict)

    def update_key_map(self, key_map: dict[str, bool | Iterable | Callable]):
        """Update 'self.key_map' with the values in 'key_map'.

        :param key_map: Dict of the stuff in 'self.key_map' that you want to update.
        """
        self.deactivate_keys()
        for key, value in key_map.items():
            if isinstance(value, bool) or isinstance(value, Iterable):
                self.key_map[key] = value

            elif isinstance(value, str):
                self.key_map[key] = (value, self.key_map[key][1])

            elif isinstance(value, Callable):
                self.key_map[key] = (self.key_map[key][0], value)

            else:
                raise TypeError(f"unsupported type {type(value)} for the key_map")

        self.activate_keys()

    def update_activation_key(self, key: str):
        """Used to set the key to press to activate the currently selected gui element.

        :param key: The new key.
        """
        self.accept(key, self._activate)

    def activate_keys(self):
        """Bind the keys in 'self.key_map' to the functions specified in 'self.key_map'."""
        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.accept(value[0], self._navigate_next, extraArgs=[key])

    def deactivate_keys(self):
        """Unbind the keys in 'self.key_map'."""
        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.ignore(value[0])

    def _navigate_next(self, direction: str):
        if self.current_selection is None:
            self._default_implementation(direction)

        elif hasattr(self.current_selection, "navigate_next"):
            self.current_selection.navigate_next(direction)

        else:
            self._default_implementation(direction)

    def _default_implementation(self, direction: str):
        option = self.key_map[direction]
        if option is False:
            return

        option[1]()

    @property
    def current_selection(self):
        """The currently selected gui."""
        return self._current_selection

    @current_selection.setter
    def current_selection(self, value: DirectGuiBase.DirectGuiWidget | None):
        if self._current_selection is not None:
            if hasattr(self._current_selection, "unhighlight"):
                self._current_selection.unhighlight()

            else:
                self._unhighlight(self._current_selection)

        self._current_selection = value
        if self._current_selection is not None:
            if hasattr(self._current_selection, "highlight"):
                self._current_selection.highlight()

            else:
                self._highlight(self._current_selection)

        print("current_selection", value)

    @staticmethod
    def _highlight(gui: DirectGuiBase.DirectGuiWidget):
        gui._color_scale = gui.getColorScale()
        gui.setColorScale(*base.gui_controller.highlight_color)

    @staticmethod
    def _unhighlight(gui: DirectGuiBase.DirectGuiWidget):
        if hasattr(gui, "_color_scale"):
            gui.set_color_scale(gui._color_scale)
        else:
            gui.setColorScale(1, 1, 1, 1)

    @staticmethod
    def _has_option(gui: DirectGuiBase.DirectGuiWidget, option: str) -> bool:
        try:
            gui[option]

        except Exception:
            return False

        return True

    def _activate(self):
        if self.current_selection is None:
            return

        c = self.current_selection
        if self._has_option(c, "selected"):
            c["selected"] = not c["selected"]
            print("selected" if c["selected"] else "unselected", c)
            if c["selected"]:
                self.deactivate_keys()
            else:
                self.activate_keys()

        else:
            print("object has no option 'selected'")

    @staticmethod
    def _get_guiId(np: p3d.NodePath) -> str | None:
        name = np.getName().split("-")
        if len(name) < 2:
            return None

        return name[1]

    def _get_gui(self, np: p3d.NodePath) -> DirectGuiBase.DirectGuiWidget | None:
        guiId = self._get_guiId(np)
        if guiId is None:
            return None

        if guiId in self._guiItems:
            return self._guiItems[guiId]

        return None

    def _is_gui(self, np: p3d.NodePath | None) -> bool:
        if np is None:
            return False

        name = np.getName().split("-")
        if len(name) < 2:
            return False

        name = name[1]
        if name in self._guiItems:
            return True

        return False

    def _is_selectable_gui(self, np: p3d.NodePath) -> bool:
        if (gui := self._get_gui(np)) is None:
            return False

        try:
            if gui["selectable"] and not np.isHidden() and not np.isStashed():
                return True

        except Exception:
            return False

        return False

    def _has_gui(self, np: p3d.NodePath = None) -> bool:
        def helper(node_path: p3d.NodePath):
            if self._is_gui(node_path):
                return True

            for child in node_path.get_children():
                b = helper(child)
                if b:
                    return b

            return False

        if np is None:
            np = self.current_selection

        for c in np.get_children():
            if helper(c):
                return True

        return False

    def _has_selectable_gui(self, np: p3d.NodePath = None) -> bool:
        def helper(node_path: p3d.NodePath):
            if self._is_selectable_gui(node_path):
                return True

            for child in node_path.get_children():
                b = helper(child)
                if b:
                    return b

            return False

        if np is None:
            np = self.current_selection

        for c in np.get_children():
            if helper(c):
                return True

        return False

    def _get_gui_children(self, np: p3d.NodePath) -> list[DirectGuiBase]:
        children = np.get_children()
        children_list = []
        for child in children:
            if self._is_gui(child):
                children_list.append(self._get_gui(child))

        if self._respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)

        return children_list

    def _get_selectable_gui_children(self, np: p3d.NodePath) -> list[p3d.NodePath]:
        children = np.get_children()
        children_list = []
        for child in children:
            if self._is_selectable_gui(child):
                children_list.append(self._get_gui(child))

        if self._respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)

        return children_list

    def _get_next_on_level(self, parent: p3d.NodePath = None,
                           skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self._base_np
            else:
                parent = self.current_selection.parent

        if not self._has_gui(parent):
            return None

        children = self._get_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if self._has_selectable_gui(child) and child != skip_np:
                    next_item = self._get_next_on_level(child)

                elif index + 1 >= len(children):
                    if parent == self._base_np:
                        next_item = children[0]
                    else:
                        return None
                else:
                    next_item = children[index + 1]

        if next_item == self.current_selection:
            return None

        return self._get_gui(next_item)

    def _get_previous_on_level(self, parent: p3d.NodePath = None,
                               skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self._base_np
            else:
                parent = self.current_selection.parent

        if not self._has_gui(parent):
            return None

        children = self._get_gui_children(parent)
        next_item = children[-1]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index == 0:
                    if parent == self._base_np:
                        # next_item = children[-1]
                        self.current_selection = None
                        next_item = self._get_previous_on_level()
                    else:
                        if self._is_selectable_gui(parent):
                            next_item = self._get_gui(parent)
                        else:
                            self.current_selection = self._get_gui(parent)
                            next_item = self._get_previous_on_level(parent.parent)

                else:
                    next_item = children[index - 1]
                    if self._has_selectable_gui(next_item) and next_item != skip_np:
                        next_item = self._get_previous_on_level(next_item)

        if next_item == self.current_selection:
            return None

        return self._get_gui(next_item)

    def _next_selectable_gui(self):
        next_item = self._get_next_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            while True:
                if next_item is None:
                    self.current_selection = self._get_gui(self._current_selection.parent)
                    if self.current_selection is not None:
                        next_item = self._get_next_on_level(self.current_selection.parent,
                                                            skip_np=self.current_selection)

                    else:
                        next_item = self._get_next_on_level()

                else:
                    break

            if not self._is_selectable_gui(next_item):
                if self._has_selectable_gui(next_item):
                    next_item = self._get_next_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self._get_next_on_level(next_item.parent)
            else:
                break

        self.current_selection = next_item

    def _previous_selectable_gui(self):
        next_item = self._get_previous_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            if next_item is None:
                self.current_selection = self._get_gui(self._current_selection.parent)
                next_item = self._get_previous_on_level(self.current_selection.parent, skip_np=self.current_selection)

            if not self._is_selectable_gui(next_item):
                if self._has_selectable_gui(next_item):
                    next_item = self._get_previous_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self._get_previous_on_level(next_item.parent)
            else:
                break

        self.current_selection = next_item

    def _move_next_current_level(self):
        if self.current_selection is None:
            next_item = self._get_selectable_gui_children(self._base_np)[0]
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = self.current_selection.parent
        children = self._get_selectable_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index + 1 >= len(children):
                    next_item = children[0]
                else:
                    next_item = children[index + 1]

        self.current_selection = next_item

    def _move_previous_current_level(self):
        if self.current_selection is None:
            next_item = self._get_selectable_gui_children(self._base_np)[-1]
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = self.current_selection.parent
        children = self._get_selectable_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index == 0:
                    next_item = children[-1]

                else:
                    next_item = children[index - 1]

        self.current_selection = next_item

    def _parent_selectable_gui(self):
        if self.current_selection is None:
            return

        parent = self.current_selection.parent
        if parent == self._base_np:
            return

        if self._is_selectable_gui(parent):
            self.current_selection = self._get_gui(parent)
            return

        children = self._get_gui_children(parent.parent)
        og_parent = parent
        for _ in range(500):
            if self._is_selectable_gui(parent):
                break

            for index, child in enumerate(children):
                if child == parent:
                    if index == 0:
                        parent = children[-1]
                    else:
                        parent = children[index - 1]
                    break

            if parent == og_parent:
                parent = parent.parent

            if parent == self._base_np:
                return

        self.current_selection = parent

    def _child_selectable_gui(self):
        if self.current_selection is None:
            child = self._get_next_on_level()
            if child is None:
                return

            if self._is_selectable_gui(child):
                self.current_selection = child
                return
            else:
                self.current_selection = child
                self._child_selectable_gui()
                return

        if self._has_selectable_gui(self.current_selection):
            child = self._get_next_on_level(self.current_selection)
            if child is None:
                return

            self.current_selection = child
            return

        children = self._get_gui_children(self.current_selection.parent)
        for child in children:
            if self._has_selectable_gui(child):
                guis = self._get_selectable_gui_children(child)
                child = guis[0]
                self.current_selection = child
                break
