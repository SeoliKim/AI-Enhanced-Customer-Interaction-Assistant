import time
import os
import sys
import base64
import mesop as me
import random
from dataclasses import asdict, dataclass
from typing import Callable, Literal


# Add the parent directory to the Python path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.main import MainAssistant

Role = Literal["user", "bot"]


_APP_TITLE = "Ecommerce Chatbot"
_BOT_AVATAR_LETTER = "M"
_EMPTY_CHAT_MESSAGE = "Get started with an example"
_EXAMPLE_USER_QUERIES = (
    "Track my order _your_id_",
    "Recommend me a new microwave",
    "I want the item in this image",
)
_CHAT_MAX_WIDTH = "800px"
_MOBILE_BREAKPOINT = 640

assistant = MainAssistant()


@dataclass(kw_only=True)
class ChatMessage:
    """Chat message metadata."""

    role: Role = "user"
    content: str = ""
    image: me.UploadedFile = None
    edited: bool = False
    # 1 is positive
    # -1 is negative
    # 0 is no rating
    rating: int = 0


@me.stateclass
class State:
    input: str
    uploadedimage: me.UploadedFile
    inputimage: bool
    output: list[ChatMessage]
    in_progress: bool
    sidebar_expanded: bool = False
    # Need to use dict instead of ChatMessage due to serialization bug.
    # See: https://github.com/google/mesop/issues/659
    history: list[list[dict]]


def respond_to_chat(input: str, history: list[ChatMessage]):
    state = me.state(State)
    try:
        print(input)
        state.in_progress = True
        yield ""
        response = assistant.graph.invoke({"messages": [("user", input)]}, assistant.config)
        state.in_progress = False
        msg=response["messages"][-1]
        if hasattr(msg, 'content'):
            for l in msg.content:
                time.sleep(0.0005)
                yield(l)
        elif isinstance(msg, tuple) and len(msg) == 2:
            yield(msg[1])
    except Exception as e:
        print(e)
        yield ""

def on_load(e: me.LoadEvent):
    me.set_theme_mode("system")


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=[
            "https://google.github.io", "https://huggingface.co"]
    ),
    title="Ecommerce Assistant",
    on_load=on_load,
)
def page():
    state = me.state(State)

    with me.box(
        style=me.Style(
            background=me.theme_var("surface-container-lowest"),
            display="flex",
            flex_direction="column",
            height="100%",
        )
    ):
        with me.box(
            style=me.Style(
                display="flex", flex_direction="row", flex_grow=1, overflow="hidden"
            )
        ):
            with me.box(
                style=me.Style(
                    background=me.theme_var("surface-container-low"),
                    display="flex",
                    flex_direction="column",
                    flex_shrink=0,
                    position="absolute"
                    if state.sidebar_expanded and _is_mobile()
                    else None,
                    height="100%" if state.sidebar_expanded and _is_mobile() else None,
                    width=300 if state.sidebar_expanded else None,
                    z_index=2000,
                )
            ):
                sidebar()

            with me.box(
                style=me.Style(
                    display="flex",
                    flex_direction="column",
                    flex_grow=1,
                    padding=me.Padding(left=60)
                    if state.sidebar_expanded and _is_mobile()
                    else None,
                )
            ):
                header()
                with me.box(style=me.Style(flex_grow=1, overflow_y="scroll")):
                    if state.output:
                        chat_pane()
                    else:
                        examples_pane()
                chat_input()


def sidebar():
    state = me.state(State)
    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="column",
            flex_grow=1,
        )
    ):
        with me.box(style=me.Style(display="flex", gap=20)):
            menu_icon(icon="menu", tooltip="Menu", on_click=on_click_menu_icon)

        if state.sidebar_expanded:
            menu_item(icon="add", label="New chat", on_click=on_click_new_chat)
        else:
            menu_icon(icon="add", tooltip="New chat",
                      on_click=on_click_new_chat)

        if state.sidebar_expanded:
            history_pane()


def history_pane():
    state = me.state(State)
    for index, chat in enumerate(state.history):
        with me.box(
            key=f"chat-{index}",
            on_click=on_click_history,
            style=me.Style(
                background=me.theme_var("surface-container"),
                border=me.Border.all(
                    me.BorderSide(
                width=1, color=me.theme_var("outline-variant"), style="solid"
                        )
                ),
                border_radius=5,
                cursor="pointer",
                margin=me.Margin.symmetric(horizontal=10, vertical=10),
                padding=me.Padding.all(10),
                text_overflow="ellipsis",
            ),
        ):
            me.text(_truncate_text(chat[0]["content"]))


