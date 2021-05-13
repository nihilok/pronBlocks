from ursina import ButtonList, TextField


class MyInput(TextField):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.update_func = update_func

    def input(self, key):
        super().input(key)


class MyButtonList(ButtonList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = None

    def input(self, key):
        super().input(key)
        if key == 'down arrow':
            y = round(abs(self.highlight.y / self.button_height))
            if y < len(self.actions) - 1:
                if not self.selection_marker.enabled:
                    self.selection_marker.enable()
                else:
                    self.highlight.y -= self.button_height
                self.selection_marker.y = self.highlight.y
                y = round(abs(self.highlight.y / self.button_height))
            self.action = self.actions[y]

        if key == 'up arrow':
            y = round(abs(self.highlight.y / self.button_height))
            if y > 0:
                if not self.selection_marker.enabled:
                    self.selection_marker.enable()
                else:
                    self.highlight.y += self.button_height
                self.selection_marker.y = self.highlight.y
                y = round(abs(self.highlight.y / self.button_height))
            self.action = self.actions[y]
