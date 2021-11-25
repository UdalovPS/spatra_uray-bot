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

    def build_dialogs(self) -> DialogsList:
        db = SelectorDataDb(self.message)
        data_from_db = db.select_dialog_from_db(self.step_id)
        if db.select_step_id_from_db() > 1:
            if data_from_db != None:
                data_from_db.append(('Назад', 'back', '\U0001F519'))
            else:
                data_from_db = [('Назад', 'back', '\U0001F519')]
        if data_from_db == None:
            return DialogsList()
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


class AnswerWithPersonList(Builder):
    def __init__(self, message):
        self.message = message
        self.step_id = SelectorDataDb(message).select_step_id_from_db()

    def build_chat_id(self) -> ChatId:
        return ChatId(self.message.chat.id)

    def build_question(self) -> Question:
        question = SelectorDataDb(self.message).select_question_from_db(self.step_id)
        return Question(question)

    def build_dialogs(self) -> DialogsList:
        db = SelectorDataDb(self.message)
        data_from_db = db.select_dialog_from_db(self.step_id)
        data_about_all_stud = db.select_data_about_all_persons()
        for item in data_about_all_stud:
            tmp = []
            tmp.append(f"{item[1]} {item[2]}")
            tmp.append(f"{12000 + item[0]}, 13110")
            data_from_db.append(tmp)
        data_from_db.append(('Назад', 'back', '\U0001F519'))
        if data_from_db == None:
            return DialogsList()
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


class AnswerDataAboutOnePerson(Builder):
    def __init__(self, message):
        self.message = message
        self.step_id = SelectorDataDb(message).select_step_id_from_db()

    def build_chat_id(self) -> ChatId:
        return ChatId(self.message.chat.id)

    def build_question(self) -> Question:
        db = SelectorDataDb(self.message)
        person_id = db.select_tmp_personal_id()
        data = db.select_data_about_one_person(person_id)
        question = f"Имя: <strong>{data[1]}</strong>\n" \
                   f"Фамилия: <strong>{data[2]}</strong>\n" \
                   f"Отчество: <strong>{data[3]}</strong>\n" \
                   f"Дата рождения: <strong>{data[4]}</strong>\n" \
                   f"Пояс: <strong>{data[5]}</strong>"
        return Question(question)

    def build_dialogs(self) -> DialogsList:
        db = SelectorDataDb(self.message)
        data_from_db = db.select_dialog_from_db(self.step_id)
        if db.select_step_id_from_db() > 1:
            if data_from_db != None:
                data_from_db.append(('Назад', 'back', '\U0001F519'))
            else:
                data_from_db = [('Назад', 'back', '\U0001F519')]
        if data_from_db == None:
            return DialogsList()
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

    def create_testing_obj(self) -> AnswerMessage:
        _id = self.test.build_chat_id()
        _que = self.test.build_question()
        _dia = self.test.build_dialogs()
        _pre = self.test.build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)

    def create_standart_answer_to_msg(self) -> AnswerMessage:
        standart = StandartDataForAnswer(self.message)
        _id = standart.build_chat_id()
        _que = standart.build_question()
        _dia = standart.build_dialogs()
        _pre = standart.build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)

    def create_answer_to_start_msg(self) -> AnswerMessage:
        CommandHandler('10000, 11000', self.message)
        return self.create_standart_answer_to_msg()

    def choice_answer_to_text_message(self) -> AnswerMessage:
        step_id = SelectorDataDb(self.message).select_step_id_from_db()
        if step_id == 0:
            data = self.check_password()
            # return data
        elif step_id == 101:
            data = self.answer_after_updating_last_name()
            # return data
        elif step_id == 102:
            data = self.answer_after_updating_first_name()
        elif step_id == 103:
            data = self.answer_after_updating_patronymic()
        elif step_id == 104:
            data = self.answer_after_updating_birthdate()
        elif step_id == 105:
            data = self.answer_after_updating_belt()
        return data

    def check_password(self) -> AnswerMessage:
        password = SelectorDataDb(self.message).select_admin_password()
        try:
            if int(self.message.text) == password:
                CommandHandler('13001,', self.message)
                return self.create_standart_answer_to_msg()
            else:
                raise ValueError
        except ValueError:
            raise ValueError

    def choice_answer_to_not_named_inline_command(self, call) -> AnswerMessage:
        CommandHandler(call.data, call.message)
        step_id = SelectorDataDb(self.message).select_step_id_from_db()
        if step_id == 100:
            return self.answer_with_personal_list()
        elif step_id == 110:
            return self.answer_with_data_about_one_person()
        else:
            standart = StandartDataForAnswer(self.message)
            _id = standart.build_chat_id()
            _que = standart.build_question()
            _dia = standart.build_dialogs()
            _pre = standart.build_pre_answer()
            return AnswerMessage(_id, _que, _dia, _pre)

    def answer_with_data_about_one_person(self):
        one = AnswerDataAboutOnePerson(self.message)
        _id = one.build_chat_id()
        _que = one.build_question()
        _dia = one.build_dialogs()
        _pre = one.build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)

    def answer_with_personal_list(self) -> AnswerMessage:
        # standart = StandartDataForAnswer(self.message)
        _id = StandartDataForAnswer(self.message).build_chat_id()
        _que = StandartDataForAnswer(self.message).build_question()
        _dia = AnswerWithPersonList(self.message).build_dialogs()
        _pre = StandartDataForAnswer(self.message).build_pre_answer()
        return AnswerMessage(_id, _que, _dia, _pre)

    def create_answer_to_add_commands(self, call):
        CommandHandler('40000, 13101', call.message)
        return self.create_standart_answer_to_msg()

    def answer_after_updating_last_name(self):
        CommandHandler('41000, 13102', self.message)
        return self.create_standart_answer_to_msg()

    def answer_after_updating_first_name(self):
        CommandHandler('42000, 13103', self.message)
        return self.create_standart_answer_to_msg()

    def answer_after_updating_patronymic(self):
        CommandHandler('43000, 13104', self.message)
        return self.create_standart_answer_to_msg()

    def answer_after_updating_birthdate(self):
        CommandHandler('44000, 13105', self.message)
        return self.create_standart_answer_to_msg()

    def answer_after_updating_belt(self):
        CommandHandler('45000, 13100', self.message)
        return self.answer_with_personal_list()

    def answer_to_back_command(self):
        pre_step_id = SelectorDataDb(self.message).select_pre_question_id()
        CommandHandler(f"{13000 + pre_step_id},", self.message)
        if pre_step_id == 100:
            data = self.answer_with_personal_list()
        else:
            data = self.create_standart_answer_to_msg()
        return data



if __name__ == '__main__':
    test = Director()
    test_obj = test.create_testing_obj()
    print(test_obj._id.chat_id)
