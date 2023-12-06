"""Showcase and entrypoint for tests."""
from panda3d.core import loadPrcFileData
loadPrcFileData("", "model-path $MAIN_DIR/tests")

from direct.showbase.ShowBase import ShowBase
import BetterDirectGui
import direct.gui.DirectGuiGlobals as DGG
import panda3d.core as p3d


def test_most_types():
    import tests.most_gui_types as tg
    tg.GUI(base.aspect2d)


def test_nesting():
    import tests.nesting_test as ns
    ns.test_setup1()


def test_radio_button():
    import tests.radio_button


def test_scrolled_list():
    import tests.scrolled_list


def test_new_frame_tex():
    button = BetterDirectGui.DirectGui.DirectButton(
        pos=(0, 0, 0.25),
        text='button',
        pressEffect=1,
        frameTexture="models/maps/circle.png",
        frameTextureCenter="center.png",
        frameTextureEdge="edge.png",
        frameTextureCorner="corner.png",
        relief=DGG.FLAT,
        scale=0.8,
        # frameSize=[-0.5, 0.5, -0.5, 0.5],
        pad=[0.1, 0.1],
        borderWidth=(0.1, 0.1)
    )
    button.setTransparency(1)
    print(button["frameSize"], button.getBounds())  # , button.getBounds(), button.bounds)
    button3 = BetterDirectGui.DirectGui.DirectButton(
        pos=(0, 0, -0.55),
        text='button',
        pressEffect=1,
        frameTexture="models/maps/circle.png",
        frameTextureCenter="center.png",
        frameTextureEdge="edge.png",
        frameTextureCorner="corner.png",
        relief=DGG.FLAT,
        scale=0.8,
        frameSize=[-0.2, 0.5, -0.8, 0.8],
        pad=[0.1, 0.1],
        text_scale=0.6
    )
    button3.setTransparency(1)
    button2 = BetterDirectGui.DirectGui.DirectButton(
        pos=(0, 0, -0.75),
        text='button',
        pressEffect=1,
        scale=0.8
    )
    button2.hide()

    def show_screen(task):
        screen_size = base.getSize()
        aspect_ratio = base.getAspectRatio()  # the scaling of gui elements in aspect2d is based on the smallest of screen height and width
        # print(screen_size, aspect_ratio)
        return task.cont

    button.add_task(show_screen, "show_screen")


def pixel2d_test():
    button = BetterDirectGui.DirectGui.DirectButton(
        borderWidth=(.5, .2),
        pos=p3d.LPoint3f(533.328, 0, -324),
        text='button',
        frameTexture="models/maps/circle.png",
        frameTextureCenter="center.png",
        frameTextureEdge="edge.png",
        frameTextureCorner="corner.png",
        text_scale=(48, 48),
        parent=base.pixel2d,
        relief=DGG.FLAT,
        pressEffect=1,
        pad=(100, 100)
    )
    button.setTransparency(1)


def test_inverted_scrollbar():
    from tests.inverted_scrollbars import GUI
    GUI()


if __name__ == '__main__':
    base = ShowBase()  # init ShowBase
    base.accept("escape", base.userExit)
    test_pixel2d = False
    if test_pixel2d:
        BetterDirectGui.init(respect_sortOrder=False, do_bug_fixes=True, do_keyboard_navigation=True, base_np=base.pixel2d)  # init BetterDirectGui after ShowBase
    else:
        BetterDirectGui.init(respect_sortOrder=False, do_bug_fixes=True, do_keyboard_navigation=True)  # init BetterDirectGui after ShowBase

    run_test = 0

    if run_test == 0:
        test_most_types()
    elif run_test == 1:
        test_nesting()
    elif run_test == 2:
        test_radio_button()
    elif run_test == 3:
        test_scrolled_list()
    elif run_test == 4:
        test_new_frame_tex()
    elif run_test == 5:
        test_inverted_scrollbar()
    elif run_test == 6:
        pass  # test empty scene
    # test pixel 2d
    elif run_test == 7:
        pixel2d_test()

    # start application
    base.run()
