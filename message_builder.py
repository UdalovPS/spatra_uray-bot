from abc import ABC, abstractmethod
from Database.command_handler import CommandHandler
from Database.data_selector import SelectorDataDb



class Builder(ABC):
    @abstractmethod
    def build_chat_id(self) -> None:
        pass

    @abstractmethod
    def build_question(self) -> None:
        pass

    @abstractmethod
    def build_dialogs(self) -> None:
        pass

    @abstractmethod
    def build_pre_answer(self) -> None:
        pass


class ChatId:
    def __init__(self, chat_id=None):
        self.chat_id = chat_id


class Question:
    def __init__(self, question=None):
        self.question = question


class Dialogs:
    def __init__(self, dialog=None, commands=None, emoji=None):
        self.dialog = dialog
        self.commands = commands
        self.emoji = emoji


class DialogsList:
    def __init__(self) -> None:
        self.dialogs_list = []

    def add_obj_in_list(self, obj) -> None:
        self.dialogs_list.append(obj)


class PreAnswer:
    def __init__(self, pre_answer=None):
        self.pre_answer = pre_answer


class AnswerMessage:
    def __init__(self, chat_id, question, dialogs, pre_answer):
        self._id = chat_id
        self._quest = question
        self._dia = dialogs
        self._pre = pre_answer


class TestingBuilder(Builder):
    def build_chat_id(self) -> ChatId:
        return ChatId('Test chat_id')

    def build_question(self) -> Question:
        return Question('Test question', 'Test sticker')

    def build_dialogs(self) -> Dialogs:
        return Dialogs('Test dialogs')

    def build_pre_answer(self) -> PreAnswer:
        return PreAnswer('Test pre_answer')


class StandartDataForAnswer(Builder):
    def __init__(self, message):
        self.message = message
        self.step_id = SelectorDataDb(message).select_step_id_from_db()

    def build_chat_id(self) -> ChatId:
        return ChatId(self.message.chat.id)

    def build_question(self) -> Question:
        question = SelectorDataDb(self.message).select_question_from_db(self.step_id)
        return Question(question)

    def build_dialogs(self) -> Dialogs:
        data_from_db = SelectorDataDb(self.message).select_dialog_from_db(self.step_id)
        if data_from_db == None:
            return Dialogs()
        else:
            dialog_list = DialogsList()
            self.add_objects_in_dialog_list(dialog_list, data_from_db)
            return dialog_list

    def build_pre_answer(self) -> PreAnswer:
        return PreAnswer('Test pre_answer')

    def add_objects_in_dialog_list(self, obj, dialogs) -> None:
        for dialog in dialogs:
            data = Dialogs(*dialog)
            obj.add_obj_in_list(data)


class Director:
    def __init__(self, message_obj):
        self.message = message_obj
        self.test = TestingBuilder()
        self.standart = StandartDataForAnswer(message_obj)

    def create_testing_obj(self) -> AnswerMessage:
        _id = self.test.build_chat_id()
        _que = self.test.build_question()
        _dia = self.test.build_dialogs()
        _pre = self.test.build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)

    def create_answer_to_start_msg(self) -> AnswerMessage:
        CommandHandler('10000, 11000', self.message)
        _id = self.standart.build_chat_id()
        _que = self.standart.build_question()
        _dia = self.standart.build_dialogs()
        _pre = self.standart.build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)


if __name__ == '__main__':
    test = Director()
    test_obj = test.create_testing_obj()
    print(test_obj._id.chat_id)
