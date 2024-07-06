from BetterDirectGui.GuiTools import ThemeUtil


class GuiFactory:
    """Class to help storing standard settings for some gui widget.
    It can be seen as a way to set custom default values for options.
    """

    def __init__(self, gui_type, theme=None, **kwargs):
        self.gui_type = gui_type
        self.theme = theme
        self.kwargs = kwargs

    def __call__(self, parent=None, theme=None, **kwargs):
        kw = self.kwargs.copy()
        kw.update(kwargs)
        gui_item = self.gui_type(parent, **kw)
        priority = gui_item._theme_priority
        theme_ = ThemeUtil.merge(self.theme, theme)
        gui_item.set_theme(theme_, priority + 1)

        return gui_item