def header():
    state = me.state(State)
    with me.box(
        style=me.Style(
            align_items="center",
            background=me.theme_var("surface-container-lowest"),
            display="flex",
            gap=5,
            justify_content="space-between",
            padding=me.Padding.symmetric(horizontal=20, vertical=10),
        )
    ):
        with me.box(style=me.Style(display="flex", gap=5)):
            me.text(
                _APP_TITLE,
                style=me.Style(margin=me.Margin(bottom=0),
                               font_size=36,
                               font_weight=700,
                               background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                               color="transparent",),
                type="headline-6",
            )

        with me.box(style=me.Style(display="flex", gap=5)):
            icon_button(
                key="",
                icon="dark_mode" if me.theme_brightness() == "light" else "light_mode",
                tooltip="Dark mode"
                if me.theme_brightness() == "light"
                else "Light mode",
                on_click=on_click_theme_brightness,
            )


def examples_pane():
    with me.box(
        style=me.Style(
            margin=me.Margin.symmetric(horizontal="auto"),
            padding=me.Padding.all(15),
            width=f"min({_CHAT_MAX_WIDTH}, 100%)",
        )
    ):
        with me.box(style=me.Style(margin=me.Margin(top=25), font_size=24)):
            me.text(_EMPTY_CHAT_MESSAGE)

        with me.box(
            style=me.Style(
                display="flex",
                flex_direction="column" if _is_mobile() else "row",
                gap=20,
                margin=me.Margin(top=25),
            )
        ):
            for index, query in enumerate(_EXAMPLE_USER_QUERIES):
                if index <2: 
                    with me.box(
                        key=f"query-{index}",
                        on_click=on_click_example_user_query,
                        style=me.Style(
                            background=me.theme_var("surface-container-highest"),
                            border_radius=15,
                            padding=me.Padding.all(20),
                            cursor="pointer",
                        ),
                    ):
                        me.text(query)
                else:
                    with me.box(
                        style=me.Style(
                                background=me.theme_var("surface-container-highest"),
                                border_radius=15,
                                padding=me.Padding.all(20),
                                cursor="pointer",
                            ),
                    ):
                        me.text(query)
                        me.content_uploader(
                            accepted_file_types=["image/jpeg", "image/png"],
                            on_upload=submit_image,
                            style=me.Style(
                                width= "100%",
                                height="100%"
                            )
                        )
                            
                         
                
                    

def chat_pane():
    state = me.state(State)
    with me.box(
        style=me.Style(
            background=me.theme_var("surface-container-lowest"),
            color=me.theme_var("on-surface"),
            display="flex",
            flex_direction="column",
            margin=me.Margin.symmetric(horizontal="auto"),
            padding=me.Padding.all(15),
            width=f"min({_CHAT_MAX_WIDTH}, 100%)",
        )
    ):
        for index, msg in enumerate(state.output):
            if msg.role == "user":
                user_message(message=msg)
            else:
                bot_message(message_index=index, message=msg)

        if state.in_progress:
            with me.box(key="scroll-to", style=me.Style(height=250)):
                pass


def user_message(*, message: ChatMessage):
    with me.box(
        style=me.Style(
            display="flex",
            gap=15,
            justify_content="end",
            margin=me.Margin.all(20),
        )
    ):
        if message.image == None:
            with me.box(
                style=me.Style(
                    background=me.theme_var("surface-container-low"),
                    border_radius=10,
                    color=me.theme_var("on-surface-variant"),
                    padding=me.Padding.symmetric(vertical=0, horizontal=10),
                    # width="6",
                )
            ):
                me.markdown(message.content)
        else:
             with me.box(style=me.Style(display="flex", flex_direction="column")):
                with me.box(
                style=me.Style(
                    background=me.theme_var("surface-container-low"),
                    border_radius=10,
                    color=me.theme_var("on-surface-variant"),
                    padding=me.Padding.symmetric(vertical=0, horizontal=10),
                    # width="6",
                )
                ):
                    if message.image.size:
                        with me.box(style=me.Style(margin=me.Margin.all(10))):
                            me.text(f"File name: {message.image.name}")

                        with me.box(style=me.Style(margin=me.Margin.all(10))):
                            me.image(
                                src=_convert_contents_data_url(message.image),
                                style=me.Style(
                                    width="200px",
                                    )
                                )

  
