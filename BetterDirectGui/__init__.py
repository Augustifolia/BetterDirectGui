__version__ = "0.1"
__author__ = "Augustifolia"


from BetterDirectGui import DirectGui
from .GuiController import GuiController
from .DirectGuiBase import DirectGuiWidget

__all__ = ["init", "DirectGui", "DirectGuiBase", "GuiController"]


def init(base_np=None, respect_sortOrder=True, do_bug_fixes=False):
    GuiController(base_np, respect_sortOrder, do_bug_fixes)
