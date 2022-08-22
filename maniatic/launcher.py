import gi

gi.require_versions(
    dict(
        Gtk="4.0",
        Adw="1",
    )
)

from gi.repository import Gtk, Adw, Gio
from .setup_game import DATA_DEST, launch_game
import shutil as sh

MESSAGE = """\
The app couldn't find a copy of Sonic Mania installed on Steam.

We can't legally distribute the assets (sprites, levels, music, etc.)
from the game, so you need to provide your legal copy of it.
"""


class ImportData(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        self.set_valign(Gtk.Align.CENTER)
        self.set_margin_start(32)
        self.set_margin_end(32)
        self.set_margin_top(32)
        self.set_margin_bottom(32)

        title = Gtk.Label()
        title.set_markup("Not so fast!")
        title.get_style_context().add_class("title-1")

        text = Gtk.Label()
        text.set_markup(MESSAGE)
        text.set_justify(Gtk.Justification.CENTER)

        buy_mania_title = Gtk.Label()

        self.append(title)
        self.append(text)


@Gtk.Template(resource_path="/io/github/santiagocezar/maniatic-launcher/main.ui")
class LauncherWindow(Adw.ApplicationWindow):
    __gtype_name__ = "LauncherWindow"

    description = Gtk.Template.Child()

    def on_import_response(self, chooser: Gtk.FileChooserNative, res: int):
        print("response:", res)
        if res == Gtk.ResponseType.ACCEPT:
            file = chooser.get_file()
            path = str(file.get_path())
            sh.copy(path, DATA_DEST)
            self.close()

    @Gtk.Template.Callback()
    def on_import(self, *args):
        print("clicked")
        self._native = Gtk.FileChooserNative.new(
            title="Open Data.rsdk", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        # chooser = Gtk.FileChooser(native)

        self._native.connect("response", self.on_import_response)
        self._native.show()

    def __init__(self, app: Adw.Application) -> None:
        super().__init__(application=app)
        self.description.set_label(MESSAGE)
        self.present()


def on_activate(app: Adw.Application):
    win = LauncherWindow(app)
    win.present()


def main():
    app = Adw.Application(application_id="io.github.santiagocezar.maniatic-launcher")

    css = Gtk.CssProvider()
    css.load_from_resource("/io/github/santiagocezar/maniatic-launcher/style.css")

    app.connect("activate", on_activate)
    app.run()
