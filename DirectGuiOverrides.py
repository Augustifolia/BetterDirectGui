import direct.gui.DirectGui as DirectGui
import direct.gui.DirectCheckBox as ogDirectCheckBox
from DirectGuiBase import DirectGuiWidget


class DirectFrame(DirectGui.DirectFrame, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        # Inherits from DirectGuiWidget
        optiondefs = (
            ('selectable',     False,       None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectGui.DirectFrame.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectFrame)


class DirectButton(DirectGui.DirectButton, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectButton.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectButton)

    def activate(self):
        print("activate")
        self.commandFunc("")
        self["selected"] = False

    def deactivate(self):
        print("deactivate")


class DirectEntry(DirectGui.DirectEntry, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectEntry.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectEntry)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectEntryScroll(DirectGui.DirectEntryScroll, DirectGuiWidget):
    def __init__(self, entry, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectEntryScroll.__init__(self, entry, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectEntry)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectLabel(DirectGui.DirectLabel, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     False,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectLabel.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectLabel)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectScrolledList(DirectGui.DirectScrolledList, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     False,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectScrolledList.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectScrolledList)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectDialog(DirectGui.DirectDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class OkDialog(DirectGui.OkDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.OkDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(OkDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class OkCancelDialog(DirectGui.OkCancelDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.OkCancelDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(OkCancelDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class YesNoDialog(DirectGui.YesNoDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.YesNoDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(YesNoDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class YesNoCancelDialog(DirectGui.YesNoCancelDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.YesNoCancelDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(YesNoCancelDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class RetryCancelDialog(DirectGui.RetryCancelDialog, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.RetryCancelDialog.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(RetryCancelDialog)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectWaitBar(DirectGui.DirectWaitBar, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     False,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectWaitBar.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectWaitBar)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectSlider(DirectGui.DirectSlider, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectSlider.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectSlider)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectScrollBar(DirectGui.DirectScrollBar, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectScrollBar.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectScrollBar)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectScrolledFrame(DirectGui.DirectScrolledFrame, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectScrolledFrame.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectScrolledFrame)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectCheckButton(DirectGui.DirectCheckButton, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectCheckButton.__init__(self, parent)
        print(self.components())
        DirectGuiWidget.__init__(self, parent)
        DirectGui.DirectCheckButton.__init__(self, parent)
        print(self.components())

        # Call option initialization functions
        self.initialiseoptions(DirectCheckButton)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectOptionMenu(DirectGui.DirectOptionMenu, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     False,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectOptionMenu.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectOptionMenu)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectRadioButton(DirectGui.DirectRadioButton, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGui.DirectRadioButton.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectRadioButton)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")


class DirectCheckBox(ogDirectCheckBox.DirectCheckBox, DirectGuiWidget):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('selectable',     True,        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        ogDirectCheckBox.DirectCheckBox.__init__(self, parent)
        DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectCheckBox)

    def activate(self):
        print("activate")

    def deactivate(self):
        print("deactivate")
