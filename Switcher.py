import sublime, sublime_plugin
import os
import json

if sublime.version() <= 2174:
	pref = 'Preferences.sublime-settings'
else:
	pref = 'Global.sublime-settings'

def get_files(extension):
	settings = sublime.load_settings(pref)
	package_dir = sublime.packages_path()
	ignored_packages = settings.get('ignored_packages')
	results = []

	for root, subFolders, files in os.walk(sublime.packages_path()):
		for filename in files:
			if filename.endswith(extension):
				print filename, package_dir
				results.append(os.path.join("Packages", os.path.relpath(os.path.join(root, filename), package_dir)))

	print results



def get_themes():
	pass

def get_colour_schemes():
	pass

class SwitcherCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		get_files('.tmTheme')
		# self.view.insert(edit, 0, get)

