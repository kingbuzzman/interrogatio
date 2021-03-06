# pylint: disable=unused-argument

from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, VSplit
from prompt_toolkit.widgets import Label, TextArea

from ..widgets import SelectMany, SelectOne
from .base import QHandler, register


class StringHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:input.answer'
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)
        return VSplit(
            [
                Label(msg,
                      dont_extend_width=True,
                      style='class:input.question'),
                widget
            ],
            padding=1)


    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(result=False)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=True)

        return bindings

    def get_value(self):
        return self.get_widget().text


register('input', StringHandler)



class PasswordHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:password.answer',
            password=True
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)

        return VSplit(
            [
                Label(msg,
                      dont_extend_width=True,
                      style='class:password.question'),
                widget
            ],
            padding=1)

    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=self.get_answer())

        return bindings

register('password', PasswordHandler)


class SelectOneHandler(QHandler):

    def get_widget_class(self):
        return SelectOne

    def get_value(self):
        return self.get_widget().current_value

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectone.answer'
        )
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        return HSplit([
            Label(msg, style='class:selectone.question'),
            self.get_widget()
        ])

    def get_keybindings(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())

        self.get_widget().accept_handler = accept_handler

        return bindings

register('selectone', SelectOneHandler)


class SelectManyHandler(QHandler):


    def get_widget_class(self):
        return SelectMany


    def get_value(self):
        return list(self.get_widget().checked)

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectmany.answer'
        )
        if 'checked' in self._question:
            kwargs['checked'] = set(self._question['checked'])
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )

        return HSplit([
            Label(msg, style='class:selectmany.question'),
            self.get_widget()
        ])

    def get_keybindings(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())

        self.get_widget().accept_handler = accept_handler

        return bindings

register('selectmany', SelectManyHandler)

class TextHandler(QHandler):

    def get_widget_class(self):
        return TextArea


    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=True,
            height=4,
            style='class:text.answer'
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        extra_args = self.get_init_extra_args()
        if 'rows' in extra_args:
            self.get_widget().height = int(extra_args['rows'])
        return VSplit(
            [
                Label(msg,
                      dont_extend_width=True,
                      style='class:text.question'),
                self.get_widget()
            ],
            padding=1)

    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.ControlX)
        def _enter(event):
            get_app().exit(result=self.get_answer())

        return bindings


class PathHandler(StringHandler):
    def get_widget(self):
        widget = super(PathHandler, self).get_widget()
        widget.completer = PathCompleter()
        return widget

register('path', PathHandler)

class RePasswordHandler(QHandler):

    ALIAS = 'repassword'


    def __init__(self, *args, **kwargs):
        super(RePasswordHandler, self).__init__(*args, **kwargs)
        self._rewidget = TextArea(**self.get_widget_init_kwargs())
        self._rewidget.buffer.cursor_position = len(self._rewidget.text)


    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:repassword.answer',
            password=True
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        extra_args = self.get_init_extra_args()
        remsg = '{}{}'.format(
            extra_args.get('remessage', 'Please repeat to confirm'),
            self._question.get('question_mark', ' ?')
        )
        lbl_msg = Label(msg,
                        dont_extend_width=True,
                        style='class:repassword.question')
        lbl_remsg = Label(remsg,
                          dont_extend_width=True,
                          style='class:repassword.question')
        return HSplit(
            [
                VSplit([lbl_msg, self.get_widget()], padding=1),
                VSplit([lbl_remsg, self._rewidget], padding=1)
            ]
        )

    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)


        @bindings.add('tab')
        def _tab(event):
            get_app().layout.focus_next()

        @bindings.add('s-tab')
        def _stab(event):
            get_app().layout.focus_previous()

        @bindings.add(Keys.Enter)
        def _enter(event):
            if get_app().layout.has_focus(self._rewidget):
                get_app().exit(result=self.get_answer())
            else:
                get_app().layout.focus_next()

        return bindings

    def is_valid(self):
        extra_args = self.get_init_extra_args()
        super(RePasswordHandler, self).is_valid()
        if self.get_widget().text != self._rewidget.text:
            self._errors.append(
                extra_args.get(
                    'reerror',
                    'Password and repeat password doesn\'t match'
                )
            )
        return not self.errors

register('repassword', RePasswordHandler)
