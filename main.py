"""Showcase and entrypoint for tests."""
from direct.showbase.ShowBase import ShowBase
import BetterDirectGui


def test_most_types():
    import tests.most_gui_types as tg
    gui = tg.GUI(base.aspect2d)
    # gui.destroy()


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
    BetterDirectGui.init(respect_sortOrder=False, do_bug_fixes=True, do_keyboard_navigation=True, no_initopts=True)  # init BetterDirectGui after ShowBase
    # base.gui_controller.update_key_map()

    # create some gui
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
        test_inverted_scrollbar()
    elif run_test == 5:
        pass  # test empty scene

    # start application
    base.run()
