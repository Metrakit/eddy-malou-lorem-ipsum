import sublime
import sublime_plugin
import random
import json
from os.path import dirname, realpath

class MalouCommand(sublime_plugin.TextCommand):

    dictionary = []
    sizes_json = {
        "malou-xs": 1,
        "malou-sm": 2,
        "malou-md": 3,
        "malou-lg": 4,
    }
    sizes_list = []

    def makeParagraph(self, size):

        number = self.sizes_json[size]

        paragraph = ""

        for i in range(number):
            paragraph += random.choice (self.dictionary['sentences_1']) + " "
            paragraph += random.choice (self.dictionary['sentences_2']) + " "
            paragraph += random.choice (self.dictionary['sentences_3']) + " "
            paragraph += random.choice (self.dictionary['sentences_4']) + " "
            paragraph += random.choice (self.dictionary['sentences_5']) + " "
            paragraph += random.choice (self.dictionary['sentences_6']) + " "
            paragraph += random.choice (self.dictionary['sentences_7'])
            paragraph += random.choice (self.dictionary['sentences_8']) + ". "
        return paragraph[:-1]

    def run(self, edit, nb=1):

        for i in self.sizes_json:
            self.sizes_list.append(i)

        nb=nb-1

        package_path = "Packages/EddyMalouLoremIpsum"
        jsonfile = package_path + "/dictionary.json"
        content = sublime.load_resource(jsonfile)  
        self.dictionary = json.loads(content)

        selects = self.view.sel()
        for select in selects:

            default = sublime.Region(select.begin() - 5, select.begin())
            size = sublime.Region(select.begin() - 8, select.begin())

            current_text = self.view.substr(size).lower()
            if current_text not in self.sizes_list:
                current_text = self.view.substr(default).lower()

            if current_text == 'malou':
                txt = str(self.makeParagraph('malou-xs'))
                self.view.erase(edit, default)
                select = sublime.Region(default.begin())
            elif current_text in self.sizes_list:
                txt = str(self.makeParagraph(current_text))
                self.view.erase(edit, size)
                select = sublime.Region(size.begin())
            else:
                txt = str(self.makeParagraph(self.sizes_list[nb]))
                self.view.erase(edit, select)

            self.view.insert(edit, select.begin(), txt)
