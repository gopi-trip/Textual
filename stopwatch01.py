from time import monotonic
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header
from textual.reactive import reactive

class TimeDisplay(Digits):
    """A widget to display elapsed time"""
    
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
    
    def on_mount(self) -> None:
        """ Event Handler called when widget is added to the app """
        self.update_timer = self.set_interval(1/60, self.update_time,pause=True)
        
        
    def update_time(self) -> None:
        """ Method to update the time to the current time """
        self.time = self.total + (monotonic() - self.start_time)
    
    def watch_time(self,time:float) -> None:
        """ Called when the time attribute changes. """
        minutes, seconds = divmod(time,60)
        hours,minutes = divmod(minutes,60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")
    
    def start(self) -> None:
        """ Method to start (or resume) with updating """
        self.start_time = monotonic()
        self.update_timer.resume()
        
    def stop(self) -> None:
        """ Method to stop the time display updating """
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total
    
    def reset(self) -> None:
        """ Method to reset the time display to zero """
        self.total = 0
        self.time = 0
        
class Stopwatch(HorizontalGroup):
    """ A Stopwatch widget. """
    
    def on_button_pressed(self,event: Button.Pressed) -> None:
        
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == 'start':
            time_display.start()
            self.add_class('started')
        elif button_id == 'stop':
            time_display.stop()
            self.remove_class('started')
        elif button_id == 'reset':
            time_display.reset()
    
    def compose(self) -> ComposeResult:
        """ Create child widgets of a stopwatch """
        yield Button("Start",id='start',variant="success")
        yield Button("Stop",id="stop",variant="error")
        yield Button("Reset",id='reset',variant='primary')
        yield TimeDisplay()

class StopwatchApp(App):
    """A Textual app to manage stopwatches."""
    CSS_PATH = 'stopwatch.tcss'
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("a","add_stopwatch","Add"),
                ("r","remove_stopwatch","Remove")
                ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(),Stopwatch(),Stopwatch(),id='timers')

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
        
    def action_add_stopwatch(self) -> None:
        """ An action to add a timer """
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        """ Called to remove a timer """
        timers = self.query("Stopwatch")
        if(timers):
            timers.last().remove()
            

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()