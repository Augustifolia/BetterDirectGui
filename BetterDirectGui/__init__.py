"""Package containing a version of DirectGui with some improvements."""
__version__ = "0.1"
__author__ = "Augustifolia"


from BetterDirectGui import DirectGui
from .GuiController import GuiController
from .DirectGuiBase import DirectGuiWidget

__all__ = ["init", "DirectGui", "DirectGuiBase", "GuiController"]

init = GuiController