def bot_message(*, message_index: int, message: ChatMessage):
    with me.box(style=me.Style(display="flex", gap=15, margin=me.Margin.all(20))):
        text_avatar(
            background=me.theme_var("primary"),
            color=me.theme_var("on-primary"),
            label=_BOT_AVATAR_LETTER,
        )

        # Bot message response 
        with me.box(style=me.Style(display="flex", flex_direction="column")):
            me.markdown(
                message.content,
                style=me.Style(color=me.theme_var("on-surface")),
            )

            # Actions panel
            with me.box():
                icon_button(
                    key=f"thumb_up-{message_index}",
                    icon="thumb_up",
                    is_selected=message.rating == 1,
                    tooltip="Good response",
                    on_click=on_click_thumb_up,
                )
                icon_button(
                    key=f"thumb_down-{message_index}",
                    icon="thumb_down",
                    is_selected=message.rating == -1,
                    tooltip="Bad response",
                    on_click=on_click_thumb_down,
                )



def chat_input():
    state = me.state(State)
    with me.box(
        style=me.Style(
            background=me.theme_var("surface-container")
            if _is_mobile()
            else me.theme_var("surface-container"),
            border_radius=16,
            display="flex",
            margin=me.Margin.symmetric(horizontal="auto", vertical=15),
            padding=me.Padding.all(8),
            width=f"min({_CHAT_MAX_WIDTH}, 90%)",
        )
    ):
        with me.box(
            style=me.Style(
                flex_grow=1,
            )
        ):
            me.native_textarea(
                autosize=True,
                key="chat_input",
                min_rows=4,
                on_blur=on_chat_input,
                shortcuts={
                    me.Shortcut(shift=True, key="Enter"): on_submit_chat_msg,
                },
                placeholder="Enter your prompt",
                style=me.Style(
                    background=me.theme_var("surface-container")
                    if _is_mobile()
                    else me.theme_var("surface-container"),
                    border=me.Border.all(
                        me.BorderSide(style="none"),
                    ),
                    color=me.theme_var("on-surface-variant"),
                    outline="none",
                    overflow_y="auto",
                    padding=me.Padding(top=16, left=16),
                    width="100%",
                ),
                value=state.input,
            )
        with me.content_button(
            disabled=state.in_progress,
            on_click=on_click_submit_chat_msg,
            type="icon",
        ):
            me.icon("send")
            
        with me.content_uploader(
            disabled=state.in_progress,
            accepted_file_types=["image/jpeg", "image/png"],
            on_upload=submit_image,
            type="icon",
            style=me.Style(font_weight="bold"),
        ):
            me.icon("photo")


@me.component
def text_avatar(*, label: str, background: str, color: str):
    me.text(
        label,
        style=me.Style(
            background=background,
            border_radius="50%",
            color=color,
            font_size=20,
            height=40,
            line_height="1",
            margin=me.Margin(top=16),
            padding=me.Padding(top=10),
            text_align="center",
            width="40px",
        ),
    )


@me.component
def icon_button(
    *,
    icon: str,
    tooltip: str,
    key: str = "",
    is_selected: bool = False,
    on_click: Callable | None = None,
):
    selected_style = me.Style(
        background=me.theme_var("surface-container-low"),
        color=me.theme_var("on-surface-variant"),
    )
    with me.tooltip(message=tooltip):
        with me.content_button(
            type="icon",
            key=key,
            on_click=on_click,
            style=selected_style if is_selected else None,
        ):
            me.icon(icon)


@me.component
def menu_icon(
    *, icon: str, tooltip: str, key: str = "", on_click: Callable | None = None
):
    with me.tooltip(message=tooltip):
        with me.content_button(
            key=key,
            on_click=on_click,
            style=me.Style(margin=me.Margin.all(10)),
            type="icon",
        ):
            me.icon(icon)


@me.component
def menu_item(
    *, icon: str, label: str, key: str = "", on_click: Callable | None = None
):
    with me.box(on_click=on_click):
        with me.box(
            style=me.Style(
                background=me.theme_var("surface-container-high"),
                border_radius=20,
                cursor="pointer",
                display="inline-flex",
                gap=10,
                line_height=1,
                margin=me.Margin.all(10),
                padding=me.Padding(top=10, left=10, right=20, bottom=10),
            ),
        ):
            me.icon(icon)
            me.text(label, style=me.Style(height=24, line_height="24px"))


# Event Handlers


def on_click_example_user_query(e: me.ClickEvent):
    """Populates the user input with the example query"""
    state = me.state(State)
    _, example_index = e.key.split("-")
    state.input = _EXAMPLE_USER_QUERIES[int(example_index)]
    me.focus_component(key="chat_input")


def on_click_thumb_up(e: me.ClickEvent):
    """Gives the message a positive rating"""
    state = me.state(State)
    _, msg_index = e.key.split("-")
    msg_index = int(msg_index)
    state.output[msg_index].rating = 1


