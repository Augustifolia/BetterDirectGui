"""Showcase and entrypoint for tests."""
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui
from BetterDirectGui.GuiTools import Themes

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
    BetterDirectGui.init()  # do_keyboard_navigation=False)  # init BetterDirectGui after ShowBase

    # create some gui
    run_test = 0

    # which theme to apply
    do_theme = 1

    # use default theme
    theme = Themes.default_theme

    if do_theme == 0:  # todo if a theme is applied before the gui is created, some options are not set correctly
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
