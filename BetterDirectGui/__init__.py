"""Package containing a version of DirectGui with some improvements."""
__version__ = "0.1"
__author__ = "Augustifolia"


from BetterDirectGui import DirectGui
from .GuiController import GuiController
from .DirectGuiBase import DirectGuiWidget

__all__ = ["init", "DirectGui", "DirectGuiBase", "GuiController"]


def init(base_np=None, respect_sortOrder=True, do_bug_fixes=False):
    """Initialize GuiController and setup keyboard navigation.

    :param base_np: The NodePath that keyboard navigation should start from.
    :param respect_sortOrder: If True: navigation will take into account the sort order of the gui elements
     when selecting the next element to jump to.
    :param do_bug_fixes: Changes some buggy behaviour in DirectGui.
    """
    GuiController(base_np, respect_sortOrder, do_bug_fixes)
