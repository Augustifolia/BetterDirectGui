"""Drag and drop system. DraggableItems can be dragged between DraggableTiles in the same group."""
from BetterDirectGui.DirectGui.DirectButton import DirectButton
from BetterDirectGui.DirectGui import DGG


__all__ = ["DraggableItem", "DraggableTile"]


class DraggableTile(DirectButton):
    """
    A Widget that DraggableItems can be placed in by dropping them on the DraggableTile.

    Only Tiles and Items with the same 'group' number interact with each other.
    The 'content' of the Tile is the item that is currently placed in it.
    If self contains no item, 'content' will be 'None' instead.
    """
    _target = None

    def __init__(self, parent=None, **kw):
        optiondefs = (
            # All DraggableTiles and DraggableItems with the same number can interact with each other.
            ('group',           0,          None),
            # The item that is placed at this tile, if self is empty this is 'None'.
            ('content',         None,       self._addItem),
            ('selectable',      False,      None),
            ('frameSize', [-.1, .1, -.1, .1], None),
        )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectButton.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DraggableTile)

        # Set up stuff related to drag and drop
        self.bind(DGG.WITHIN, self._handle_target, extraArgs=["in"])
        self.bind(DGG.WITHOUT, self._handle_target, extraArgs=["out"])

        # Apply the theme to self
        self.add_theming_options(kw, parent, DraggableTile)

    def addItem(self, item):
        """Convenience method to add some content widget to self.

        The item should be of type 'DraggableItem' for drag and drop to work properly.
        """
        self["content"] = item

    def _handle_target(self, toggle, _):
        if toggle == "in":
            self.__class__._target = self
        elif toggle == "out" and self._target == self:
            self.__class__._target = None

    def _addItem(self):
        item = self["content"]
        if item is None:
            return

        item.reparentTo(self)
        item.setPos(item["placementOffset"][0], 0, item["placementOffset"][1])


class DraggableItem(DirectButton):
    """
    An item that can be dragged and dropped in different DraggableTiles.

    Make sure that you add your Item to a Tile by using:
        yourTile["content"] = yourItem

    Use 'placementOffset' to position the Item in its' Tile.

    Only Tiles and Items with the same 'group' number interact with each other.
    If you add some child widget to this item,
    make sure that the child does not interfere with mouse events sent to the item.
    """
    def __init__(self, parent=None, **kw):
        optiondefs = (
            # All DraggableTiles and DraggableItems with the same number can interact with each other.
            ('group',           0,         None),
            ('selectable',      True,      None),
            # An offset to apply to the items placement in a tile.
            ('placementOffset', (0, 0),    None),
        )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectButton.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DraggableItem)

        # Set up some stuff for drag and drop
        self._is_dragged = False
        self._old_parent = None
        self.bind(DGG.B1PRESS, self._grab)
        self.bind(DGG.B1RELEASE, self._release)

        # Apply the theme to self
        self.add_theming_options(kw, parent, DraggableItem)

    def _grab(self, _):
        if self._is_dragged:
            return

        self._is_dragged = True
        self._old_parent = base.gui_controller._get_gui(self.parent)
        assert self._old_parent is not None, f"{self} has an invalid parent node. It should be parented to a 'DraggableTile'"

        self.reparentTo(base.aspect2d)
        self.addTask(self._drag_task, "drag")

    def _release(self, _):
        if not self._is_dragged:
            return

        self._is_dragged = False
        new_parent = DraggableTile._target

        if new_parent is not None and new_parent["group"] != self["group"]:
            new_parent = None

        self.removeTask("drag")
        self.setPos(self["placementOffset"][0], 0, self["placementOffset"][1])

        if new_parent is None:
            new_parent = self._old_parent
        else:
            if new_parent["content"] is not None:
                self._old_parent["content"] = new_parent["content"]
            else:
                self._old_parent["content"] = None

        new_parent["content"] = self

    def _drag_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
        else:
            return task.cont

        self.setPos(base.render2d, x, 0, y)
        return task.cont
