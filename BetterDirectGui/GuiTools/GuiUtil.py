"""Module with some functions that might be useful when dealing with gui widgets in the scene graph."""
from __future__ import annotations

import panda3d.core as p3d
from BetterDirectGui import DirectGuiBase


def get_all_gui() -> dict[str: DirectGuiBase.DirectGuiWidget]:
    """Get a dict of all existing directGui widgets.

    With guiId as keys and the widgets as values."""
    return DirectGuiBase.DirectGuiWidget.guiDict


def get_guiId(np: p3d.NodePath) -> str | None:
    """Get the 'guiId' of a node if it is a DirectGui widget,
    otherwise return 'None'."""
    name = np.getName().split("-")
    if len(name) < 2:
        return None

    return name[1]


def get_gui(np: p3d.NodePath) -> DirectGuiBase.DirectGuiWidget | None:
    """Return the directGui object corresponding with the nodePath passed.

    If hte gui object does not exist 'None' is returned instead."""
    guiId = get_guiId(np)
    if guiId is None:
        return None

    if guiId in get_all_gui():
        return get_all_gui()[guiId]

    return None


def is_gui(np: p3d.NodePath | None) -> bool:
    """Check if the given nodePath corresponds to a directGui object."""
    if np is None:
        return False

    name = np.getName().split("-")
    if len(name) < 2:
        return False

    name = name[1]
    if name in get_all_gui():
        return True

    return False


def is_selectable_gui(np: p3d.NodePath) -> bool:
    """Check if the np is 'selectable'. Meaning that it can currently be selected with keyboard navigation.
    (It should be visible and have the option 'selectable' set to True.)"""
    if (gui := get_gui(np)) is None:
        return False

    try:
        if gui["selectable"] and not np.isHidden() and not np.isStashed():
            return True

    except Exception as e:
        print(f"Warning: {e}. You might not be using the gui-classes from BetterDirectGui.DirectGui")
        return False

    return False


def has_gui(np: p3d.NodePath) -> bool:
    """Recursively check if there is a directGui object as a descendant to the np.
    If there are any directGui object below the np in the scene graph return True."""
    def _helper(node_path: p3d.NodePath):
        if is_gui(node_path):
            return True

        for child in node_path.get_children():
            b = _helper(child)
            if b:
                return b

        return False

    for c in np.get_children():
        if _helper(c):
            return True

    return False


def has_selectable_gui(np: p3d.NodePath) -> bool:
    """Does the same as 'has_gui', but instead searches for an object that is currently selectable."""
    def _helper(node_path: p3d.NodePath):
        if is_selectable_gui(node_path):
            return True

        for child in node_path.get_children():
            b = _helper(child)
            if b:
                return b

        return False

    for c in np.get_children():
        if _helper(c):
            return True

    return False


def get_gui_children(np: p3d.NodePath) -> list[DirectGuiBase]:
    """Return a list of the children of the np that are directGui objects."""
    children = np.get_children()
    children_list = []
    for child in children:
        if is_gui(child):
            children_list.append(get_gui(child))
        if child.name == "canvas_parent":
            new_list = get_gui_children(child.children[0])
            children_list.extend(new_list)

    try:
        if base.gui_controller.respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)
    except NameError:  # base is not initialized yet
        pass

    return children_list


def get_selectable_gui_children(np: p3d.NodePath) -> list[p3d.NodePath]:
    """Return a list of the children of the np that are currently selectable directGui objects."""
    children = np.get_children()
    children_list = []
    for child in children:
        if is_selectable_gui(child):
            children_list.append(get_gui(child))
        if child.name == "canvas_parent":
            new_list = get_selectable_gui_children(child.children[0])
            children_list.extend(new_list)

    try:
        if base.gui_controller.respect_sortOrder:
            children_list.sort(key=lambda c: c["sortOrder"], reverse=True)
    except NameError:  # base is not initialized yet
        pass

    return children_list


def get_parent(np: p3d.NodePath) -> p3d.NodePath:
    """Function to get the parent of given node,
    but it skips over any node called 'canvas'.

    This is useful to get the closest parent node that should be a gui widget."""
    parent = np.parent
    if parent.name == "canvas":
        parent = parent.parent.parent
    return parent
