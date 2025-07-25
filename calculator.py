from textual.app import App
from textual.widgets import Button, Footer, Header, Input
from textual.containers import HorizontalGroup, VerticalScroll

class MyNum(HorizontalGroup):

    def compose(self):
        yield Button()

class myApp(App):
    pass

if(__name__=='__main__'):
    app = myApp()
    app.run()