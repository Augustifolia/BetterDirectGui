"""Module with subclass of DirectGuiWidget that implements keyboard navigation.
Along with some other features that BetterDirectGui offers."""
from __future__ import annotations
import direct.gui.DirectGuiBase as DirectGuiBase
import direct.gui.DirectGuiGlobals as DGG
import panda3d.core as p3d
from BetterDirectGui.GuiTools import GuiUtil

from typing import Any
from collections.abc import MutableSequence, MutableMapping, MutableSet
from copy import deepcopy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from direct.showbase.ShowBase import ShowBase
    base: ShowBase

__all__ = ["DirectGuiWidget"]

DGG.MWUP = p3d.PGButton.getPressPrefix() + p3d.MouseButton.wheel_up().getName() + '-'
DGG.MWDOWN = p3d.PGButton.getPressPrefix() + p3d.MouseButton.wheel_down().getName() + '-'


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
            # Is this element able to be selected, or is it skipped when navigating with keyboard
            ('selectable',     False,         None),
            # Is this element the currently selected element (activates when user presses "enter")
            ('selected',       False,         self.set_selected),
            # if user should be able to exit this element with some key from "allowed_directions_while_selected" while this element is selected
            ('allowExit',      True,          None),
            # map to specify explicitly how to navigate from this element
            ('navigationMap',  navigationMap, None)
        )

        if base.gui_controller.no_initopts:
            optiondefs += (
                ('pos', None, self._set_pos),
                ('hpr', None, self._set_hpr),
                ('scale', None, self._set_scale),
                ('color', None, self._set_color),
                ('transparency', None, self._set_transparency),
                # Do events pass through this widget?
                ('suppressMouse', 1, self._suppress_mouse_and_keys),
                ('suppressKeys', 0, self._suppress_mouse_and_keys),
                ('enableEdit', 1, self._enable_edit),
            )

        # Do not override if it already exists
        if not hasattr(self, "_kw"):
            self._kw = {}
        if not hasattr(self, "_theme"):
            self._theme: dict[str, dict[str: Any]] | None = None
            self._theme_priority = -1
        self._dont_edit: set[str] = set()  # set of stuff not to touch when setting a theme, this has already been handled

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize the base classes (after defining the options).
        DirectGuiBase.DirectGuiWidget.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DirectGuiWidget)

        # If this is parented to some scrolled frame, make sure that can be scrolled
        self._is_child_of_scrolled_frame = False
        self._handle_parent_scrolling()

        # make sure to update stuff for keyboard navigation when self is pressed with the mouse.
        self.bind(DGG.B1PRESS, self._set_active)

        # Apply the theme to self
        self.add_theming_options(kw, parent, DirectGuiWidget)

    def hide(self, *args):
        super().hide(*args)
        if base.gui_controller.do_keyboard_navigation and self["selected"]:
            self["selected"] = False
            base.gui_controller.activate_keys()

    def stash(self, *args, **kwargs):
        super().stash(*args, **kwargs)
        if base.gui_controller.do_keyboard_navigation and self["selected"]:
            self["selected"] = False
            base.gui_controller.activate_keys()

    def _comp_update_func(self, **kwargs):
        self.resetFrameSize()

    def createcomponent(
        self,
        componentName,
        componentAliases,
        componentGroup,
        widgetClass,
        *widgetArgs,
        **kw,
    ):
        # Make sure to include any options set earlier
        itemKW = {}
        # check for component group
        if componentGroup is not None:
            for i in self._kw:
                if i.startswith(f"{componentGroup}_"):
                    itemKW[i.removeprefix(f"{componentGroup}_")] = self._kw[i]

        # override with values set for this specific component
        for i in self._kw:
            if i.startswith(f"{componentName}_"):
                itemKW[i.removeprefix(f"{componentName}_")] = self._kw[i]

        kw.update(itemKW)
        return super().createcomponent(componentName, componentAliases, componentGroup, widgetClass, *widgetArgs, **kw)

    def _handle_parent_scrolling(self):
        # Make sure that children of DirectScrolledFrames get bound to scroll events
        # to make sure scrolling works properly
        if self._is_child_of_scrolled_frame:
            self.unbind(DGG.MWUP)
            self.unbind(DGG.MWDOWN)
            self._is_child_of_scrolled_frame = False

        ancestors = self.getAncestors()
        for ancestor in ancestors:
            if ancestor.name == "canvas":
                node = ancestor.parent.parent
                name = node.name.split("-")[-1]
                try:
                    self._is_child_of_scrolled_frame = self.guiDict[name].setup_scroll_bind(self)
                except AttributeError:
                    pass

                break

    # is needed to make sure scrolling is updated in all directScrolledFrames
    def reparentTo(self, *args, **kwargs):
        super().reparentTo(*args, **kwargs)
        self._handle_parent_scrolling()

    reparent_to = reparentTo

    def wrtReparentTo(self, *args, **kwargs):
        super().wrtReparentTo(*args, **kwargs)
        self._handle_parent_scrolling()

    wrt_reparent_to = wrtReparentTo

    def _set_pos(self):
        if self['pos']:
            self.setPos(self['pos'])

    def _set_hpr(self):
        if self['hpr']:
            self.setHpr(self['hpr'])

    def _set_scale(self):
        if self['scale']:
            self.setScale(self['scale'])

    def _set_color(self):
        if self['color']:
            self.setColor(self['color'])

    def _set_transparency(self):
        if self["transparency"] is not None:
            self.setTransparency(self["transparency"])

    def _enable_edit(self):
        # Is drag and drop enabled?
        if self['enableEdit'] and self.guiEdit:
            self.enableEdit()
        else:
            self.disableEdit()

    def _suppress_mouse_and_keys(self):
        # Set up event handling
        suppressFlags = 0
        if self['suppressMouse']:
            suppressFlags |= p3d.MouseWatcherRegion.SFMouseButton
            suppressFlags |= p3d.MouseWatcherRegion.SFMousePosition
        if self['suppressKeys']:
            suppressFlags |= p3d.MouseWatcherRegion.SFOtherButton
        self.guiItem.setSuppressFlags(suppressFlags)

    def addoptions(self, optionDefs, optionkeywords):
        """ addoptions(optionDefs) - add option def to option info """
        # Add additional options, providing the default value and the
        # method to call when the value is changed.  See
        # "defineoptions" for more details

        # optimisations:
        optionInfo = self._optionInfo
        optionInfo_has_key = optionInfo.__contains__
        keywords = self._constructorKeywords
        keywords_has_key = keywords.__contains__
        FUNCTION = DGG._OPT_FUNCTION

        for name, default, function in optionDefs:
            if '_' not in name:
                default = optionkeywords.get(name, default)
                # The option will already exist if it has been defined
                # in a derived class.  In this case, do not override the
                # default value of the option or the callback function
                # if it is not None.
                if not optionInfo_has_key(name):
                    if keywords_has_key(name):
                        # Overridden by keyword, use keyword value
                        value = keywords[name][0]
                        optionInfo[name] = [default, value, function]
                        # Delete it from self._constructorKeywords
                        del keywords[name]
                    else:
                        # Use optionDefs value
                        value = default
                        if isinstance(default, (MutableSequence, MutableMapping, MutableSet)):  # some bug fixing
                            value = deepcopy(default)
                        optionInfo[name] = [default, value, function]
                elif optionInfo[name][FUNCTION] is None:
                    # Only override function if not defined by derived class
                    optionInfo[name][FUNCTION] = function
            else:
                # This option is of the form "component_option".  If this is
                # not already defined in self._constructorKeywords add it.
                # This allows a derived class to override the default value
                # of an option of a component of a base class.
                if not keywords_has_key(name):
                    keywords[name] = [default, 0]

    def set_theme(self, theme: dict, priority=0, clear_old_theme=True):
        """Set theme of this element and its children to the specified theme.
        The method to call to change the theme after widget creation.

        :param theme: The new theme.
        :param priority: Requires a higher value than the current themes priority to override.
        :param clear_old_theme: Option to reset all options set by the old theme before setting the new one.
        """
        if priority <= self._theme_priority:
            return

        if clear_old_theme:
            self.clear_theme()  # reset any options set by the last theme

        self._theme_priority = priority
        self._theme = theme
        self._apply_theme()

    # todo save "_kw" and "_dont_edit" in the object that actually has the option (might require onscreenText to actually support themability directly)
    def _apply_theme(self):
        theme = self._theme
        priority = self._theme_priority
        if theme is None:
            return

        gui_theme = self._get_theme_options(theme)

        for key, value in gui_theme.items():
            if key in self._kw:  # make sure to not override value set by user
                value = self._kw[key]

            elif key in self._dont_edit:  # some ancestor has already handled this value
                self._dont_edit.remove(key)
                continue

            if "_" in key:  # the option is for some component
                index = key.rfind("_")
                comp_name = key[:index]
                if not self.hascomponent(comp_name):  # for example "text" is not a component, but "text0" is
                    # comp_name += "0"
                    pass
                try:
                    comp = self.component(comp_name)
                except KeyError as e:
                    if key[:index] not in self._dynamicGroups:
                        raise e  # this is a bug, throw the error again
                else:
                    option_name = key[index + 1:]
                    # if hasattr(comp, "_kw") and option_name in comp._kw:
                    #     value = comp._kw[option_name]
                    if hasattr(comp, "_dont_edit"):  # OnscreenText/Image/Geom does not have that
                        # this makes sure thumb_frameColor takes precedence over frameColor in a theme
                        comp._dont_edit.add(option_name)  # make sure the component doesn't override the value just set

            self.configure(**{key: value})

            # make sure to also update the widget if a component has been updated
            self._update_parent(key, value)

        children = GuiUtil.get_gui_children(self)
        for child in children:  # propagate the theme to the children
            child.set_theme(theme, priority)

    def _get_theme_options(self, theme: dict[str: Any]):
        name = type(self).__name__
        parent_class = type(self).__base__.__name__
        gui_theme = {}

        # start with general options, the specific theme for this element overrides values from the general theme
        if "general" in theme:
            gui_theme = theme["general"].copy()

        # check if any options from superclass should be included
        for key, value in theme.items():
            if key.startswith("sub-") and key.endswith(parent_class):
                gui_theme.update(value)
                break

        # add options set for this specific type of element
        if name in theme:
            gui_theme.update(theme[name])  # get theme for this gui-type

        return gui_theme

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

        # make sure to update element if a component has changed
        self._update_parent(key, value)

        self._kw[key] = value  # keep track of the options set directly by the user, used for themability

    def _update_parent(self, key, value):
        if not base.gui_controller.do_bug_fixes:
            return

        # This is just a way to skip the update
        if hasattr(self, "_update_comp"):
            del self._update_comp
            return

        # make sure to update the widget if a component has been updated
        if "_" in key and self._comp_update_func is not None:
            self._comp_update_func(**{key: value})

        # if self is a component: update the parent widget
        parent = GuiUtil.get_parent(self)
        parent = GuiUtil.get_gui(parent)
        if parent is not None:
            for comp in parent.components():
                if self is parent.component(comp):
                    parent._comp_update_func(**{key: value})

    def clear_theme(self):
        """Remove the theming options from this element and its children."""
        if self._theme is None:
            return

        name = type(self).__name__
        options = {option[0]: option[1] for option in self.options()}  # dict with name and default value for options of self
        theme = {}
        if name in self._theme:
            theme = self._theme[name]
        if "general" in self._theme:
            gen_theme: dict[str: Any] = self._theme["general"].copy()
            gen_theme.update(theme)
            theme = gen_theme

        for key in theme:
            if "_" in key:  # this option is for a component of self
                index = key.rfind("_")
                comp_name = key[:index]

                try:  # check if component can be found (this includes subcomponents)
                    comp = self.component(comp_name)
                except KeyError:  # otherwise try appending "0" to the name, needed for stuff like 'text' components
                    comp_name += "0"

                try:
                    comp = self.component(comp_name)
                except KeyError as e:
                    if key[:index] not in self._dynamicGroups:
                        raise e  # this is a bug, throw the error again
                else:
                    option_name = key[index + 1:]
                    default = comp.get_default(option_name)
                    if key in self._kw:  # if user has set the option, use that value instead
                        default = self._kw[key]
                    self.configure(**{key: default})

            # if the current value is different from the theme, the user has overriden the value and we should not change it
            elif self[key] == theme[key]:
                if key not in self._kw:  # value has not been set, reset to default
                    default = options[key]
                    self.configure(**{key: default})

        self._theme_priority = -1
        self._theme = None

        children = GuiUtil.get_gui_children(self)
        for child in children:  # clear the theme for the children
            child.clear_theme()

    def add_theming_options(self, kw: dict, parent: DirectGuiWidget | None, myClass):
        """Merge kw with the theming specified in guiController. Only to be used during initialization.

        :param parent: The parent element of self
        :param kw: The keywords given by the user.
        :return: kw
        """
        if self.__class__ is not myClass:
            return

        self._kw = kw.copy()

        if not base.gui_controller.do_theming:
            return

        name = type(self).__name__
        if GuiUtil.is_gui(parent) and parent._theme is not None:
            themes = parent._theme
            self._theme = themes
            self._theme_priority = parent._theme_priority

        elif base.gui_controller.gui_themes is not None and name in base.gui_controller.gui_themes:
            themes = base.gui_controller.gui_themes
            self._theme = themes
            self._theme_priority = base.gui_controller.gui_theme_priority

        self._apply_theme()

    def get_default(self, option_name: str) -> Any:
        """Get the default value of the option.
        The default in this case meaning either the actual default or the value passed at creation time for self."""
        config = self._optionInfo[option_name]
        return config[DGG._OPT_DEFAULT]

    def copy(self):  # todo make sure components options are also updated (there might be options saved in comp._kw)
        """Creates a copy of self with the same options set and the same theme."""
        new_widget = type(self)(**self._kw)
        if new_widget._theme != self._theme:
            new_widget.set_theme(self._theme, self._theme_priority)

        return new_widget

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

    def isBound(self, event):
        """Check if the given event is bound to self."""
        gEvent = event + self.guiId
        return self.isAccepting(gEvent)

    is_bound = isBound

    def getAllBound(self):
        """Get all events that are bound to self."""
        all_accepting = self.getAllAccepting()
        return [event for event in all_accepting if event.endswith(self.guiId)]

    get_all_bound = getAllBound

    def isUnbound(self, event):
        """Check if the event is not bound to self."""
        gEvent = event + self.guiId
        return self.isIgnoring(gEvent)

    is_unbound = isUnbound

    def _set_active(self, event, skip_activate=True):
        if not base.gui_controller.do_keyboard_navigation:
            return

        base.gui_controller._do_highlight = False

        if self["selectable"]:
            if base.gui_controller.current_selection is None:
                pass
            elif base.gui_controller.current_selection is self:
                pass
            elif not hasattr(base.gui_controller.current_selection,"_optionInfo"):
                pass
            else:
                base.gui_controller.current_selection["selected"] = False

            base.gui_controller.current_selection = self
            if skip_activate:
                base.gui_controller._skip_activate = True
                base.gui_controller._activate()
                base.gui_controller._skip_activate = False
            else:
                base.gui_controller._activate()

        base.gui_controller._do_highlight = True

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
        self.set_scale(self._scale * 0.98)

    def unclick(self):
        """Do stuff that would normally happen when user clicks away from element.
        Is only called when navigating with keyboard.
        """
        self.show_unclick()

    def show_unclick(self):
        """Reset the scale changed in show_click."""
        def reset_scale(scale):
            if self.is_empty():  # Make sure self was not deleted
                return
            self.set_scale(scale)
        if hasattr(self, "_scale"):
            self.do_method_later(0.1, reset_scale, "unclick", [self._scale])

    def activate(self):
        """Do the stuff that need to happen for element to be selected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        # print("activate")
        pass

    def deactivate(self):
        """Do the stuff that need to happen for element to be deselected properly.
        Is both called when element is clicked and when selected with keyboard.
        """
        # print("deactivate")
        pass

    def highlight(self):
        """Method to be called when element is the "current_selection"
        (not selected, just the current node for the GuiController) to highlight it."""
        if not base.gui_controller.do_keyboard_navigation:
            return

        if not base.gui_controller._do_highlight:
            return

        self._color_scale = p3d.LVecBase4(self.getColorScale())
        self.setColorScale(*base.gui_controller.highlight_color)

    def unhighlight(self):
        """Method to be called when element is no longer the "current_selection"
        (not selected, just the current node for the GuiController) to unhighlight it."""
        if hasattr(self, "_color_scale"):
            self.set_color_scale(self._color_scale)
        else:
            self.setColorScale(1, 1, 1, 1)
