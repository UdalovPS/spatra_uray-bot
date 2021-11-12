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
                if len(dialog) > 3:
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


if __name__ == '__main__':
    data = Dialogs()
    ins_data = data.zero_d
    DataInsector(*ins_data)
    pass