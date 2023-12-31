from BetterDirectGui.DirectGui import *


def test():
    print("click")


def test_setup1():
    b1 = DirectButton(text="button1", command=test)  # , suppressMouse=0, frameTexture="models/maps/circle.png")
    b1.setScale(0.2)
    b1.setPos(-0.7, 0, 0)
    # b1["scale"] = 0.2
    # b1["pos"] = (-0.7, 0, 0)
    # b1["hpr"] = (30, 30, 30)
    # b1["suppressMouse"] = 1
    # b1["suppressKeys"] = 1
    # b1["transparency"] = 1

    f0 = DirectFrame(frameSize=(-1, 1, -1, 1))
    f0.setScale(0.2)
    f0.setPos(0, 0, 0)
    b11 = DirectButton(text="button1", parent=f0)
    b11.setScale(0.2)
    b11.setPos(0, 0, 0.7)
    f11 = DirectFrame(frameSize=(-1, 1, -1, 1), parent=f0)
    f11.setScale(0.6)
    f11.setPos(0, 0, 0)
    b14 = DirectButton(text="button4", parent=f11)
    b14.setScale(0.8)
    b14.setPos(0, 0, 0.3)
    b15 = DirectButton(text="button5", parent=f11)
    b15.setScale(0.8)
    b15.setPos(0, 0, -0.7)

    f1 = DirectFrame(frameSize=(-1, 1, -1, 1))
    f1.setScale(0.2)
    f1.setPos(0.7, 0, 0)
    b4 = DirectButton(text="button4", parent=f1)
    b4.setScale(0.2)
    b4.setPos(0, 0, 0)
    b5 = DirectButton(text="button5", parent=f1)
    b5.setScale(0.2)
    b5.setPos(0, 0, -0.3)

    b2 = DirectButton(text="button2")
    b2.setScale(0.2)
    b2.setPos(-0.7, 0, -0.5)
    b3 = DirectButton(text="button3")
    b3.setScale(0.2)
    b3.setPos(0.7, 0, -0.5)

    theme = {
        "DirectButton": dict(
            borderWidth=(0.2, 0.2),
            frameColor=(.2, 1.0, 1.0, 1.0),
            pad=(0.2, 0.2),
            pos=(0, 0, 0),
            hpr=(0, 0, -30),
            scale=(0.1, 0.1, 0.1),
            text='button',
        ),
        "DirectFrame": dict(
            # frameSize=(-1, 1, -1, 1),
            frameColor=(.2, 1, 1, 1),
            text=""
        )
    }

    # b1.override_navigation_map("f", b2)
    # f1.set_theme(theme, 1)
    # f1.clear_theme()
