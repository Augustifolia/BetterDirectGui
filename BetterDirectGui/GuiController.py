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
    def __init__(self, base_np: p3d.NodePath = None, respect_sortOrder=True, do_bug_fixes=False):
        super().__init__()
        base.gui_controller = self
        self.respect_sortOrder = respect_sortOrder
        self.guiItems = DirectGuiBase.DirectGuiWidget.guiDict
        base._do_bug_fixes = do_bug_fixes

        self.skip_activate = False

        if base_np is None:
            base_np = base.aspect2d
        self.base_np = base_np
        self._current_selection: DirectGuiBase.DirectGuiWidget | None = None
        self._current_pos: DirectGuiBase.DirectGuiWidget | None = None

        self._mouse_current_selection: DirectGuiBase.DirectGuiWidget | None = None

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

        self.activate_keys()

        # todo not activate if user clicks enter while doing something else (in directEntry for example)
        self.accept("enter", self.activate)
        # self.accept("f", self.test)

        # base.messenger.toggle_verbose()

    def test(self):
        print(self.guiItems, "\n", DirectGuiBase.DirectGuiWidget.guiDict)

    def update_key_map(self, key_map: dict[str, bool | Iterable | Callable]):
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

    def activate_keys(self):
        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.accept(value[0], self.navigate_next, extraArgs=[key])

    def deactivate_keys(self):
        for key, value in self.key_map.items():
            if isinstance(value, tuple):
                self.ignore(value[0])

    def navigate_next(self, direction: str):
        if self.current_selection is None:
            self.default_implemetation(direction)

        elif hasattr(self.current_selection, "navigate_next"):
            self.current_selection.navigate_next(direction)

        else:
            self.default_implemetation(direction)

    def default_implemetation(self, direction: str):
        option = self.key_map[direction]
        if option is False:
            return

        option[1]()

    @property
    def current_selection(self):
        return self._current_selection

    @current_selection.setter
    def current_selection(self, value: DirectGuiBase.DirectGuiWidget | None):
        if self._current_selection is not None:
            if hasattr(self._current_selection, "unhighlight"):
                self._current_selection.unhighlight()

            else:
                self.unhighlight(self._current_selection)

        self._current_selection = value
        if self._current_selection is not None:
            if hasattr(self._current_selection, "highlight"):
                self._current_selection.highlight()

            else:
                self.highlight(self._current_selection)

        print("current_selection", value)

    @staticmethod
    def highlight(gui: DirectGuiBase.DirectGuiWidget):
        gui.setColorScale(.5, 1, .5, 1)

    @staticmethod
    def unhighlight(gui: DirectGuiBase.DirectGuiWidget):
        gui.setColorScale(1, 1, 1, 1)

    def has_option(self, gui: DirectGuiBase.DirectGuiWidget, option: str) -> bool:
        try:
            gui[option]

        except Exception:
            print(option, "ex")
            return False

        print(option, "y")
        return True

    def activate(self):
        if self.current_selection is None:
            return

        if self._mouse_current_selection is not None: # and self._mouse_current_selection is not self.current_selection:
            print(self._mouse_current_selection, "mouse current selection")
            return

        c = self.current_selection
        if self.has_option(c, "selected"):
            c["selected"] = not c["selected"]
            if c["selected"]:
                print("sel")
                self.deactivate_keys()
            else:
                print("unsel")
                self.activate_keys()

        else:
            print("object has no option 'selected'")

    def get_guiId(self, np: p3d.NodePath) -> str | None:
        name = np.getName().split("-")
        if len(name) < 2:
            return None

        return name[1]

    def get_gui(self, np: p3d.NodePath) -> DirectGuiBase.DirectGuiWidget | None:
        guiId = self.get_guiId(np)
        if guiId is None:
            return None

        if guiId in self.guiItems:
            return self.guiItems[guiId]

        return None

    def is_gui(self, np: p3d.NodePath) -> bool:
        name = np.getName().split("-")
        if len(name) < 2:
            return False

        name = name[1]
        if name in self.guiItems:
            return True

        return False

    def is_selectable_gui(self, np: p3d.NodePath) -> bool:
        if (gui := self.get_gui(np)) is None:
            return False

        try:
            if gui["selectable"] and not np.isHidden() and not np.isStashed():
                return True
        except:
            return False

        return False

    def has_gui(self, np: p3d.NodePath = None) -> bool:
        def helper(node_path: p3d.NodePath):
            if self.is_gui(node_path):
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

    def has_selectable_gui(self, np: p3d.NodePath = None) -> bool:
        def helper(node_path: p3d.NodePath):
            if self.is_selectable_gui(node_path):
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

    def get_gui_children(self, np: p3d.NodePath) -> list[p3d.NodePath]:
        children = np.get_children()
        children_list = []
        for child in children:
            if self.is_gui(child):
                children_list.append(self.get_gui(child))

        if self.respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)

        return children_list

    def get_selectable_gui_children(self, np: p3d.NodePath) -> list[p3d.NodePath]:
        children = np.get_children()
        children_list = []
        for child in children:
            if self.is_selectable_gui(child):
                children_list.append(self.get_gui(child))

        if self.respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)

        return children_list

    def get_next_on_level(self, parent: p3d.NodePath = None,
                          skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self.base_np
            else:
                parent = self.current_selection.parent

        if not self.has_gui(parent):
            return None

        children = self.get_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if self.has_selectable_gui(child) and child != skip_np:
                    next_item = self.get_next_on_level(child)

                elif index + 1 >= len(children):
                    if parent == self.base_np:
                        next_item = children[0]
                    else:
                        return None
                else:
                    next_item = children[index + 1]

        if next_item == self.current_selection:
            return None

        return self.get_gui(next_item)

    def get_previous_on_level(self, parent: p3d.NodePath = None,
                              skip_np: p3d.NodePath = None) -> DirectGuiBase.DirectGuiWidget | None:

        if parent is None:
            if self.current_selection is None:
                parent = self.base_np
            else:
                parent = self.current_selection.parent

        if not self.has_gui(parent):
            return None

        children = self.get_gui_children(parent)
        next_item = children[-1]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index == 0:
                    if parent == self.base_np:
                        # next_item = children[-1]
                        self.current_selection = None
                        next_item = self.get_previous_on_level()
                    else:
                        if self.is_selectable_gui(parent):
                            next_item = self.get_gui(parent)
                        else:
                            self.current_selection = self.get_gui(parent)
                            next_item = self.get_previous_on_level(parent.parent)

                else:
                    next_item = children[index - 1]
                    if self.has_selectable_gui(next_item) and next_item != skip_np:
                        next_item = self.get_previous_on_level(next_item)

        if next_item == self.current_selection:
            return None

        return self.get_gui(next_item)

    def next_selectable_gui(self):
        next_item = self.get_next_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            while True:
                if next_item is None:
                    self.current_selection = self.get_gui(self._current_selection.parent)
                    if self.current_selection is not None:
                        next_item = self.get_next_on_level(self.current_selection.parent, skip_np=self.current_selection)

                    else:
                        next_item = self.get_next_on_level()

                else:
                    break

            if not self.is_selectable_gui(next_item):
                if self.has_selectable_gui(next_item):
                    next_item = self.get_next_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self.get_next_on_level(next_item.parent)
            else:
                break

        self.current_selection = next_item

    def previous_selectable_gui(self):
        next_item = self.get_previous_on_level()
        if next_item is None and self.current_selection is None:
            return

        while True:
            if next_item is None:
                self.current_selection = self.get_gui(self._current_selection.parent)
                next_item = self.get_previous_on_level(self.current_selection.parent, skip_np=self.current_selection)

            if not self.is_selectable_gui(next_item):
                if self.has_selectable_gui(next_item):
                    next_item = self.get_previous_on_level(next_item)
                else:
                    self.current_selection = next_item
                    next_item = self.get_previous_on_level(next_item.parent)
            else:
                break

        self.current_selection = next_item

    def move_next_current_level(self):
        if self.current_selection is None:
            next_item = self.get_selectable_gui_children(self.base_np)[0]
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = self.current_selection.parent
        children = self.get_selectable_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index + 1 >= len(children):
                    next_item = children[0]
                else:
                    next_item = children[index + 1]

        self.current_selection = next_item

    def move_previous_current_level(self):
        if self.current_selection is None:
            next_item = self.get_selectable_gui_children(self.base_np)[-1]
            if next_item is None:
                return

            self.current_selection = next_item
            return

        parent = self.current_selection.parent
        children = self.get_selectable_gui_children(parent)
        next_item = children[0]
        for index, child in enumerate(children):
            if child == self.current_selection:
                if index == 0:
                    next_item = children[-1]

                else:
                    next_item = children[index - 1]

        self.current_selection = next_item

    def parent_selectable_gui(self):
        if self.current_selection is None:
            return

        parent = self.current_selection.parent
        if parent == self.base_np:
            return

        if self.is_selectable_gui(parent):
            self.current_selection = self.get_gui(parent)
            return

        children = self.get_gui_children(parent.parent)
        og_parent = parent
        for _ in range(500):
            if self.is_selectable_gui(parent):
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

            if parent == self.base_np:
                return

        self.current_selection = parent

    def child_selectable_gui(self):
        if self.current_selection is None:
            child = self.get_next_on_level()
            print(child)
            if child is None:
                return

            if self.is_selectable_gui(child):
                self.current_selection = child
                return
            else:
                self.current_selection = child
                self.child_selectable_gui()
                return

        if self.has_selectable_gui(self.current_selection):
            child = self.get_next_on_level(self.current_selection)
            if child is None:
                return

            self.current_selection = child
            return

        children = self.get_gui_children(self.current_selection.parent)
        for child in children:
            if self.has_selectable_gui(child):
                guis = self.get_selectable_gui_children(child)
                child = guis[0]
                self.current_selection = child
                break
