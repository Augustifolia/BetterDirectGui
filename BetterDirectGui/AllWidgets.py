"""Module to easily import all widgets."""

# Direct gui default stuff
from .DirectGui.OnscreenText import OnscreenText
from .DirectGui.OnscreenGeom import OnscreenGeom
from .DirectGui.OnscreenImage import OnscreenImage

# Direct Gui Classes
from .DirectGui.DirectFrame import DirectFrame
from .DirectGui.DirectButton import DirectButton
from .DirectGui.DirectEntry import DirectEntry
from .DirectGui.DirectEntryScroll import DirectEntryScroll
from .DirectGui.DirectLabel import DirectLabel
from .DirectGui.DirectScrolledList import DirectScrolledList, DirectScrolledListItem
from .DirectGui.DirectDialog import (
    DirectDialog,
    OkDialog,
    OkCancelDialog,
    YesNoDialog,
    YesNoCancelDialog,
    RetryCancelDialog,
)
from .DirectGui.DirectWaitBar import DirectWaitBar
from .DirectGui.DirectSlider import DirectSlider
from .DirectGui.DirectScrollBar import DirectScrollBar
from .DirectGui.DirectScrolledFrame import DirectScrolledFrame
from .DirectGui.DirectCheckButton import DirectCheckButton
from .DirectGui.DirectOptionMenu import DirectOptionMenu
from .DirectGui.DirectRadioButton import DirectRadioButton
from .DirectGui.DirectCheckBox import DirectCheckBox

# new widgets
from .NewWidgets.DraggableTile import DraggableTile, DraggableItem

# DirectGuiExtension widgets
try:
    import DirectGuiExtension
    del DirectGuiExtension
except ImportError:  # DirectGuiExtension is not installed
    pass
else:  # DirectGuiExtension is installed, we can import the widgets from it
    from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
    from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
    from DirectGuiExtension.DirectCollapsibleFrame import DirectCollapsibleFrame
    from DirectGuiExtension.DirectDatePicker import DirectDatePicker
    from DirectGuiExtension.DirectDiagram import DirectDiagram
    from DirectGuiExtension.DirectGridSizer import DirectGridSizer
    from DirectGuiExtension.DirectMenuBar import DirectMenuBar
    from DirectGuiExtension.DirectMenuItem import (
        DirectMenuItem,
        DirectMenuItemEntry,
        DirectMenuItemSubMenu,
        DirectMenuSeparator
    )
    # from DirectGuiExtension.DirectOptionMenu import DirectOptionMenu  # we already have one version of the option menu
    from DirectGuiExtension.DirectScrolledWindowFrame import DirectScrolledWindowFrame
    from DirectGuiExtension.DirectSpinBox import DirectSpinBox
    from DirectGuiExtension.DirectSplitFrame import DirectSplitFrame
    from DirectGuiExtension.DirectTabbedFrame import DirectTabbedFrame
    from DirectGuiExtension.DirectTooltip import DirectTooltip
    from DirectGuiExtension.DirectTreeView import DirectTreeView
