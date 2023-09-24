from BetterDirectGui.DirectGui import *


def test():
    print("click")


def test_setup1():
    b1 = DirectButton(text="button1", command=test)
    b1.setScale(0.2)
    b1.setPos(-0.7, 0, 0)

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
