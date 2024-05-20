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
            ('borderWidth', (.02, .02),       None),
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

        item.wrt_reparent_to(self)
        center_x, center_z = item.getCenterPosition()
        item.setPos(
            item["placementOffset"][0] - center_x,
            0,
            item["placementOffset"][1] - center_z
        )


class DraggableItem(DirectButton):
    """
    An item that can be dragged and dropped in different DraggableTiles.

    Make sure that you add your Item to a Tile by using:
        yourTile["content"] = yourItem

    Use 'placementOffset' to adjust the Item position in its' Tile. It should automatically be centered.

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
        self._task = None
        self.bind(DGG.B1PRESS, self._grab)
        self.bind(DGG.B1RELEASE, self._release)

        # Apply the theme to self
        self.add_theming_options(kw, parent, DraggableItem)

    def getCenterPosition(self) -> tuple[float, float]:
        """Method to get the center position of the self."""
        frameSize = None
        if self["frameSize"]:
            frameSize = self["frameSize"]
        else:
            frameSize = self.bounds

        if frameSize is None:
            frameSize = (0,) * 4

        height = frameSize[3] - frameSize[2]
        center_z = (height / 2 + frameSize[2]) * self.getScale().z
        width = frameSize[1] - frameSize[0]
        center_x = (width / 2 + frameSize[0]) * self.getScale().x

        return center_x, center_z

    def _grab(self, _):
        if self._is_dragged:
            return

        self._is_dragged = True
        self._old_parent = base.gui_controller._get_gui(self.parent)
        assert self._old_parent is not None, f"{self} has an invalid parent node. It should be parented to a 'DraggableTile'"

        self.wrt_reparent_to(base.aspect2d)
        self._task = self.addTask(self._drag_task, "drag")

    def _release(self, _):
        if not self._is_dragged:
            return

        self._is_dragged = False
        new_parent = DraggableTile._target

        if new_parent is not None and new_parent["group"] != self["group"]:
            new_parent = None

        self.removeTask(self._task)
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

        center_x, center_y = self.getCenterPosition()
        self.setPos(base.render2d, x - center_x, 0, y - center_y)
        return task.cont
