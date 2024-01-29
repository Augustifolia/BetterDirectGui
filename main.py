"""Showcase and entrypoint for tests."""
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui
from direct.gui import DirectGuiGlobals as DGG


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


if __name__ == '__main__':
    base = ShowBase()  # init ShowBase
    base.accept("escape", base.userExit)
    BetterDirectGui.init()  # init BetterDirectGui after ShowBase

    # create some gui
    run_test = 0

    # which theme to apply
    do_theme = 1

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

    if do_theme == 1:
        # This looks terrible, but it illustrates how one easily can create a theme
        theme = {
            "general": dict(
                text_shadow=(.6, .6, .6, 1),
                text_shadowOffset=(0.05, 0.05),
                relief=DGG.FLAT,
                frameTexture="models/maps/circle.png",
                # frameTexture="BetterDirectGui/BDGAssets/corner.png",
                transparency=True,
                frameColor=(.1, .67, .3, 1),
                # compositeFrameTexture=dict(
                #     edge="BetterDirectGui/BDGAssets/edge.png",
                #     corner="BetterDirectGui/BDGAssets/corner.png",
                #     center="BetterDirectGui/BDGAssets/center.png",
                # )
            ),
            "DirectButton": dict(
                frameColor=(0.1, 1, 1, 1),
                text_shadow=(.4, .4, .7, 1),
            ),
            "DirectEntry": dict(
                enteredText="initial text"
            ),
            "DirectCheckButton": dict(
                indicatorValue=1,
            ),
            "OkDialog": dict(
                # buttonTextList=["Ok", "No"],
                # buttonValueList=[DGG.DIALOG_OK, DGG.DIALOG_NO]
            ),
            "DirectScrollBar": dict(
                # relief=DGG.SUNKEN,
                # borderWidth=(0.01, 0.01),
                thumb_frameColor=(1, 1, .1, 1)
            ),
            "DirectScrolledFrame": dict(
                scrollBarWidth=0.03
            ),
            "DirectOptionMenu": dict(
                cancelframe_frameColor=(0, 0, 0, 0)
            ),
            "DirectScrolledList": dict(
                itemFrame_frameColor=(1, 1, 1, 1)
            )
        }
        base.gui_controller.set_theme(theme)
        # base.gui_controller.clear_theme()
        # base.gui_controller.set_theme(theme)

    # start application
    base.run()
