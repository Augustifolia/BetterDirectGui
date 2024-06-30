from BetterDirectGui.NewWidgets.DraggableTile import DraggableItem, DraggableTile
# from BetterDirectGui import theme


d1 = DraggableTile(pos=(-.5, 0, 0))
d2 = DraggableTile(pos=(-.25, 0, 0))
d3 = DraggableTile(pos=(0, 0, 0))
d4 = DraggableTile(pos=(.25, 0, 0))
d5 = DraggableTile(pos=(.5, 0, 0))

i1 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="1", scale=0.2)
d1["content"] = i1
i2 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="2", scale=0.2)
d3["content"] = i2

d1 = DraggableTile(pos=(-.5, 0, -.3), group=1)
d2 = DraggableTile(pos=(-.25, 0, -.3), group=1)
d3 = DraggableTile(pos=(0, 0, -.3), group=1)
d4 = DraggableTile(pos=(.25, 0, -.3), group=1)
d5 = DraggableTile(pos=(.5, 0, -.3), group=1)

i1 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="1", scale=0.2, group=1)
d1["content"] = i1
i2 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="2", scale=0.2, group=1)
d3["content"] = i2

# testing stackable items
# i1 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="1", scale=0.2, stackSize=10, itemCount=6)
# d1["content"] = i1
# i2 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="2", scale=0.2, stackSize=10, itemCount=8, itemType=1)
# d3["content"] = i2

# d1 = DraggableTile(pos=(-.5, 0, -.3), group=0)
# d2 = DraggableTile(pos=(-.25, 0, -.3), group=0)
# d3 = DraggableTile(pos=(0, 0, -.3), group=0)
# d4 = DraggableTile(pos=(.25, 0, -.3), group=0)
# d5 = DraggableTile(pos=(.5, 0, -.3), group=0)

# i1 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="1", scale=0.2, group=0, stackSize=10, itemCount=7)
# d1["content"] = i1
# i2 = DraggableItem(frameColor=(0.1, 1, .1, 1), text="2", scale=0.2, group=0, stackSize=10, itemType=1)
# d3["content"] = i2

# base.gui_controller.set_theme(theme.default_theme)
