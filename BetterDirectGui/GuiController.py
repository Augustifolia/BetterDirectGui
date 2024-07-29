"""Module for handling the added gui functionality."""
from __future__ import annotations

from direct.showbase.DirectObject import DirectObject
import panda3d.core as p3d
from BetterDirectGui import DirectGuiBase
from BetterDirectGui.GuiTools import GuiUtil

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
    :param no_initopts: Bool for making all initopts editable after gui creation.
    """

    gui_themes = None  # By default, no theme
    gui_theme_priority = -1

    def __init__(self, base_np: p3d.NodePath = None,
                 respect_sortOrder=False,
                 do_bug_fixes=True,
                 theme=None,
                 do_keyboard_navigation=True,
                 no_initopts=True,
                 default_option_menu=False):
        super().__init__()
        base.gui_controller = self
        self._respect_sortOrder = respect_sortOrder
        self._guiItems = DirectGuiBase.DirectGuiWidget.guiDict
        self._do_bug_fixes = do_bug_fixes
        self._default_option_menu = default_option_menu
        self._do_theming = True
        self._no_initopts = no_initopts
        if base_np is None:
            base_np = base.aspect2d
        self._base_np = base_np
        if theme is not None:
            self.set_theme(theme)

        self._skip_activate = False
        self._do_highlight = True

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
        self._activation_key = "enter"
        self._unhighlight_key = "mouse3"
        self._do_keyboard_navigation = do_keyboard_navigation

        self._allowed_during_active = ["f", "b"]  # the directions that can be used to navigate while some element is selected

        if do_keyboard_navigation:
            self.activate_keys()
            self.accept(self._activation_key, self._activate)
            self.accept(f"{self._activation_key}-repeat", self._activate)
            self.accept(self._unhighlight_key, self._unhighlight_when_no_key_nav, extraArgs=[])

        self.highlight_color = (0.7, 0.7, 0.7, 1)

    def set_theme(self, theme: dict, priority: int = 0):
        """Set the global theme. Theme is set for all DirectGui objects that are children of 'self.base_np'.

        :param theme: The new theme to set.
        :param priority: Priority value to override previous theme.
        """
        self.gui_themes = theme
        self.gui_theme_priority = priority
        children = GuiUtil.get_gui_children(self._base_np)
        for child in children:
            child.set_theme(theme, priority)

    def clear_theme(self):
        """Clear the global theme."""
        self.gui_themes = None
        self.gui_theme_priority = -1
        children = GuiUtil.get_gui_children(self._base_np)
        for child in children:
            child.clear_theme()

    @property
    def do_theming(self):
        """Is themeability turned on?"""
        return self._do_theming

    @property
    def default_option_menu(self):
        """Does DirectOptionMenus have their default appearance?"""
        return self._default_option_menu

    @property
    def key_map(self):
        """The map used to decide what keyboard keys will activate which functions when navigating the gui."""
        return self._key_map

    @property
    def allowed_directions_while_selected(self):
        """A list of the directions that are still active while some element is selected.
        By default, "f" and "b" is enabled (corresponding to "tab" and "shift-tab").
        This means that if you are writing in a DirectEntry you can navigate the text with the arrow keys,
        but still be able to jump to the next element with "tab".
        """
        return self._allowed_during_active

    @allowed_directions_while_selected.setter
    def allowed_directions_while_selected(self, new_list: list[str]):
        self._allowed_during_active = []
        for arg in new_list:
            if arg in self.key_map:
                self._allowed_during_active.append(arg)
            else:
                print(f"warning: '{arg}' is not an defined direction for keyboard navigation")

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

    @property
    def no_initopts(self):
        """Bool for making all initopts editable after gui creation."""
        return self._no_initopts

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

    def update_activation_key(self, key: str, include_repeat_event=True):
        """Used to set the key to press to activate the currently selected gui element.

        :param key: The new key.
        :param include_repeat_event: If gui:s should react to the activation key being held down.
        """
        self.ignore(self._activation_key)
        self.ignore(f"{self._activation_key}-repeat")
        self.accept(key, self._activate)
        if include_repeat_event:
            self.accept(f"{key}-repeat", self._activate)
        self._activation_key = key

    def update_unhighlight_key(self, key: str):
        """Used to set the key to press to unhighlight the currently selected gui. By default, mouse3.

        :param key: The new key.
        """
        self.ignore(self._unhighlight_key)
        self.accept(key, self._unhighlight_when_no_key_nav, extraArgs=[])
        self._unhighlight_key = key

    def _unhighlight_when_no_key_nav(self):
        if self.current_selection is not None:
            if hasattr(self.current_selection, "unhighlight"):
                self.current_selection.unhighlight()
            else:
                self._unhighlight(self.current_selection)

    def activate_keys(self):
        """Bind the keys in 'self.key_map' to the functions specified in 'self.key_map'."""
        for key in self._allowed_during_active:
            value = self.key_map[key]
            if isinstance(value, tuple):
                self.ignore(value[0])

        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.accept(value[0], self._navigate_next, extraArgs=[key])

    def deactivate_keys(self, current_selection=None):
        """Unbind the keys in 'self.key_map'."""
        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.ignore(value[0])

        for key in self._allowed_during_active:
            value = self.key_map[key]
            if isinstance(value, tuple):
                if current_selection is not None and not current_selection["allowExit"]:
                    continue
                self.accept(value[0], self._navigate_while_selected, extraArgs=[key])

    def _navigate_next(self, direction: str):
        if self.current_selection is None:
            self._default_implementation(direction)

        elif hasattr(self.current_selection, "navigate_next"):
            self.current_selection.navigate_next(direction)

        else:
            self._default_implementation(direction)

    def _navigate_while_selected(self, direction: str):
        if self.current_selection is not None:
            if not self.current_selection["allowExit"]:
                return

            if self.current_selection["selected"]:
                self._activate()

        self._navigate_next(direction)

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
        if self._current_selection is not None and hasattr(self._current_selection, "_optionInfo"):
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

        # print("current_selection", value)

    def _highlight(self, gui: DirectGuiBase.DirectGuiWidget):
        if not self.do_keyboard_navigation:
            return

        if not self._do_highlight:
            return

        gui._color_scale = gui.getColorScale()
        gui.setColorScale(*self.highlight_color)

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
            selected_element = self.current_selection
            c["selected"] = not c["selected"]
            if c["selected"]:
                self.deactivate_keys(selected_element)
            else:
                self.activate_keys()

        else:
            print("object has no option 'selected'")

    def _get_next_on_level(self, parent: p3d.NodePath = None,
                           skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self._base_np
            else:
                parent = GuiUtil.get_parent(self.current_selection)

        if not GuiUtil.has_gui(parent):
            return None

        children = GuiUtil.get_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if GuiUtil.has_selectable_gui(child) and child != skip_np:
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

        return GuiUtil.get_gui(next_item)

    def _get_previous_on_level(self, parent: p3d.NodePath = None,
                               skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self._base_np
            else:
                parent = GuiUtil.get_parent(self.current_selection)

        if not GuiUtil.has_gui(parent):
            return None

        children = GuiUtil.get_gui_children(parent)
        next_item = children[-1]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index == 0:
                    if parent == self._base_np:
                        # next_item = children[-1]
                        self.current_selection = None
                        next_item = self._get_previous_on_level()
                    else:
                        if GuiUtil.is_selectable_gui(parent):
                            next_item = GuiUtil.get_gui(parent)
                        else:
                            self.current_selection = GuiUtil.get_gui(parent)
                            next_item = self._get_previous_on_level(GuiUtil.get_parent(parent))

                else:
                    next_item = children[index - 1]
                    if GuiUtil.has_selectable_gui(next_item) and next_item != skip_np:
                        next_item = self._get_previous_on_level(next_item)

        if next_item == self.current_selection:
            return None

        return GuiUtil.get_gui(next_item)

    def _next_selectable_gui(self):
        next_item = self._get_next_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            while True:
                if next_item is None:
                    self.current_selection = GuiUtil.get_gui(GuiUtil.get_parent(self._current_selection))
                    if self.current_selection is not None:
                        next_item = self._get_next_on_level(GuiUtil.get_parent(self.current_selection),
                                                            skip_np=self.current_selection)

                    else:
                        next_item = self._get_next_on_level()

                else:
                    break

            if not GuiUtil.is_selectable_gui(next_item):
                if GuiUtil.has_selectable_gui(next_item):
                    next_item = self._get_next_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self._get_next_on_level(GuiUtil.get_parent(next_item))
            else:
                break

        self.current_selection = next_item

    def _previous_selectable_gui(self):
        next_item = self._get_previous_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            if next_item is None:
                self.current_selection = GuiUtil.get_gui(GuiUtil.get_parent(self._current_selection))
                next_item = self._get_previous_on_level(GuiUtil.get_parent(self.current_selection),
                                                        skip_np=self.current_selection)

            if not GuiUtil.is_selectable_gui(next_item):
                if GuiUtil.has_selectable_gui(next_item):
                    next_item = self._get_previous_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self._get_previous_on_level(GuiUtil.get_parent(next_item))
            else:
                break

        self.current_selection = next_item

    def _move_next_current_level(self):
        if self.current_selection is None:
            next_item = GuiUtil.get_selectable_gui_children(self._base_np)
            if next_item:
                next_item = next_item[0]
            else:
                return
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = GuiUtil.get_parent(self.current_selection)
        children = GuiUtil.get_selectable_gui_children(parent)
        next_item = children[0]  # todo this list might be empty
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index + 1 >= len(children):
                    next_item = children[0]
                else:
                    next_item = children[index + 1]

        self.current_selection = next_item

    def _move_previous_current_level(self):
        if self.current_selection is None:
            next_item = GuiUtil.get_selectable_gui_children(self._base_np)
            if next_item:
                next_item = next_item[-1]
            else:
                return
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = GuiUtil.get_parent(self.current_selection)
        children = GuiUtil.get_selectable_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                next_item = children[index - 1]

        self.current_selection = next_item

    def _parent_selectable_gui(self):
        if self.current_selection is None:
            return

        parent = GuiUtil.get_parent(self.current_selection)
        if parent == self._base_np:
            return

        if GuiUtil.is_selectable_gui(parent):
            self.current_selection = GuiUtil.get_gui(parent)
            return

        children = GuiUtil.get_gui_children(GuiUtil.get_parent(parent))
        og_parent = parent
        for _ in range(500):
            if GuiUtil.is_selectable_gui(parent):
                break

            for index, child in enumerate(children):
                if child == parent:
                    parent = children[index - 1]
                    break

            if parent == og_parent:
                parent = GuiUtil.get_parent(parent)

            if parent == self._base_np:
                return

        else:  # no valid parent was found
            return

        self.current_selection = parent

    def _child_selectable_gui(self):
        if self.current_selection is None:
            child = self._get_next_on_level()
            if child is None:
                return

            if GuiUtil.is_selectable_gui(child):
                self.current_selection = child
                return
            else:
                self.current_selection = child
                self._child_selectable_gui()
                return

        if GuiUtil.has_selectable_gui(self.current_selection):
            child = self._get_next_on_level(self.current_selection)
            if child is None:
                return

            self.current_selection = child
            return

        children = GuiUtil.get_gui_children(GuiUtil.get_parent(self.current_selection))
        for child in children:
            if GuiUtil.has_selectable_gui(child):
                guis = GuiUtil.get_selectable_gui_children(child)
                child = guis[0]
                self.current_selection = child
                break
