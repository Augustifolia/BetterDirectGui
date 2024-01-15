from .DirectButton import DirectButton
from panda3d.core import *
import direct.gui.DirectGuiGlobals as DGG

__all__ = ["DirectCheckBox"]


class DirectCheckBox(DirectButton):
    """
    DirectCheckBox(parent) - Create a DirectGuiWidget which responds
    to mouse clicks by setting a state of True or False and executes
    a callback function if defined.

    Uses an image swap rather than a text change to indicate state.
    """
    def __init__(self, parent=None, **kw):

        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',         PGButton,   None),
            ('numStates',      4,          None),
            ('state',          DGG.NORMAL, None),
            ('relief',         DGG.RAISED, None),
            ('invertedFrames', (1,),       None),
            # Command to be called on button click
            ('command',        None,       None),
            ('extraArgs',      [],         None),
            # Which mouse buttons can be used to click the button
            ('commandButtons', (DGG.LMB,),     self.setCommandButtons),
            # Sounds to be used for button events
            ('rolloverSound', DGG.getDefaultRolloverSound(), self.setRolloverSound),
            ('clickSound',    DGG.getDefaultClickSound(),    self.setClickSound),
            # Can only be specified at time of widget contruction
            # Do the text/graphics appear to move when the button is clicked
            # ('pressEffect',     1,         DGG.INITOPT),
            # ('uncheckedImage',  None,      None),
            # ('checkedImage',    None,      None),
            # ('isChecked',       False,     None),
            ('selectable',      True,      None),
        )

        if base.gui_controller.no_initopts:
            optiondefs += (
                ('uncheckedImage', None, self._update_image),
                ('checkedImage', None, self._update_image),
                ('isChecked', False, self._update_image),
            )
        else:
            optiondefs += (
                ('uncheckedImage', None, None),
                ('checkedImage', None, None),
                ('isChecked', False, None),
            )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        DirectButton.__init__(self, parent)

        self.initialiseoptions(DirectCheckBox)

        if base.gui_controller._do_bug_fixes:
            self._update_image()
            if self["frameSize"] is None:
                self.resetFrameSize()

        # Apply the theme to self
        self.add_theming_options(kw, parent, DirectCheckBox)

    def _update_image(self):
        if self['isChecked']:
            self['image'] = self['checkedImage']
        else:
            self['image'] = self['uncheckedImage']

        self.setImage()

    def click(self):
        self.commandFunc("")
        self.show_click()

    def activate(self):
        self["selected"] = False

    def deactivate(self):
        pass

    def commandFunc(self, event):
        self['isChecked'] = not self['isChecked']

        self._update_image()

        if self['command']:
            # Pass any extra args to command
            self['command'](*[self['isChecked']] + self['extraArgs'])

