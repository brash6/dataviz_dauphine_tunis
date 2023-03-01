from panel.pane import Markdown


class DocMarkdown(Markdown):
    def __init__(self, *args, **params):
        if "style" not in params.keys():
            params["style"] = {"margin-left": "20px", "margin-right":"20px"}

        super().__init__(*args, **params)
