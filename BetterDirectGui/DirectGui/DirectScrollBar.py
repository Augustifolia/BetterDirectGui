"""Defines the DirectScrollBar class.

See the :ref:`directscrollbar` page in the programming manual for a more
in-depth explanation and an example of how to use this class.
"""

__all__ = ['DirectScrollBar']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from .DirectFrame import *
from .DirectButton import *

"""
import DirectScrollBar
d = DirectScrollBar(borderWidth=(0, 0))

"""

class DirectScrollBar(DirectFrame):
    """
    DirectScrollBar -- a widget which represents a scroll bar the user can
    use for paging through a large document or panel.
    """
    def __init__(self, parent = None, **kw):
        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',         PGSliderBar,        None),
            ('state',          DGG.NORMAL,         None),
            ('frameColor',     (0.6, 0.6, 0.6, 1), None),

            ('range',          (0, 1),             self.setRange),
            ('value',          0,                  self.__setValue),
            ('scrollSize',     0.01,               self.setScrollSize),
            ('pageSize',       0.1,                self.setPageSize),
            ('orientation',    DGG.HORIZONTAL,     self.setOrientation),
            ('manageButtons',  1,                  self.setManageButtons),
            ('resizeThumb',    1,                  self.setResizeThumb),

            # Function to be called repeatedly as the bar is scrolled
            ('command',        None,               None),
            ('extraArgs',      [],                 None),
            ('selectable',     True,               None),
            )

        if kw.get('orientation') in (DGG.VERTICAL, DGG.VERTICAL_INVERTED):
            # These are the default options for a vertical layout.
            optiondefs += (
                ('frameSize',      (-0.04, 0.04, -0.5, 0.5),   None),
                )
        else:
            # These are the default options for a horizontal layout.
            optiondefs += (
                ('frameSize',      (-0.5, 0.5, -0.04, 0.04),  None),
                )

        # Merge keyword options with theme from gui_controller
        kw = self.add_theming_options(kw, parent)

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectFrame.__init__(self, parent)

        self.thumb = self.createcomponent(
            "thumb", (), None,
            DirectButton, (self,),
            borderWidth = self['borderWidth'])
        self.incButton = self.createcomponent(
            "incButton", (), None,
            DirectButton, (self,),
            borderWidth = self['borderWidth'])
        self.decButton = self.createcomponent(
            "decButton", (), None,
            DirectButton, (self,),
            borderWidth = self['borderWidth'])

        if self.decButton['frameSize'] == None and \
           self.decButton.bounds == [0.0, 0.0, 0.0, 0.0]:
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.decButton['frameSize'] = (f[0]*0.05, f[1]*0.05, f[2], f[3])
            else:
                self.decButton['frameSize'] = (f[0], f[1], f[2]*0.05, f[3]*0.05)

        if self.incButton['frameSize'] == None and \
           self.incButton.bounds == [0.0, 0.0, 0.0, 0.0]:
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.incButton['frameSize'] = (f[0]*0.05, f[1]*0.05, f[2], f[3])
            else:
                self.incButton['frameSize'] = (f[0], f[1], f[2]*0.05, f[3]*0.05)

        self.guiItem.setThumbButton(self.thumb.guiItem)
        self.guiItem.setLeftButton(self.decButton.guiItem)
        self.guiItem.setRightButton(self.incButton.guiItem)

        # setup keyboard navigation for buttons
        self.decButton.activate = self._activate_dec_button
        self.incButton.activate = self._activate_inc_button
        self.thumb.activate = self.activate
        self.thumb.deactivate = self.deactivate
        self.thumb.show_click = self.thumb_show_click
        self.thumb.show_unclick = self.thumb_show_unclick

        # Bind command function
        self.bind(DGG.ADJUST, self.commandFunc)

        # Call option initialization functions
        self.initialiseoptions(DirectScrollBar)

    def activate(self):
        self.setup_keyboard_navigation()

    def deactivate(self):
        self.ignore_keyboard_navigation()

    def thumb_show_click(self):
        self._scale = VBase4(self.thumb.guiItem.get_frame())
        self.thumb["frameSize"] = self._scale * 0.9

    def thumb_show_unclick(self):
        def set_scale(scale):
            self.thumb["frameSize"] = scale
        if hasattr(self, "_scale"):
            self.do_method_later(0.1, set_scale, "unclick", [self._scale])

    def setup_keyboard_navigation(self):
        # todo check orientation of the scroll bar to determine scroll direction
        for key, value in base.gui_controller.key_map.items():
            if isinstance(value, tuple):
                if key in ("d", "r"):
                    self.accept(value[0], self.scrollStep, extraArgs=[1])
                    self.accept(value[0] + "-repeat", self.scrollStep, extraArgs=[1])
                elif key in ("u", "l"):
                    self.accept(value[0], self.scrollStep, extraArgs=[-1])
                    self.accept(value[0] + "-repeat", self.scrollStep, extraArgs=[-1])

    def ignore_keyboard_navigation(self):
        for key, value in base.gui_controller.key_map.items():
            if isinstance(value, tuple):
                if key in ("u", "d", "l", "r"):
                    self.ignore(value[0])
                    self.ignore(value[0] + "-repeat")

    def _activate_inc_button(self):
        self.scrollStep(1)
        self.incButton["selected"] = False

    def _activate_dec_button(self):
        self.scrollStep(-1)
        self.decButton["selected"] = False

    def setRange(self):
        # Try to preserve the value across a setRange call.
        v = self['value']
        r = self['range']
        self.guiItem.setRange(r[0], r[1])
        self['value'] = v

    def __setValue(self):
        # This is the internal function that is called when
        # self['value'] is directly assigned.
        self.guiItem.setValue(self['value'])

    def setValue(self, value):
        # This is the public function that is meant to be called by a
        # user that doesn't like to use (or doesn't understand) the
        # preferred interface of self['value'].
        self['value'] = value

    def getValue(self):
        return self.guiItem.getValue()

    def getRatio(self):
        return self.guiItem.getRatio()

    def setScrollSize(self):
        self.guiItem.setScrollSize(self['scrollSize'])

    def setPageSize(self):
        self.guiItem.setPageSize(self['pageSize'])

    def scrollStep(self, stepCount):
        """Scrolls the indicated number of steps forward.  If
        stepCount is negative, scrolls backward."""
        self['value'] = self.guiItem.getValue() + self.guiItem.getScrollSize() * stepCount

    def scrollPage(self, pageCount):
        """Scrolls the indicated number of pages forward.  If
        pageCount is negative, scrolls backward."""
        self['value'] = self.guiItem.getValue() + self.guiItem.getPageSize() * pageCount

    def setOrientation(self):
        if self['orientation'] == DGG.HORIZONTAL:
            self.guiItem.setAxis(Vec3(1, 0, 0))
        elif self['orientation'] == DGG.VERTICAL:
            self.guiItem.setAxis(Vec3(0, 0, -1))
        elif self['orientation'] == DGG.VERTICAL_INVERTED:
            self.guiItem.setAxis(Vec3(0, 0, 1))
        else:
            raise ValueError('Invalid value for orientation: %s' % (self['orientation']))

    def setManageButtons(self):
        self.guiItem.setManagePieces(self['manageButtons'])

    def setResizeThumb(self):
        self.guiItem.setResizeThumb(self['resizeThumb'])

    def destroy(self):
        self.thumb.destroy()
        del self.thumb
        self.incButton.destroy()
        del self.incButton
        self.decButton.destroy()
        del self.decButton
        DirectFrame.destroy(self)

    def commandFunc(self):
        # Store the updated value in self['value']
        self._optionInfo['value'][DGG._OPT_VALUE] = self.guiItem.getValue()

        if self['command']:
            self['command'](*self['extraArgs'])

