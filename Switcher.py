import sublime, sublime_plugin
from os import walk, path
import json

if sublime.version() <= 2174:
  pref = 'Preferences.sublime-settings'
else:
  pref = 'Global.sublime-settings'

switcher = sublime.load_settings('switcher.sublime-settings')
settings = sublime.load_settings(pref)
package_dir = sublime.packages_path()
ignored_packages = settings.get('ignored_packages')

class SwitcherCommand(sublime_plugin.ApplicationCommand):

  def __init__(self):
    self.color_names = []
    self.color_paths = {}
    self.theme_names = []
    self.theme_paths = {}
    self.load_data()

  def run(self, type):
    self.type = type
    if type == "theme":
      self.names = self.theme_names
      self.paths = self.theme_paths
    elif type == "color_scheme":
      self.names = self.color_names
      self.paths = self.color_paths

    window = sublime.active_window()
    window.show_quick_panel(self.names, self.change_setting)

  def change_setting(self, index):
    if index > -1:
      settings.set(self.type, self.paths[self.names[index]])
      sublime.save_settings(pref)
      sublime.status_message('Switcher: changed ' + self.type.replace('_', ' ') + ' to ' + self.names[index])

  def load_data(self):
    for root, subFolders, files in walk(sublime.packages_path()):
      for filename in files:
        name = path.splitext(filename)[0].replace('-', ' ')
        if filename.lower().endswith('.tmtheme'):
          location = path.join("Packages", path.relpath(path.join(root, filename), package_dir))
          self.color_names.append(name)
          self.color_paths[name] = location
        elif filename.endswith('.sublime-theme'):
          if self.theme_paths.get(name) == None:
            self.theme_paths[name] = filename
            self.theme_names.append(name)
    self.theme_names.sort()
    self.color_names.sort()