def on_click_thumb_down(e: me.ClickEvent):
    """Gives the message a negative rating"""
    state = me.state(State)
    _, msg_index = e.key.split("-")
    msg_index = int(msg_index)
    state.output[msg_index].rating = -1


def on_click_new_chat(e: me.ClickEvent):
    """Resets messages."""
    state = me.state(State)
    if state.output:
        state.history.insert(0, [asdict(messages)
                             for messages in state.output])
    state.output = []
    me.focus_component(key="chat_input")


def on_click_history(e: me.ClickEvent):
    """Loads existing chat from history and saves current chat"""
    state = me.state(State)
    _, chat_index = e.key.split("-")
    chat_messages = [
        ChatMessage(**chat) for chat in state.history.pop(int(chat_index))
    ]
    if state.output:
        state.history.insert(0, [asdict(messages)
                             for messages in state.output])
    state.output = chat_messages
    me.focus_component(key="chat_input")


def on_click_theme_brightness(e: me.ClickEvent):
    """Toggles dark mode."""
    if me.theme_brightness() == "light":
        me.set_theme_mode("dark")
    else:
        me.set_theme_mode("light")


def on_click_menu_icon(e: me.ClickEvent):
    """Expands and collapses sidebar menu."""
    state = me.state(State)
    state.sidebar_expanded = not state.sidebar_expanded


def on_chat_input(e: me.InputBlurEvent):
    """Capture chat text input on blur."""
    state = me.state(State)
    state.input = e.value


def on_click_regenerate(e: me.ClickEvent):
    """Regenerates response from an existing message"""
    state = me.state(State)
    _, msg_index = e.key.split("-")
    msg_index = int(msg_index)

    # Get the user message which is the previous message
    user_message = state.output[msg_index - 1]
    # Get bot message to be regenerated
    assistant_message = state.output[msg_index]
    assistant_message.content = ""
    state.in_progress = True
    yield

    start_time = time.time()
    # Send in the old user input and chat history to get the bot response.
    # We make sure to only pass in the chat history up to this message.
    output_message = respond_to_chat(
        user_message.content, state.output[:msg_index]
    )
    for content in output_message:
        assistant_message.content += content
        # TODO: 0.25 is an abitrary choice. In the future, consider making this adjustable.
        if (time.time() - start_time) >= 0.25:
            start_time = time.time()
            yield

    state.in_progress = False
    me.focus_component(key="chat_input")
    yield


def on_submit_chat_msg(e: me.TextareaShortcutEvent):
    state = me.state(State)
    state.input = e.value
    yield
    yield from _submit_chat_msg()


def on_click_submit_chat_msg(e: me.ClickEvent):
    yield from _submit_chat_msg()


def _submit_chat_msg():
    """Handles submitting a chat message."""
    state = me.state(State)
    if state.in_progress or not state.input:
        return
    
    output = state.output
    if output is None:
        output = []
        
    input = state.input
    state.input = ""
    output.append(ChatMessage(role="user", content=input))
        
    if state.uploadedimage:
        print("Image uploaded")
        input = input + f" Image URL: {_convert_contents_data_url(state.uploadedimage)}"
        state.uploadedimage = None
        
    # Clear the text input.
    yield
    
    state.in_progress = True
    me.scroll_into_view(key="scroll-to")
    yield

    start_time = time.time()
    # Send user input and chat history to get the bot response.
    output_message = respond_to_chat(input, state.output)
    assistant_message = ChatMessage(role="bot")
    output.append(assistant_message)
    state.output = output
    for content in output_message:
        assistant_message.content += content
        # TODO: 0.25 is an abitrary choice. In the future, consider making this adjustable.
        if (time.time() - start_time) >= 0.25:
            start_time = time.time()
            yield

    state.in_progress = False
    me.focus_component(key="chat_input")
    yield

def _convert_contents_data_url(file: me.UploadedFile) -> str:
  return (
    f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
  )
  
def submit_image(event: me.UploadEvent):
    """Handles submitting an image."""
    state = me.state(State)
    if state.in_progress or not event.file:
        return
    image = event.file
    state.uploadedimage= image
    
    state.input= "identify the object in the image"
    
    output = state.output
    if output is None:
        output = []
    output.append(ChatMessage(role="user", image=image))
    yield _submit_chat_msg


def _is_mobile():
    return me.viewport_size().width < _MOBILE_BREAKPOINT


def _truncate_text(text, char_limit=100):
    """Truncates text that is too long."""
    if len(text) <= char_limit:
        return text
    truncated_text = text[:char_limit].rsplit(" ", 1)[0]
    return truncated_text.rstrip(".,!?;:") + "..."
