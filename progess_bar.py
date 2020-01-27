import kivy
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyWidget(Widget): 

	progress_bar = ObjectProperty()

	def __init__(self, **kwa):
		super(MyWidget, self).__init__(**kwa)

		self.progress_bar = ProgressBar()
		self.popup = Popup(
			title ='Download',
			content = self.progress_bar
		)
		self.popup.bind(on_open = self.puopen)
		self.add_widget(Button(text ='Download', on_release = self.pop))

	# the function which works when you clicj = k the button
	def pop(self, instance):
		self.progress_bar.value = 1
		self.popup.open()

	# To continuesly increasing the value of pb.
	def next(self, dt):
		if self.progress_bar.value>= 100:
			return False
		self.progress_bar.value += 1

	# def puopen(self, instance):
		Clock.schedule_interval(self.next, 1 / 25)

# Create the App class
class MyApp(App):
	def build(self):
		return MyWidget()

# run the App
if __name__ in ("__main__"):
	MyApp().run()
