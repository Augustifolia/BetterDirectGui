"""Module with some default themes to get more modern gui:s out of the box."""
import direct.gui.DirectGuiGlobals as DGG
from panda3d.core import Filename
import os
from BetterDirectGui.GuiTools import ThemeUtil


# some useful directories
root = Filename.fromOsSpecific(os.path.dirname(os.path.dirname(__file__)))
assets = Filename.fromOsSpecific(os.path.join(root, "assets"))
dark = Filename.fromOsSpecific(os.path.join(assets, "dark"))
light = Filename.fromOsSpecific(os.path.join(assets, "light"))

__all__ = ["default_theme", "dark_theme"]


default_theme = {
    "general": dict(
        # text_shadow=(.6, .6, .6, 1),
        # text_shadowOffset=(0.05, 0.05),
        relief=DGG.TEXTUREBORDER,
        frameTexture=f"{assets}/frame.png",
        # borderUvWidth=(.15, .15),

        frameColor=(.4, .7, .4, 1),
        borderWidth=(.05, .05),
        text_scale=1/12,
        text_fg=(0, 0, 0, 1),
        transparency=True,
    ),
    "DirectButton": dict(

    ),
    "DirectCheckBox": dict(
        uncheckedImage=f"{assets}/toggle_off.png",
        checkedImage=f"{assets}/toggle_on.png",
        image_scale=0.05,
    ),
    "DirectCheckButton": dict(
        boxRelief=DGG.FLAT,
        # indicator_scale=0.2,  # does not update properly
        indicator_frameSize=[-.05, .05, -.05, .05],
        indicator_frameTexture=(f"{assets}/toggle_off.png", f"{assets}/toggle_on.png"),
        indicator_frameColor=(1, 1, 1, 1),
        indicator_borderWidth=(.0, .0),
        indicator_relief=DGG.FLAT,
        indicator_text=" ",
    ),
    "OkCancelDialog": dict(
        # buttonTextList=["Ok", "No"],
        # buttonValueList=[DGG.DIALOG_OK, DGG.DIALOG_NO]
        # borderWidth=(.1, .1),
        # button_borderWidth=(.1, .1),
        button_relief=DGG.TEXTUREBORDER,
    ),
    "DirectEntry": dict(

    ),
    "DirectEntryScroll": dict(

    ),
    "DirectFrame": dict(
        frameTexture=f"{assets}/borderless.png",
    ),
    "DirectLabel": dict(

    ),
    "DirectOptionMenu": dict(
        # popupMarker_numStates=2,
        cancelframe_frameColor=(0, 0, 0, 0),
        highlightScale=(1/12, 1/12),
        popupMarker_frameTexture=(f"{assets}/arrow_down.png", f"{assets}/arrow_right.png"),
        popupMarker_frameColor=(.1, .6, .1, 1),
        popupMarker_relief=DGG.FLAT,
        popupMarker_frameSize=(-0.08, 0.08, -0.08, 0.08),
    ),
    "DirectRadioButton": dict(
        boxRelief=DGG.FLAT,
        # indicator_scale=0.2,  # does not update properly
        indicator_frameSize=[-.05, .05, -.05, .05],
        # indicator_frameTexture=("models/maps/circle.png", "models/maps/envir-bamboo.png"),
        indicator_frameTexture=f"{assets}/radio.png",
        indicator_frameColor=(
            (.4, .4, .4, 1),  # unselected
            (.1, .7, .1, 1),  # selected
            (.1, .1, .1, 1),
            (.1, .1, .1, 1)
        ),
        indicator_borderWidth=(.0, .0),
        indicator_text=" ",
    ),
    "DirectScrollBar": dict(
        thumb_frameTexture=f"{assets}/borderless.png",
        thumb_frameColor=(.1, .5, .1, 1),
        incButton_frameTexture=f"{assets}/borderless.png",
        incButton_frameColor=(.1, .5, .1, 1),
        decButton_frameTexture=f"{assets}/borderless.png",
        decButton_frameColor=(.1, .5, .1, 1),
    ),
    "DirectScrolledFrame": dict(
        verticalScroll_borderWidth=(.4, .4),
        horizontalScroll_borderWidth=(.4, .4),
        scrollBarWidth=0.05,
        borderWidth=(.01, .01),
        borderUvWidth=(.03, .03),
    ),
    "DirectScrolledList": dict(
        itemFrame_frameColor=(.1, .5, .1, 1),
        # items_relief=DGG.TEXTUREBORDER,
        decButton_pos=(0.35, 0, 0.58),
        decButton_text="Dec",
        # decButton_text_scale=0.04,  # todo for some reason this crashes
        decButton_borderWidth=(0.03, 0.03),

        incButton_pos=(0.35, 0, -0.07),
        incButton_text="Inc",
        incButton_borderWidth=(0.03, 0.03),

        frameSize=(0.0, 0.7, -0.15, 0.69),
        pos=(-.35, 0, 0),
        numItemsVisible=3,
        forceHeight=.1,
        itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
        itemFrame_pos=(0.35, 0, 0.4),
    ),
    "DirectSlider": dict(
        thumb_frameTexture=f"{assets}/borderless.png",
        thumb_frameColor=(.1, .5, .1, 1),
    ),
    "DirectWaitBar": dict(
        # borderWidth=(.1, .1),
        # barBorderWidth=(.5, .5),
        barColor=(.1, .5, .4, 1),
        borderUvWidth=(.05, .05),
        borderWidth=(.03, .03),
    ),
    "DraggableTile": dict(

    ),
    "DraggableItem": dict(

    ),
    "DirectDatePicker": dict(

    ),
    "DirectSpinBox": dict(

    ),
}

dark_theme = ThemeUtil.merge(
    default_theme,
    {
        "general": dict(
            text_fg=(1, 1, 1, 1),
            frameTexture=f"{dark}/frame.png",
            frameColor=(
                (.1, .6, .1, 1),
                (.1, .5, .1, 1),
                (.1, .4, .1, 1),
                (.1, .3, .1, 1),
            ),
        ),
        "DirectButton": dict(

        ),
        "DirectCheckBox": dict(

        ),
        "DirectCheckButton": dict(

        ),
        "OkCancelDialog": dict(

        ),
        "DirectEntry": dict(
            cursorColor=(1, 1, 1, 1),
        ),
        "DirectEntryScroll": dict(

        ),
        "DirectFrame": dict(
            frameColor=(0, 0, 0, 1),
        ),
        "DirectLabel": dict(

        ),
        "DirectOptionMenu": dict(

        ),
        "DirectRadioButton": dict(

        ),
        "DirectScrollBar": dict(

        ),
        "DirectScrolledFrame": dict(

        ),
        "DirectScrolledList": dict(
            itemFrame_frameColor=(.2, .2, .2, 1),
        ),
        "DirectSlider": dict(

        ),
        "DirectWaitBar": dict(

        ),
        "DraggableTile": dict(

        ),
        "DraggableItem": dict(

        ),
        "DirectDatePicker": dict(

        ),
        "DirectSpinBox": dict(

        ),
    }
)
