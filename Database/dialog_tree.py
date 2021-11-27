from databases import QuestionsTable, DialogsTable

class DialogTree():
    def __init__(self):
        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()

    def insert_question_in_db(self, step_id, question, pre_step_id):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{step_id, question, pre_step_id}')


    def insert_dialog(self, step, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          f'{self.dialogs.split_fields[0]},'
                                          f'{self.dialogs.split_fields[1]},'
                                          f'{self.dialogs.split_fields[2]},'
                                          f'{self.dialogs.split_fields[3]}',
                                          f"({step}, '{dialog[0]}', "
                                          f"'{dialog[1]}')")

    def insert_dialogs_with_emoji(self, step, dialog):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                      self.dialogs.fields,
                                      f"({step}, '{dialog[0]}',"
                                      f"'{dialog[1]}', '{dialog[2]}')")


class DataInsector:
    def __init__(self, step_id=None, question=None, pre_step_id=None,
                 dialog_list=None):
        self.step_id = step_id
        self.question = question
        self.pre_step_id = pre_step_id
        self.dialog_list = dialog_list

        self.questions = QuestionsTable()
        self.dialogs = DialogsTable()
        self.insert_question_and_dialogs()

    def insert_question_and_dialogs(self):
        self.delete_data()
        if self.question != None:
            self.insert_question_in_db()
        if self.dialog_list != None:
            for dialog in self.dialog_list:
                if len(dialog) > 2:
                    self.insert_dialogs_with_emoji(*dialog)
                else:
                    self.insert_dialog(*dialog)

    def delete_data(self):
        conditions = f"step_id = {self.step_id}"
        self.questions.delete_data_from_table(self.questions.table_name,
                                              conditions)
        self.dialogs.delete_data_from_table(self.dialogs.table_name,
                                            conditions)

    def insert_question_in_db(self):
        self.questions.insert_data_in_table(self.questions.table_name,
                                            self.questions.fields,
                                            f'{self.step_id, self.question, self.pre_step_id}')

    def insert_dialog(self, dialog, commands):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                          f'{self.dialogs.split_fields[0]},'
                                          f'{self.dialogs.split_fields[1]},'
                                          f'{self.dialogs.split_fields[2]}',
                                          f"({self.step_id}, '{dialog}', '{commands}')")

    def insert_dialogs_with_emoji(self, dialog, commands, emoji):
        self.dialogs.insert_data_in_table(self.dialogs.table_name,
                                      self.dialogs.fields,
                                      f"({self.step_id}, '{dialog}',"
                                      f"'{commands}', '{emoji}')")


class Dialogs:
    def __init__(self):
        super(Dialogs, self).__init__()
        """(step, question, previous step_id) 
            (dialog, commands, emoji IF EXISTS)"""

        self.zero_d = (0, 'Введите код доступа', 0)
        self.main_menu = (1, 'Выберите команду', 0,
                          (('Список учеников', '13100,', '\U0001F44A'),
                           ('Управление группами', '13200,', '\U0001F4CB'),
                           ('Управление оплатой', '13300,', '\U0001F4B5'))
                          )
        self.all_persons_step = (100, 'Выберите ученика', 1,
                                 (('Добавить ученика', 'add', '\U00002795'),)
                                 )
        self.person_last_name = (101, 'Введите фамилию ученика', 100,
                                 (('Не изменять. Далее', '13102,', '\U000023E9'),)
                                 )
        self.person_first_name = (102, 'Введите имя ученика', 101,
                                  (('Не изменять. Далее', '13103,', '\U000023E9'),)
                                  )
        self.person_patronymic = (103, 'Введите отчество ученика', 102,
                                  (('Не изменять. Далее', '13104,', '\U000023E9'),)
                                  )
        self.person_birthdate = (104, 'Введите дату рождения', 103,
                                 (('Не изменять. Далее', '13105,', '\U000023E9'),)
                                 )
        self.choice_belt = (105, 'Введите пояс ученика', 104,
                            (('Не изменять. Далее', '13100,', '\U000023E9'),)
                            )
        self.one_person = (110, '-', 100,
                           (('Удалить данный по ученику', '13100, 46000', '\U0000274C'),
                            ('Изменить данные по ученику', '13101,', '\U0001F4AC'))
                           )
        self.all_groups = (200, 'Выберите группу', 1,
                           (('Создать новую группу', '13201, 20000, 21000', '\U00002795'),)
                           )
        self.update_group_name = (201, 'Введите имя группы', 200)
        self.data_about_one_group = (202, '-', 200,
                                     (('Добавить учеников в группу', '13203,', '\U0000270F'),
                                      ('Удалить учеников из группу', '13204,', '\U00002796'),
                                      ('Изменить имя группы', '13201', '\U000027B0'),
                                      ('Удалить группу', '13200, 26000', '\U0000274C'))
                                     )
        self.add_person_in_group = (203, 'Выберите нужных учеников', 202)
        self.del_person_in_group = (204, 'Выберите нужных учеников которых нужно удалить из группы', 202)

if __name__ == '__main__':
    data = Dialogs()
    ins_data = data.data_about_one_group
    DataInsector(*ins_data)
    pass
