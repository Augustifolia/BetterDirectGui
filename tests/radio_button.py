from BetterDirectGui.DirectGui import *

v = [0]
# Add some text
bk_text = "This is my Demo"
textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
                          fg=(1, 0.5, 0.5, 1),
                          mayChange=True)


# Callback function to set  text
def setText(status=None):
    bk_text = "CurrentValue : %s"%v
    textObject.setText(bk_text)


# Add button
buttons = [
    DirectRadioButton(text='RadioButton0', variable=v, value=[0],
                      scale=0.05, pos=(-0.4, 0, 0), command=setText),
    DirectRadioButton(text='RadioButton1', variable=v, value=[1],
                      scale=0.05, pos=(0, 0, 0), command=setText),
    DirectRadioButton(text='RadioButton2', variable=v, value=[2],
                      scale=0.05, pos=(0.4, 0, 0), command=setText)
]

for button in buttons:
    button.setOthers(buttons)
