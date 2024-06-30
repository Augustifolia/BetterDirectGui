import direct.gui.DirectGuiGlobals as DGG
from panda3d.core import Filename
import os


root = Filename.fromOsSpecific(os.path.dirname(__file__))

__all__ = ["default_theme"]


default_theme = {
    "general": dict(
        text_shadow=(.6, .6, .6, 1),
        text_shadowOffset=(0.05, 0.05),
        relief=DGG.TEXTUREBORDER,
        frameTexture=f"{root}/assets/border.png",
        borderUvWidth=(.15, .15),
        transparency=True,
        frameColor=(.4, .7, .4, 1),
    ),
    "DirectButton": dict(
        frameColor=(0.1, 1, 1, 1),
        text_shadow=(.4, .4, .7, 1),
    ),
    "DirectEntry": dict(
        # enteredText="initial text",
        # numLines=3,
        # overflow=1,
    ),
    "DirectCheckButton": dict(
        indicatorValue=1,
        boxRelief=DGG.TEXTUREBORDER,
        # indicator_borderWidth=(.2, .2),
        boxBorder=.1,
        indicator_borderUvWidth=(.1, .1),
    ),
    "OkDialog": dict(
        # buttonTextList=["Ok", "No"],
        # buttonValueList=[DGG.DIALOG_OK, DGG.DIALOG_NO]
        borderWidth=(.1, .1),
        button_borderWidth=(.1, .1),
        button_relief=DGG.TEXTUREBORDER
    ),
    "DirectScrollBar": dict(
        # borderWidth=(0.01, 0.01),
        # thumb_frameColor=(1, 1, .1, 1)
    ),
    "DirectScrolledFrame": dict(
        scrollBarWidth=0.03,
        borderWidth=(.03, .03),
        borderUvWidth=(.08, .08),
        verticalScroll_thumb_frameColor=[1, .1, 1, 1]
    ),
    "DirectOptionMenu": dict(
        cancelframe_frameColor=(0, 0, 0, 0)
    ),
    "DirectScrolledList": dict(
        itemFrame_frameColor=(1, 1, 1, 1),
        # items_relief=DGG.TEXTUREBORDER
    ),
    "DirectWaitBar": dict(
        borderWidth=(.1, .1),
    ),
    "DirectRadioButton": dict(
        boxRelief=DGG.TEXTUREBORDER,
        boxBorder=.1,
        # boxPlacement="right",
        indicator_borderUvWidth=(.1, .1),
    ),
    "DraggableTile": dict(
        borderWidth=(.05, .05),
    ),
}
