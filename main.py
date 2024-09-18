# -*-coding:utf-8 -*-
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.key_binding import KeyBindings

from core.init import Init

bindings = KeyBindings()


@bindings.add('c-c')
def _(event):
    " Exit when `ctrl-c` is pressed. "
    event.app.exit()


def main():
    # 主函数
    # input_memory_history = InMemoryHistory()
    input_word_completer = WordCompleter(
        ['help',
         'credential',
         'login',
         'exit']
    )
    prompt_session = PromptSession('[>>] ', completer=input_word_completer, cursor=CursorShape.BLINKING_BEAM,
                                   key_bindings=bindings)

    init = Init()
    while True:
        prompt_input = prompt_session.prompt()
        if prompt_input == 'credential':
            init.set_login_credential()
        if prompt_input == 'login':
            init.set_login_url()
        elif prompt_input == 'exit':
            break

    sys.exit(0)


if __name__ == '__main__':
    main()