"""Module with subclass of DirectGuiWidget that implements keyboard navigation."""
from __future__ import annotations
import direct.gui.DirectGuiBase as DirectGuiBase
import direct.gui.DirectGuiGlobals as DGG
import panda3d.core as p3d

from typing import Any

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
    base: ShowBase

__all__ = ["DirectGuiWidget"]


class DirectGuiWidget(DirectGuiBase.DirectGuiWidget):
    """Subclass of DirectGuiWidget with keyboard navigation support."""

    def __init__(self, parent=None, **kw):
        # True for default implementation (using node-graph to infer jump order)
        # False for disabled
        # To specify a jump explicitly, pass the object that should be jumped to
        navigationMap = {
            "u": True,  # 'up' move upward (by default upwards in the node-graph)
            "d": True,  # 'down' inverse of 'up'
            "l": True,  # 'left' move left (to next gui node at the current level of the node-graph)
            "r": True,  # 'right' inverse of 'left'
            "i": False,  # 'inward'
            "o": False,  # 'outward'

            "f": True,  # 'forward' move to next item (to next gui node in the node-graph)
            "b": True  # 'backward' inverse of 'forward' (backward in the node-graph)
        }

        optiondefs = (
            ('selectable',     False,         None),
            ('selected',       False,         self.set_selected),
            ('navigationMap',  navigationMap, None),
            ('frameTextureCenter',  None,  self.update_frame_texture),
            ('frameTextureEdge',  None,  self.update_frame_texture),
            ('frameTextureCorner',  None,  self.update_frame_texture)
        )
        if not hasattr(self, "_kw"):
            self._kw = {}
        if not hasattr(self, "_theme"):
            self._theme: dict[str, Any] | None = None
            self._theme_priority = -1

        # Merge keyword options with theme from gui_controller
        kw = self.add_theming_options(kw, parent)

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGuiBase.DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectGuiWidget)

        self.bind(DGG.B1PRESS, self._set_active)
        self.update_frame_texture()

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame)
        # if "frameSize" in self._optionInfo and self["frameSize"] is None:
        #     self._optionInfo["frameSize"][DGG._OPT_VALUE] = list(self.bounds)
