import sys
from typing import Optional

from l_parser import extract_comments
from rich.style import StyleType
from rich.syntax import Syntax
from textual import events
from textual.app import App
from textual.widgets import ScrollView


class LockedScrollView(ScrollView):
    def __init__(
        self,
        to_lock: "LockedScrollView" = None,
        contents: None = None,
        name: Optional[str] = None,
        style: StyleType = "",
        fluid: bool = True,
    ) -> None:
        super().__init__(contents=contents, name=name, style=style, fluid=fluid)

        self.to_lock = to_lock

    def lock_to(self, to_lock: "LockedScrollView"):
        self.to_lock = to_lock

    # async def watch_x(self, new_value: float, first=True) -> None:
    #     await super().watch_x(new_value)

    #     if self.to_lock is not None and first:
    #         await self.to_lock.watch_x(new_value, False)

    # async def watch_y(self, new_value: float, first=True) -> None:
    #     await super().watch_y(new_value)

    #     if self.to_lock is not None and first:
    #         await self.to_lock.watch_y(new_value, False)

    def scroll_up(self, first=True) -> None:
        super().scroll_up()

        if self.to_lock is not None and first:
            self.to_lock.scroll_up(False)

    def scroll_down(self, first=True) -> None:
        super().scroll_down()

        if self.to_lock is not None and first:
            self.to_lock.scroll_down(False)

    async def key_up(self, first=True) -> None:
        await super().key_up()

        if self.to_lock is not None and first:
            await self.to_lock.key_up(False)

    async def key_down(self, first=True) -> None:
        await super().key_down()

        if self.to_lock is not None and first:
            await self.to_lock.key_down(False)


class LangTUI(App):
    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        # await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        filename = sys.argv[1]

        code = LockedScrollView(name="code")
        commentView = LockedScrollView(to_lock=code, name="comments")
        code.lock_to(commentView)

        await self.view.dock(code, commentView, edge="left")

        async def get_code(filename: str):
            with open(filename, "rt") as f:
                highlighted = Syntax(f.read(), "python", line_numbers=True)

            await code.update(highlighted)

        async def get_comments(filename: str):
            comments = extract_comments(filename)

            contents = ""
            last_line = 0

            for comment, line in comments:
                contents += "\n" * (line - last_line) + comment
                last_line = line

            await commentView.update(contents)

        await self.call_later(get_code, filename)
        await self.call_later(get_comments, filename)


LangTUI.run(log="textual.log")
