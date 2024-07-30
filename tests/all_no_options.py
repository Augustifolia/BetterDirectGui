from BetterDirectGui.DirectGui import *
from BetterDirectGui.NewWidgets import *
from BetterDirectGui.GuiTools import Themes


def cycle_through_gui(guis, value):
    guis[value[0]].hide()
    value[0] += 1
    try:
        guis[value[0]].show()
    except IndexError:
        value[0] = 0
        guis[value[0]].show()

    gui = guis[value[0]]
    t = str(gui)
    t = t.split("/")[-1]


guis = [
    # DirectGui widgets
    DirectButton(text="Button"),
    DirectCheckBox(),
    DirectCheckButton(text="Check"),
    OkCancelDialog(text="Dialog"),
    DirectEntry(enteredText="init text"),
    DirectEntryScroll(DirectEntry(), clipSize=(-.2, .2, -1, 1)),
    DirectFrame(frameSize=(-.5, .5, -.5, .5)),
    DirectLabel(text="Label"),
    DirectOptionMenu(items=["item1", "item2", "item3"], popupMarker_numStates=2),
    DirectRadioButton(text="Radio"),
    DirectScrollBar(),
    DirectScrolledFrame(),
    DirectScrolledList(items=[f"item{i}" for i in range(16)]),
    DirectSlider(),
    DirectWaitBar(value=40),

    # NewWidgets widgets,
    DraggableTile(),
    DraggableItem(frameTexture="models/maps/circle.png"),
]

for gui in guis:
    gui.hide()

base.accept("space", cycle_through_gui, extraArgs=[guis, [-2]])
base.messenger.send("space")
# base.gui_controller.set_theme(Themes.dark_theme)
