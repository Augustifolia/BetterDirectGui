"""A DirectRadioButton is a type of button that, similar to a
DirectCheckButton, has a separate indicator and can be toggled between
two states.  However, only one DirectRadioButton in a group can be enabled
at a particular time.

See the :ref:`directradiobutton` page in the programming manual for a more
in-depth explanation and an example of how to use this class.
"""

__all__ = ['DirectRadioButton']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from .DirectButton import *
from .DirectLabel import *

class DirectRadioButton(DirectButton):
    """
    DirectRadioButton(parent) - Create a DirectGuiWidget which responds
    to mouse clicks by setting given value to given variable and
    execute a callback function (passing that state through) if defined
    """
    def __init__(self, parent = None, **kw):
        # Inherits from DirectButton
        # A Direct Frame can have:
        # - A background texture (pass in path to image, or Texture Card)
        # - A midground geometry item (pass in geometry)
        # - A foreground text Node (pass in text string or Onscreen Text)
        # For a direct button:
        # Each button has 4 states (ready, press, rollover, disabled)
        # The same image/geom/text can be used for all four states or each
        # state can have a different text/geom/image
        # State transitions happen automatically based upon mouse interaction
        # Responds to click event and calls command if None

        self.colors = None
        optiondefs = (
            ('indicatorValue', 0, self.setIndicatorValue),
            # variable is a list whose value will be set by this radio button
            ('variable', [], None),
            # value is the value to be set when this radio button is selected
            ('value', [], None),
            # others is a list of other radio buttons sharing same variable
            ('others', [], None),
            # boxBorder defines the space created around the check box
            # ('boxBorder', 0, None),
            # boxPlacement maps left, above, right, below
            # ('boxPlacement', 'left', None),
            # boxGeom defines geom to indicate current radio button is selected or not
            # ('boxGeom', None, None),
            # ('boxGeomColor', None, None),
            # ('boxGeomScale', 1.0, None),
            # ('boxImage', None, None),
            # ('boxImageScale', 1.0, None),
            # ('boxImageColor', VBase4(1, 1, 1, 1), None),
            # ('boxRelief', None, None),
            ('selectable', True, None),
        )

        if base.gui_controller.no_initopts:
            optiondefs += (
                ('boxBorder', 0, self.setFrameSize),
                # boxPlacement maps left, above, right, below
                ('boxPlacement', 'left', self.setFrameSize),
                ('boxGeom', None, self._update_box_geom_image),
                ('boxGeomColor', None, self._update_box_geom_image),
                ('boxGeomScale', 1.0, self._update_box_geom_image),
                ('boxImage', None, self._update_box_geom_image),
                ('boxImageScale', 1.0, self._update_box_geom_image),
                ('boxImageColor', VBase4(1, 1, 1, 1), self._update_box_geom_image),
                ('boxRelief', None, self._update_box_geom_image),
            )
        else:
            optiondefs += (
                ('boxBorder', 0, None),
                # boxPlacement maps left, above, right, below
                ('boxPlacement', 'left', None),
                ('boxGeom', None, None),
                ('boxGeomColor', None, None),
                ('boxGeomScale', 1.0, None),
                ('boxImage', None, None),
                ('boxImageScale', 1.0, None),
                ('boxImageColor', VBase4(1, 1, 1, 1), None),
                ('boxRelief', None, None),
            )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectButton.__init__(self, parent)
        self.indicator = self.createcomponent("indicator", (), None,
                                              DirectLabel, (self,),
                                              numStates = 2,
                                              image = self['boxImage'],
                                              image_scale = self['boxImageScale'],
                                              image_color = self['boxImageColor'],
                                              geom = self['boxGeom'],
                                              geom_scale = self['boxGeomScale'],
                                              geom_color = self['boxGeomColor'],
                                              state = 'disabled',
                                              text = ('X', 'X'),
                                              relief = self['boxRelief'],
                                              )

        self.indicator._comp_update_func = self._indicator_update_func

        # Call option initialization functions
        self.initialiseoptions(DirectRadioButton)
        # After initialization with X giving it the correct size, put back space
        if self['boxGeom'] is None:
            if not 'boxRelief' in kw and self['boxImage'] is None:
                self.indicator['relief'] = DGG.SUNKEN
            self.indicator['text'] = (' ', '*')
            if not base.gui_controller.no_initopts:
                self.indicator['text_pos'] = (0, -.25)
            # self.indicator.component("text0").set_pos(0, 0, .25)
        else:
            self.indicator['text'] = (' ', ' ')

        if self['boxGeomColor'] != None and self['boxGeom'] != None:
            self.colors = [VBase4(1, 1, 1, 0), self['boxGeomColor']]
            self.component('indicator')['geom_color'] = VBase4(1, 1, 1, 0)

        needToCheck = True
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                if self['variable'][i] != self['value'][i]:
                    needToCheck = False
                    break

        if needToCheck:
            self.check()

        # Apply the theme to self
        self.add_theming_options(kw, parent, DirectRadioButton)

    def _indicator_update_func(self, **kwargs):
        for key in kwargs:
            if "text" in key:
                return

        self.indicator.resetFrameSize()

    def _update_box_geom_image(self):
        skip = False
        if (self.indicator["geom"] is None and self["boxGeom"] is None and
                self.indicator["image"] is None and self["boxImage"] is None):
            skip = True

        self.indicator["geom"] = self["boxGeom"]
        if self["boxGeomColor"] is not None:
            self.indicator["geom_color"] = self["boxGeomColor"]
        if self["boxGeomScale"] is not None:
            self.indicator["geom_scale"] = self["boxGeomScale"]

        self.indicator["image"] = self["boxImage"]
        if self["boxImageColor"] is not None:
            self.indicator["image_color"] = self["boxImageColor"]
        if self["boxImageScale"] is not None:
            self.indicator["image_scale"] = self["boxImageScale"]

        self.indicator["relief"] = self["boxRelief"]

        if self['boxGeom'] is None:
            if self["boxImage"] is None and self['boxRelief'] is None:
                self.indicator['relief'] = DGG.SUNKEN
            self.indicator['text'] = ('X', 'X')
            self.indicator.setFrameSize()
            self.indicator['text'] = (' ', '*')
            # self.indicator['text_pos'] = (0, -.25)
            self.indicator.component("text0").set_pos(0, 0, .25)

        else:
            self.indicator['text'] = (' ', ' ')
            self.indicator.setFrameSize()

        if not skip:
            self.setFrameSize()

        if self['boxGeomColor'] != None and self['boxGeom'] != None:
            self.colors = [VBase4(1, 1, 1, 0), self['boxGeomColor']]
            self.component('indicator')['geom_color'] = VBase4(1, 1, 1, 0)

    def click(self):
        self.commandFunc("")
        self.show_click()

    def activate(self):
        self["selected"] = False

    def deactivate(self):
        pass

    # Override the resetFrameSize of DirectGuiWidget inorder to provide space for label
    def resetFrameSize(self):
        self.setFrameSize(fClearFrame = 1)

    def setFrameSize(self, fClearFrame = 0):

        if self['frameSize']:
            # Use user specified bounds
            self.bounds = self['frameSize']
            frameType = self.frameStyle[0].getType()
            ibw = self.indicator['borderWidth']
        else:
            # Use ready state to compute bounds
            frameType = self.frameStyle[0].getType()
            if fClearFrame and (frameType != PGFrameStyle.TNone):
                self.frameStyle[0].setType(PGFrameStyle.TNone)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])
                # To force an update of the button
                self.guiItem.getStateDef(0)
            # Clear out frame before computing bounds
            self.getBounds()
            # Restore frame style if necessary
            if (frameType != PGFrameStyle.TNone):
                self.frameStyle[0].setType(frameType)
                self.guiItem.setFrameStyle(0, self.frameStyle[0])

            # Ok, they didn't set specific bounds,
            #  let's add room for the label indicator
            #  get the difference in height

            ibw = self.indicator['borderWidth']
            indicatorWidth = (self.indicator.getWidth() + (2*ibw[0]))
            indicatorHeight = (self.indicator.getHeight() + (2*ibw[1]))
            if "text0" in self.components():
                text = self.component("text0")
                text_bounds = text.getTightBounds()
            else:
                text_bounds = (Vec3(0), Vec3(0))
            text_width = text_bounds[1].x - text_bounds[0].x
            text_height = text_bounds[1].z - text_bounds[0].z
            diff_y = (max(indicatorHeight, text_height) + (2 * self['boxBorder']) -
                      (self.bounds[3] - self.bounds[2]))

            # check size in x direction to fit the indicator
            space_left = (self.bounds[1] - self.bounds[0]) - text_width - self["borderWidth"][0]
            diff_x = indicatorWidth + 2 * self['boxBorder'] - space_left

            # If background is smaller then indicator, enlarge background
            if self['boxPlacement'] == 'left':            #left
                self.bounds[0] += -diff_x
                self.bounds[3] += diff_y / 2
                self.bounds[2] -= diff_y / 2
            elif self['boxPlacement'] == 'below':          #below
                self.bounds[2] += -(indicatorHeight+(2*self['boxBorder']))
            elif self['boxPlacement'] == 'right':          #right
                self.bounds[1] += diff_x
                self.bounds[3] += diff_y / 2
                self.bounds[2] -= diff_y / 2
            else:                                    #above
                self.bounds[3] += indicatorHeight + (2*self['boxBorder'])

        # Set frame to new dimensions
        if ((frameType != PGFrameStyle.TNone) and
                (frameType != PGFrameStyle.TFlat)):
            bw = self['borderWidth']
        else:
            bw = (0, 0)
        # Set frame to new dimensions
        self.guiItem.setFrame(
            self.bounds[0] - bw[0],
            self.bounds[1] + bw[0],
            self.bounds[2] - bw[1],
            self.bounds[3] + bw[1])

        # If they didn't specify a position, put it in the center of new area
        if not self.indicator['pos']:
            bbounds = self.bounds
            lbounds = self.indicator.bounds
            newpos = [0, 0, 0]

            if self['boxPlacement'] == 'left':            #left
                newpos[0] += bbounds[0]-lbounds[0] + self['boxBorder'] + ibw[0]
                dropValue = (bbounds[3]-bbounds[2]-lbounds[3]+lbounds[2])/2 + self['boxBorder']
                newpos[2] += (bbounds[3]-lbounds[3] + self['boxBorder'] -
                              dropValue)
            elif self['boxPlacement'] == 'right':            #right
                newpos[0] += bbounds[1]-lbounds[1] - self['boxBorder'] - ibw[0]
                dropValue = (bbounds[3]-bbounds[2]-lbounds[3]+lbounds[2])/2 + self['boxBorder']
                newpos[2] += (bbounds[3]-lbounds[3] + self['boxBorder']
                              - dropValue)
            elif self['boxPlacement'] == 'above':            #above
                newpos[2] += bbounds[3]-lbounds[3] - self['boxBorder'] - ibw[1]
            else:                                      #below
                newpos[2] += bbounds[2]-lbounds[2] + self['boxBorder'] + ibw[1]

            self.indicator.setPos(newpos[0], newpos[1], newpos[2])

    def commandFunc(self, event):
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                self['variable'][i] = self['value'][i]
        self.check()

    def check(self):
        self['indicatorValue'] = 1
        self.setIndicatorValue()

        for other in self['others']:
            if other != self:
                other.uncheck()

        if self['command']:
            # Pass any extra args to command
            self['command'](*self['extraArgs'])

    def setOthers(self, others):
        self['others'] = others

    def uncheck(self):
        self['indicatorValue'] = 0
        if self.colors != None:
            self.component('indicator')['geom_color'] = self.colors[self['indicatorValue']]

    def setIndicatorValue(self):
        self.component('indicator').guiItem.setState(self['indicatorValue'])
        if self.colors != None:
            self.component('indicator')['geom_color'] = self.colors[self['indicatorValue']]
