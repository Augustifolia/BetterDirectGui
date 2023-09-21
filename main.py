from direct.showbase.ShowBase import ShowBase
import DirectGuiOverrides as dgo
import gui_controller


def test():
    print("click")


def test_setup1():
    b1 = dgo.DirectButton(text="button1", command=test)
    b1.setScale(0.2)
    b1.setPos(-0.7, 0, 0)

    f0 = dgo.DirectFrame(frameSize=(-1, 1, -1, 1))
    f0.setScale(0.2)
    f0.setPos(0, 0, 0)
    b11 = dgo.DirectButton(text="button1", parent=f0)
    b11.setScale(0.2)
    b11.setPos(0, 0, 0.7)
    f11 = dgo.DirectFrame(frameSize=(-1, 1, -1, 1), parent=f0)
    f11.setScale(0.6)
    f11.setPos(0, 0, 0)
    b14 = dgo.DirectButton(text="button4", parent=f11)
    b14.setScale(0.8)
    b14.setPos(0, 0, 0.3)
    b15 = dgo.DirectButton(text="button5", parent=f11)
    b15.setScale(0.8)
    b15.setPos(0, 0, -0.7)

    f1 = dgo.DirectFrame(frameSize=(-1, 1, -1, 1))
    f1.setScale(0.2)
    f1.setPos(0.7, 0, 0)
    b4 = dgo.DirectButton(text="button4", parent=f1)
    b4.setScale(0.2)
    b4.setPos(0, 0, 0)
    b5 = dgo.DirectButton(text="button5", parent=f1)
    b5.setScale(0.2)
    b5.setPos(0, 0, -0.3)

    b2 = dgo.DirectButton(text="button2")
    b2.setScale(0.2)
    b2.setPos(-0.7, 0, -0.5)
    b3 = dgo.DirectButton(text="button3")
    b3.setScale(0.2)
    b3.setPos(0.7, 0, -0.5)


def test_setup2():
    import test_gui
    test_gui.GUI(base.aspect2d)


if __name__ == '__main__':
    base = ShowBase()
    gui_controller.GuiController(respect_sortOrder=False)

    test_setup2()
    import direct.gui.DirectGuiBase as dgb
    print(dgb.DirectGuiWidget.guiDict)

    base.run()
