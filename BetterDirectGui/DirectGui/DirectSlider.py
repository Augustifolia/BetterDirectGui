"""Defines the DirectSlider class.

See the :ref:`directslider` page in the programming manual for a more
in-depth explanation and an example of how to use this class.
"""

__all__ = ['DirectSlider']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from .DirectFrame import *
from .DirectButton import *
from math import isnan

"""
import DirectSlider
d = DirectSlider(borderWidth=(0, 0))

"""


class DirectSlider(DirectFrame):
    """
    DirectSlider -- a widget which represents a slider that the
    user can pull left and right to represent a continuous value.
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

            # Function to be called repeatedly as slider is moved
            ('command',        None,               None),
            ('extraArgs',      [],                 None),
            ('selectable',     True,               None),
            )

        if kw.get('orientation') == DGG.VERTICAL:
            # These are the default options for a vertical layout.
            optiondefs += (
                ('frameSize',      (-0.08, 0.08, -1, 1),   None),
                ('frameVisibleScale', (0.25, 1),         None),
                )
        else:
            # These are the default options for a horizontal layout.
            optiondefs += (
                ('frameSize',      (-1, 1, -0.08, 0.08),  None),
                ('frameVisibleScale', (1, 0.25),        None),
                )

        # Do some theme handling. This should be called before "defineoptions"
        self.add_theming_options(kw, parent)

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectFrame.__init__(self, parent)

        self.thumb = self.createcomponent("thumb", (), None,
                                          DirectButton, (self,),
                                          borderWidth = self['borderWidth'])
        if self.thumb['frameSize'] == None and \
           self.thumb.bounds == [0.0, 0.0, 0.0, 0.0]:
            # Compute a default frameSize for the thumb.
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.thumb['frameSize'] = (f[0]*0.05, f[1]*0.05, f[2], f[3])
            else:
                self.thumb['frameSize'] = (f[0], f[1], f[2]*0.05, f[3]*0.05)

        self.guiItem.setThumbButton(self.thumb.guiItem)

        # setup keyboard navigation for the thumb
        self.thumb.activate = self.activate
        self.thumb.deactivate = self.deactivate
        self.thumb.show_click = self.thumb_show_click
        self.thumb.show_unclick = self.thumb_show_unclick

        # Bind command function
        self.bind(DGG.ADJUST, self.commandFunc)

        # Call option initialization functions
        self.initialiseoptions(DirectSlider)
        # actually apply the theme
        self.init_theme()

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
        forward = 1
        backward = -1
        if self["orientation"] == DGG.VERTICAL:
            forward, backward = backward, forward

        for key, value in base.gui_controller.key_map.items():
            if isinstance(value, tuple):
                if key in ("d", "r"):
                    self.accept(value[0], self.scrollStep, extraArgs=[forward])
                    self.accept(value[0] + "-repeat", self.scrollStep, extraArgs=[forward])
                elif key in ("u", "l"):
                    self.accept(value[0], self.scrollStep, extraArgs=[backward])
                    self.accept(value[0] + "-repeat", self.scrollStep, extraArgs=[backward])

    def ignore_keyboard_navigation(self):
        for key, value in base.gui_controller.key_map.items():
            if isinstance(value, tuple):
                if key in ("u", "d", "l", "r"):
                    self.ignore(value[0])
                    self.ignore(value[0] + "-repeat")

    def scrollStep(self, stepCount):
        """Scrolls the indicated number of steps forward.  If
        stepCount is negative, scrolls backward."""
        self['value'] = self.guiItem.getValue() + self.guiItem.getScrollSize() * stepCount

    def setRange(self):
        # Try to preserve the value across a setRange call.
        v = self['value']
        r = self['range']
        self.guiItem.setRange(r[0], r[1])
        self['value'] = v

    def __setValue(self):
        # This is the internal function that is called when
        # self['value'] is directly assigned.
        value = self['value']
        assert not isnan(value)
        self.guiItem.setValue(value)

    def setValue(self, value):
        # This is the public function that is meant to be called by a
        # user that doesn't like to use (or doesn't understand) the
        # preferred interface of self['value'].
        assert not isnan(value)
        self['value'] = value

    def getValue(self):
        return self.guiItem.getValue()

    def getRatio(self):
        return self.guiItem.getRatio()

    def setScrollSize(self):
        self.guiItem.setScrollSize(self['scrollSize'])

    def setPageSize(self):
        self.guiItem.setPageSize(self['pageSize'])

    def setOrientation(self):
        if self['orientation'] == DGG.HORIZONTAL:
            self.guiItem.setAxis(Vec3(1, 0, 0))
        elif self['orientation'] == DGG.VERTICAL:
            self.guiItem.setAxis(Vec3(0, 0, 1))
        else:
            raise ValueError('Invalid value for orientation: %s' % (self['orientation']))

    def destroy(self):
        if (hasattr(self, 'thumb')):
            self.thumb.destroy() # ow!
            del self.thumb
        DirectFrame.destroy(self)

    def commandFunc(self):
        # Store the updated value in self['value']
        self._optionInfo['value'][DGG._OPT_VALUE] = self.guiItem.getValue()

        if self['command']:
            self['command'](*self['extraArgs'])
