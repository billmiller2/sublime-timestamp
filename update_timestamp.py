import sublime
import sublime_plugin
import os
import time


class UpdateTimestampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            original = self.view.file_name()
            root, filename = os.path.split(original)

            if not os.access(original, os.W_OK):     
                sublime.error_message(filename + " is read-only")
                return

            if '_' in filename:
                first = filename.split('_', 1)[0]

                if self.isNumeric(first) and len(first) == 10:
                    filename = filename.split('_', 1)[-1]

            timestamp = str(time.time()).split('.', 1)[0]
            updated = os.path.join(root, timestamp + '_' + filename)
            os.rename(original, updated)

            view = self.view.window().find_open_file(original)
            if view:
                view.retarget(updated)

        except Exception as e:
            sublime.status_message('Error: ' + str(e))

    def isNumeric(self, string):
        try: 
            int(string)
            return True
        except ValueError:
            return False
