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
                                      'birthdate        varchar(50),' \
                                      'belt             varchar(50)'
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


class GroupsTable(DatabasePSQL):
    def __init__(self):
        super(GroupsTable, self).__init__()
        self.table_name = 'groups_table'
        self.fields_with_parameters = "id       SERIAL PRIMARY KEY, " \
                                      "name     varchar(255)"
        self.fields = 'id, name'
        self.split_fields = self.fields.split(', ')


class PersonalWithGroupTable(DatabasePSQL):
    def __init__(self):
        super(PersonalWithGroupTable, self).__init__()
        self.table_name = 'pers_group_table'
        self.fields_with_parameters = "group_id     INTEGER references groups_table(id) ON DELETE CASCADE, " \
                                      "person_id    INTEGER references person_table(id) ON DELETE CASCADE"
        self.fields = 'group_id, person_id'
        self.split_fields = self.fields.split(', ')


class PeriodTable(DatabasePSQL):
    def __init__(self):
        super(PeriodTable, self).__init__()
        self.table_name = 'period_table'
        self.fields_with_parameters = "id     SERIAL PRIMARY KEY, " \
                                      "name   varchar(30)"
        self.fields = 'id, name'
        self.split_fields = self.fields.split(', ')


class PayTable(DatabasePSQL):
    def __init__(self):
        super(PayTable, self).__init__()
        self.table_name = 'pay_table'
        self.fields_with_parameters = "person_id    INTEGER references person_table(id) ON DELETE CASCADE, " \
                                      "group_id     INTEGER references groups_table(id) ON DELETE CASCADE," \
                                      "period_id    INTEGER references period_table(id) ON DELETE CASCADE"
        self.fields = 'person_id, group_id, period_id'
        self.split_fields = self.fields.split(', ')

if __name__ == '__main__':
    db = PayTable()
    db.drop_table(db.table_name)
    db.create_table(db.table_name, db.fields_with_parameters)
    # print(sys.path)
    pass
