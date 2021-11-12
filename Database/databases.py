from Database.posgre_sql import DatabasePSQL


class AdminTable(DatabasePSQL):
    def __init__(self):
        super(AdminTable, self).__init__()
        self.table_name = 'admin_table'
        self.fields_with_parameters = 'password INTEGER'
        self.fields = "password"


class StepTable(DatabasePSQL):
    def __init__(self):
        super(StepTable, self).__init__()
        self.table_name = 'step_table'
        self.fields_with_parameters = 'chat_id          INTEGER PRIMARY KEY,' \
                                      'step_id          INTEGER,' \
                                      'tmp_person_id    INTEGER,' \
                                      'tmp_group_id     INTEGER,' \
                                      'tmp_period_id    INTEGER'
        self.fields = "chat_id, step_id, tmp_person_id, tmp_group_id, tmp_period_id"
        self.split_fields = self.fields.split(', ')


class PersonTable(DatabasePSQL):
    def __init__(self):
        super(PersonTable, self).__init__()
        self.table_name = 'person_table'
        self.fields_with_parameters = 'id               SERIAL PRIMARY KEY,' \
                                      'last_name        varchar(50),' \
                                      'first_name       varchar(50),' \
                                      'patronymic       varchar(50),' \
                                      'birthdate        DATE,' \
                                      'belt             INTEGER'
        self.fields = "id, last_name, first_name, patronymic, birthdate, belt"
        self.split_fields = self.fields.split(', ')


class BeltsTable(DatabasePSQL):
    def __init__(self):
        super(BeltsTable, self).__init__()
        self.table_name = 'belts_table'
        self.fields_with_parameters = 'id   INTEGER PRIMARY KEY,' \
                                      'name varchar(50)'
        self.fields = "id, belt"
        self.split_fields = self.fields.split(', ')


class QuestionsTable(DatabasePSQL):
    def __init__(self):
        super(QuestionsTable, self).__init__()
        self.table_name = 'questions_table'
        self.fields_with_parameters = 'step_id      INTEGER,' \
                                      'question     varchar(255),' \
                                      'pre_step_id  INTEGER'
        self.fields = 'step_id, question, pre_step_id'
        self.split_fields = self.fields.split(', ')


class DialogsTable(DatabasePSQL):
    def __init__(self):
        super(DialogsTable, self).__init__()
        self.table_name = 'dialogs_table'
        self.fields_with_parameters = "step_id      INTEGER, " \
                                      "dialog       varchar(255)," \
                                      "commands     varchar(50)," \
                                      "emoji        varchar(100)"
        self.fields = 'step_id, dialog, commands, emoji'
        self.split_fields = self.fields.split(', ')


if __name__ == '__main__':
    # db = DialogsTable()
    # db.drop_table(db.table_name)
    # db.create_table(db.table_name, db.fields_with_parameters)
    # print(sys.path)
    pass
