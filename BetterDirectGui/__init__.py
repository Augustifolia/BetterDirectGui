"""Package containing a version of DirectGui with some improvements."""
__version__ = "0.1"
__author__ = "Augustifolia"


from BetterDirectGui import DirectGui
from .GuiController import GuiController
from .DirectGuiBase import DirectGuiWidget

__all__ = ["init", "DirectGui", "DirectGuiBase", "GuiController"]


def init(base_np=None, respect_sortOrder=True, do_bug_fixes=False, theme=None,
         do_keyboard_navigation=True, no_initopts=False):
    """Initialize GuiController and setup keyboard navigation.

    :param base_np: The NodePath that keyboard navigation should start from.
    :param respect_sortOrder: If True: navigation will take into account the sort order of the gui elements
     when selecting the next element to jump to.
    :param do_bug_fixes: Changes some buggy behaviour in DirectGui.
    :param theme: The global theme used by all elements that are children of base_np.
    :param do_keyboard_navigation: Chose weather keyboard navigation is enabled.
    :param no_initopts: Bool for making all initopts editable after gui creation.
    """
    GuiController(base_np, respect_sortOrder, do_bug_fixes, theme, do_keyboard_navigation, no_initopts)