#
    def initialiseoptions(self, myClass):
        super().initialiseoptions(myClass)
        self.fix_frame_size()

    def fix_frame_size(self):
        # return
        if self.guiItem.hasFrame() and self["frameSize"] is None:
            print(self["frameSize"])
            # self["frameSize"] = list(self.guiItem.getFrame())
            self._optionInfo["frameSize"][DGG._OPT_VALUE] = list(self.guiItem.getFrame())
            print(self["frameSize"])

    def setBorderWidth(self):
        super().setBorderWidth()
        self.update_frame_texture()

    def update_frame_texture(self):
        # this might be a single texture or a list of textures (does not currently support several textures)
        center = self['frameTextureCenter']
        edge = self['frameTextureEdge']
        corner = self['frameTextureCorner']
        if not all((center, edge, corner)):
            self.setShaderOff(1)
            for node in self.stateNodePath:
                node.setShaderOff(1)
            return

        tex_dict = {"center": center, "edge": edge, "corner": corner}
        for key, tex in tex_dict.items():
            if isinstance(tex, str):
                tex = base.loader.loadTexture(tex)
                tex_dict[key] = tex
            elif isinstance(tex, p3d.Texture):
                pass
            else:
                print(f"{tex=} has invalid type: {type(tex)}")

        if self["frameSize"] is not None and self["frameSize"] != (0, 0, 0, 0):
            size = self["frameSize"]

        elif self.guiItem.hasFrame():
            size = self.guiItem.getFrame()
        else:
            size = self.getBounds()

        aspect_ratio = (size[1] - size[0])/(size[3] - size[2])

        shader = p3d.Shader.load(p3d.Shader.SL_GLSL,
                                 vertex="BetterDirectGui/Shaders/frame.vert",
                                 fragment="BetterDirectGui/Shaders/frame.frag")
        self.setShader(shader)
        self.setShaderInputs(**tex_dict,
                             borderWidth=self["borderWidth"],
                             size=aspect_ratio)
        for node in self.stateNodePath:
            # node.setShader(shader)
            # node.setShaderInputs(**tex_dict,
            #                      borderWidth=self["borderWidth"],
            #                      size=aspect_ratio)
            for child in node.children:
                child.setShaderOff(1)

    def set_theme(self, theme: dict, priority=0):
        """Set theme of this element and its children to the specified theme.

        :param theme: The new theme.
        :param priority: Requires a higher value than the current themes priority to override.
        """
        if priority <= self._theme_priority:
            return

        self._theme_priority = priority
        self._theme = theme
        if type(self).__name__ in theme:
            gui_theme = theme[type(self).__name__]
            for key, value in gui_theme.items():
                if key in self._kw:
                    continue

                self[key] = value

        children = base.gui_controller._get_gui_children(self)
        for child in children:
            child.set_theme(theme, priority)

    def clear_theme(self):
        """Remove the theming options from this element and its children."""
        if self._theme is None:
            return

        for name, default, func in self.options():
            if name in self._theme[type(self).__name__] and name not in self._kw:
                self[name] = default

        self._theme_priority = -1
        self._theme = None

        children = base.gui_controller._get_gui_children(self)
        for child in children:
            child.clear_theme()

    def add_theming_options(self, kw: dict, parent: DirectGuiWidget | None):
        """Merge kw with the theming specified in guiController.

        :param parent: The parent element of self
        :param kw: The keywords given by the user.
        :return: kw
        """
        if not hasattr(self, "_kw"):
            self._kw = kw.copy()

        if not base.gui_controller._do_theming:
            return kw

        name = type(self).__name__
        if base.gui_controller._is_gui(parent) and parent._theme is not None:
            themes = parent._theme
            self._theme = themes
            self._theme_priority = parent._theme_priority

        elif base.gui_controller.gui_themes is not None and name in base.gui_controller.gui_themes:
            themes = base.gui_controller.gui_themes
            self._theme = themes
            self._theme_priority = base.gui_controller.gui_theme_priority

        else:
            return kw

        theme = themes[name]
        kwargs = kw.copy()
        for key, value in theme.items():
            if key not in kwargs:
                kwargs[key] = value

        return kwargs

    def bind(self, event, command, extraArgs=[]):
        """Bind the command (which should expect one arg) to the specified
        event (such as ENTER, EXIT, B1PRESS, B1CLICK, etc.)
        See DirectGuiGlobals for possible events
        """
        if event == DGG.B1PRESS:  # Make sure _set_active still is bound
            def func(*args, **kwargs):
                if command != self._set_active:
                    command(*args, **kwargs)
                self._set_active(*args, **kwargs)
        else:
            func = command

        super().bind(event, func, extraArgs)

    def unbind(self, event):
        """Unbind the specified event"""
        super().unbind(event)
        if event == DGG.B1PRESS:  # Make sure _set_active is still bound
            self.bind(DGG.B1PRESS, self._set_active)

    def destroy(self):
        self["navigationMap"] = None
        super().destroy()

    def _set_active(self, event, skip_activate=True):
        if not base.gui_controller.do_keyboard_navigation:
            return

        if self["selectable"]:
            if base.gui_controller.current_selection is not None and base.gui_controller.current_selection is not self:
                base.gui_controller.current_selection["selected"] = False

            base.gui_controller.current_selection = self
            if skip_activate:
                base.gui_controller._skip_activate = True
                base.gui_controller._activate()
                base.gui_controller._skip_activate = False
            else:
                base.gui_controller._activate()

    def navigate_next(self, direction: str = "f"):
        """Navigate to next gui element in 'direction'.
        If that element is not specified in navigationMap use default implementation to find the next element.

        :param direction: A string matching a key from the navigationMap dict (i.e. "f", "b", "i", "o").
        """
        option = self["navigationMap"][direction]
        if option is False:
            return

        if option is True:
            base.gui_controller._default_implementation(direction)
            return

        base.gui_controller.current_selection = option

    def override_navigation_map(self, direction: str, next_item: DirectGuiWidget):
        """Change keys and values in the navigationMap.

        :param direction: The direction to alter.
        :param next_item: The element to select when navigating in that direction.
        """
        nav_map = self["navigationMap"]
        nav_map[direction] = next_item
        opposite_direction = base.gui_controller.get_opposite_direction(direction)
        next_item["navigationMap"][opposite_direction] = self

    def set_selected(self):
        """Handle the state of self when selected/deselected."""
        if self["selected"]:
            if not base.gui_controller._skip_activate:
                self.click()
            self.activate()
        else:
            if not base.gui_controller._skip_activate:
                self.unclick()
            self.deactivate()

    def click(self):
        """Do the stuff that would normally happen when element is clicked.
        Is only called when navigating with keyboard.
        """
        self.show_click()

    def show_click(self):
        """Show that the element is selected by changing its scale."""
        self._scale = self.get_scale()
        self.set_scale(self._scale * 0.95)

    def unclick(self):
        """Do stuff that would normally happen when user clicks away from element.
        Is only called when navigating with keyboard.
        """
        self.show_unclick()

    def show_unclick(self):
        """Reset the scale changed in show_click."""
        if hasattr(self, "_scale"):
            self.do_method_later(0.1, self.set_scale, "unclick", [self._scale])

    def activate(self):
        """Do the stuff that need to happen for element to be selected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        print("activate")

    def deactivate(self):
        """Do the stuff that need to happen for element to be deselected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        print("deactivate")

    def highlight(self):
        """Method to be called when element is the "current_selection"
        (not selected, just the current node for the GuiController) to highlight it."""
        self._color_scale = p3d.LVecBase4(self.getColorScale())
        self.setColorScale(*base.gui_controller.highlight_color)

    def unhighlight(self):
        """Method to be called when element is no longer the "current_selection"
        (not selected, just the current node for the GuiController) to unhighlight it."""
        if hasattr(self, "_color_scale"):
            self.set_color_scale(self._color_scale)
        else:
            self.setColorScale(1, 1, 1, 1)
