from direct.showbase.ShowBase import ShowBase
import gui_controller


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


if __name__ == '__main__':
    base = ShowBase()
    gui_controller.GuiController(respect_sortOrder=False, do_bug_fixes=True)

    run_test = 0

    if run_test == 0:
        test_most_types()
    elif run_test == 1:
        test_nesting()
    elif run_test == 2:
        test_radio_button()
    elif run_test == 3:
        test_scrolled_list()

    base.run()
