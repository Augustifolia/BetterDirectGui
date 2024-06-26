"""Showcase and entrypoint for tests."""
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui
from direct.gui import DirectGuiGlobals as DGG

loadPrcFileData(
    "",
    """
    want-pstats  #f
    win-size 1280 720
    """)


def test_most_types():
    import tests.most_gui_types as tg
    gui = tg.GUI(base.aspect2d)


def test_nesting():
    import tests.nesting_test as ns
    ns.test_setup1()


def test_radio_button():
    import tests.radio_button


def test_scrolled_list():
    import tests.scrolled_list


def test_inverted_scrollbar():
    from tests.inverted_scrollbars import GUI
    GUI()

def test_scroll():
    from tests.scroll_test import GUI
    GUI()


if __name__ == '__main__':
    base = ShowBase()  # init ShowBase
    base.setFrameRateMeter(True)
    base.accept("escape", base.userExit)
    BetterDirectGui.init(do_keyboard_navigation=False)  # init BetterDirectGui after ShowBase

    # create some gui
    run_test = 0

    # which theme to apply
    do_theme = 1

    # This isn't made to look good, but it illustrates how one easily can create a theme
    theme = {
        "general": dict(
            text_shadow=(.6, .6, .6, 1),
            text_shadowOffset=(0.05, 0.05),
            relief=DGG.TEXTUREBORDER,
            frameTexture="BetterDirectGui/assets/border.png",
            borderUvWidth=(.15, .15),
            transparency=True,
            frameColor=(.4, .7, .4, 1),
        ),
        "DirectButton": dict(
            frameColor=(0.1, 1, 1, 1),
            text_shadow=(.4, .4, .7, 1),
        ),
        "DirectEntry": dict(
            # enteredText="initial text",
            # numLines=3,
            # overflow=1,
        ),
        "DirectCheckButton": dict(
            indicatorValue=1,
            boxRelief=DGG.TEXTUREBORDER,
            # indicator_borderWidth=(.2, .2),
            boxBorder=.1,
            indicator_borderUvWidth=(.1, .1),
        ),
        "OkDialog": dict(
            # buttonTextList=["Ok", "No"],
            # buttonValueList=[DGG.DIALOG_OK, DGG.DIALOG_NO]
            borderWidth=(.1, .1),
            button_borderWidth=(.1, .1),
            button_relief=DGG.TEXTUREBORDER
        ),
        "DirectScrollBar": dict(
            # borderWidth=(0.01, 0.01),
            # thumb_frameColor=(1, 1, .1, 1)
        ),
        "DirectScrolledFrame": dict(
            scrollBarWidth=0.03,
            borderWidth=(.03, .03),
            borderUvWidth=(.08, .08),
            verticalScroll_thumb_frameColor=[1, .1, 1, 1]
        ),
        "DirectOptionMenu": dict(
            cancelframe_frameColor=(0, 0, 0, 0)
        ),
        "DirectScrolledList": dict(
            itemFrame_frameColor=(1, 1, 1, 1),
            # items_relief=DGG.TEXTUREBORDER
        ),
        "DirectWaitBar": dict(
            borderWidth=(.1, .1),
        ),
        "DirectRadioButton": dict(
            boxRelief=DGG.TEXTUREBORDER,
            boxBorder=.1,
            # boxPlacement="right",
            indicator_borderUvWidth=(.1, .1),
        ),
        "DraggableTile": dict(
            borderWidth=(.05, .05),
        ),
    }

    if do_theme == 0:
        base.gui_controller.set_theme(theme)
        # base.gui_controller.clear_theme()
        # base.gui_controller.set_theme(theme)

    if run_test == 0:
        test_most_types()
    elif run_test == 1:
        test_nesting()
    elif run_test == 2:
        test_radio_button()
    elif run_test == 3:
        test_scrolled_list()
    elif run_test == 4:
        test_inverted_scrollbar()
    elif run_test == 5:
        pass  # test empty scene
    elif run_test == 6:
        test_scroll()
    elif run_test == 7:
        import tests.draggable_tile_test

    if do_theme == 1:
        base.gui_controller.set_theme(theme)
        # base.gui_controller.clear_theme()
        # base.gui_controller.set_theme(theme)

    # start application
    base.run()
