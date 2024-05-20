"""A DirectCheckButton is a type of button that toggles between two states
when clicked.  It also has a separate indicator that can be modified
separately.

See the :ref:`directcheckbutton` page in the programming manual for a more
in-depth explanation and an example of how to use this class.
"""

__all__ = ['DirectCheckButton']

from panda3d.core import *
from .DirectButton import *
from .DirectLabel import *


class DirectCheckButton(DirectButton):
    """
    DirectCheckButton(parent) - Create a DirectGuiWidget which responds
    to mouse clicks by setting a state of on or off and execute a callback
    function (passing that state through) if defined
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
            # boxBorder defines the space created around the check box
            # ('boxBorder', 0, None),
            # boxPlacement maps left, above, right, below
            # ('boxPlacement', 'left', None),
            # ('boxImage', None, None),
            # ('boxImageScale', 1, None),
            # ('boxImageColor', None, None),
            # ('boxRelief', 'sunken', None),
            ('selectable', True, None),
        )
        if base.gui_controller.no_initopts:
            optiondefs += (
                ('boxBorder', 0, self.setFrameSize),
                # boxPlacement maps left, above, right, below
                ('boxPlacement', 'left', self._update_box_placement),
                ('boxImage', None, self._update_box_image),
                ('boxImageScale', 1, self._update_box_image),
                ('boxImageColor', None, self._update_image_color),
                ('boxRelief', 'sunken', self._update_box_relief),
            )
        else:
            optiondefs += (
                ('boxBorder', 0, None),
                # boxPlacement maps left, above, right, below
                ('boxPlacement', 'left', None),
                ('boxImage', None, None),
                ('boxImageScale', 1, None),
                ('boxImageColor', None, None),
                ('boxRelief', 'sunken', None),
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
                                              state = 'disabled',
                                              text = ('X', 'X'),
                                              relief = self['boxRelief'],
                                              )

        # Call option initialization functions
        self.initialiseoptions(DirectCheckButton)
        # After initialization with X giving it the correct size, put back space
        if self['boxImage'] ==  None:
            self.indicator['text'] = (' ', '*')
            if not base.gui_controller.no_initopts:
                self.indicator['text_pos'] = (0, -.2)
            # self.indicator.component("text0").set_pos(0, 0, .2)
        else:
            self.indicator['text'] = (' ', ' ')
        if self['boxImageColor'] != None and self['boxImage'] !=  None:
            self.colors = [VBase4(0, 0, 0, 0), self['boxImageColor']]
            self.component('indicator')['image_color'] = VBase4(0, 0, 0, 0)

        # Apply the theme to self
        self.add_theming_options(kw, parent, DirectCheckButton)

    def _update_box_relief(self):
        self.indicator["relief"] = self["boxRelief"]

    def _update_box_placement(self):
        self.setFrameSize()

    def _update_box_image(self):
        skip = False
        if self.indicator["image"] is None and self["boxImage"] is None:
            skip = True
        self.indicator["image"] = self["boxImage"]
        if self["boxImageScale"] is not None:
            self.indicator["image_scale"] = self["boxImageScale"]
        if self["boxImageColor"] is not None:
            self.indicator["image_color"] = self["boxImageColor"]

        if self['boxImage'] ==  None:
            self.indicator['text'] = ('X', 'X')
            self.indicator.resetFrameSize()
            self.indicator['text'] = (' ', '*')
            self.indicator.component("text0").set_pos(0, 0, .2)  # for some reason this was required to line it up
            # self.indicator['text_pos'] = (0, -.2)
        else:
            self.indicator['text'] = (' ', ' ')
            self.indicator.resetFrameSize()
        if self['boxImageColor'] != None and self['boxImage'] !=  None:
            self.colors = [VBase4(0, 0, 0, 0), self['boxImageColor']]
            self.component('indicator')['image_color'] = VBase4(0, 0, 0, 0)
        if not skip:
            self.setFrameSize()

    def _update_image_color(self):
        if self["boxImageColor"] is not None:
            self.indicator["image_color"] = self["boxImageColor"]

        if self['boxImageColor'] != None and self['boxImage'] !=  None:
            self.colors = [VBase4(0, 0, 0, 0), self['boxImageColor']]
            self.component('indicator')['image_color'] = VBase4(0, 0, 0, 0)

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
            diff_y = (indicatorHeight + (2 * self['boxBorder']) -
                      (self.bounds[3] - self.bounds[2]))

            # check size in x direction to fit the indicator
            if "text0" in self.components():
                text = self.component("text0")
                text_bounds = text.getTightBounds()
            else:
                text_bounds = (Vec3(0), Vec3(0))
            text_width = text_bounds[1].x - text_bounds[0].x
            space_left = (self.bounds[1] - self.bounds[0]) - text_width - 2 * self["borderWidth"][0]
            diff_x = indicatorWidth + 2 * self['boxBorder'] - space_left

            # If background is smaller then indicator, enlarge background
            if self['boxPlacement'] == 'left':  # left
                self.bounds[0] += -diff_x
                self.bounds[3] += diff_y / 2
                self.bounds[2] -= diff_y / 2
            elif self['boxPlacement'] == 'below':  # below
                self.bounds[2] += -(indicatorHeight + (2 * self['boxBorder']))
            elif self['boxPlacement'] == 'right':  # right
                self.bounds[1] += diff_x
                self.bounds[3] += diff_y / 2
                self.bounds[2] -= diff_y / 2
            else:  # above
                self.bounds[3] += indicatorHeight + (2 * self['boxBorder'])

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
        self['indicatorValue'] = 1 - self['indicatorValue']
        if self.colors != None:
            self.component('indicator')['image_color'] = self.colors[self['indicatorValue']]

        if self['command']:
            # Pass any extra args to command
            self['command'](*[self['indicatorValue']] + self['extraArgs'])

    def setIndicatorValue(self):
        self.component('indicator').guiItem.setState(self['indicatorValue'])
        if self.colors != None:
            self.component('indicator')['image_color'] = self.colors[self['indicatorValue']]







