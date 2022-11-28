import eel
from screeninfo import get_monitors
m0 = get_monitors()[0]


eel.init('web')

@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)

eel.say_hello_js('connected!')   # Call a Javascript function


eel.start('main.html', size=(m0.width,m0.height), mode = 'chrome')    # Start


