from BetterDirectGui.NewWidgets.DraggableTile import DraggableItem, DraggableTile


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
