from Database.databases import *


class SelectorDataDb():
    def __init__(self, message):
        self.message = message

        self.admin = AdminTable()
        self.steps = StepTable()
        self.pers = PersonTable()
        self.belt = BeltsTable()
        self.quest = QuestionsTable()
        self.dia = DialogsTable()
        self.group = GroupsTable()
        self.pers_group = PersonalWithGroupTable()
        self.period = PeriodTable()
        self.pay = PayTable()

    def select_pay_people_in_one_group(self, group_id, period_id):
        conditions = f"{self.pay.split_fields[1]}={group_id} AND {self.pay.split_fields[2]}={period_id}"
        data = self.pay.select_in_table(self.pay.table_name,
                                        self.pay.split_fields[0],
                                        conditions)
        if data:
            return data
        else:
            return []

    def select_period_name(self):
        period_id = self.select_tmp_period_id()
        conditions = f"{self.period.split_fields[0]}={period_id}"
        data = self.period.select_in_table(self.period.table_name,
                                           self.period.split_fields[1],
                                           conditions)
        return data[0][0]

    def select_all_period(self):
        data = self.period.select_in_table(self.period.table_name,
                                          '*')
        return data


    def select_tmp_period_id(self):
        conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
        data = self.steps.select_in_table(self.steps.table_name,
                                          f"{self.steps.split_fields[4]}",
                                          conditions)
        return data[0][0]


    def select_last_period_id(self):
        data = self.period.select_in_table(self.period.table_name,
                                           f"MAX({self.pers.split_fields[0]})")
        return data[0][0]

    def select_admin_password(self):
        data = self.admin.select_in_table(self.admin.table_name,
                                          self.admin.fields)
        return data[0][0]


    def select_step_id_from_db(self):
        chat_id = self.message.chat.id
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        step_id = self.steps.select_in_table(self.steps.table_name,
                                             self.steps.split_fields[1],
                                             conditions
                                             )
        if step_id:
            return step_id[0][0]
        else:
            return None

    def select_question_from_db(self, step_id):
        conditions = f'{self.quest.split_fields[0]}={step_id}'
        data = self.quest.select_in_table(self.quest.table_name,
                                          f"{self.quest.split_fields[1]}",
                                          conditions)
        if data:
            return data[0][0]
        else:
            return None

    def select_dialog_from_db(self, step_id):
        conditions = f'{self.dia.split_fields[0]}={step_id}'
        data = self.dia.select_in_table(self.dia.table_name,
                                        f'{self.dia.split_fields[1]}, '
                                        f'{self.dia.split_fields[2]},'
                                        f'{self.dia.split_fields[3]}',
                                        conditions)
        if data:
            return data
        else:
            return None

    def select_last_personal_id(self):
        data = self.pers.select_in_table(self.pers.table_name,
                                         f"MAX({self.pers.split_fields[0]})")
        return data[0][0]


    def select_tmp_personal_id(self):
        conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
        data = self.steps.select_in_table(self.steps.table_name,
                                          f"{self.steps.split_fields[2]}",
                                          conditions)
        return data[0][0]

    def select_tmp_group_id(self):
        conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
        data = self.steps.select_in_table(self.steps.table_name,
                                          f"{self.steps.split_fields[3]}",
                                          conditions)
        return data[0][0]

    def select_data_about_all_persons(self):
        data = self.pers.select_in_table(self.pers.table_name,
                                         f"{self.pers.split_fields[0]},"
                                         f"{self.pers.split_fields[1]},"
                                         f"{self.pers.split_fields[2]}")
        return data

    def select_pre_question_id(self):
        step_id = self.select_step_id_from_db()
        conditions = f'{self.quest.split_fields[0]}={step_id}'
        data = self.quest.select_in_table(self.quest.table_name,
                                          f'{self.quest.split_fields[2]}',
                                          conditions)
        return data[0][0]

    def select_data_about_one_person(self, person_id):
        conditions = f"{self.pers.split_fields[0]}={person_id}"
        data = self.pers.select_in_table(self.pers.table_name,
                                         '*', conditions)
        return data[0]

    def select_last_group_id(self):
        data = self.group.select_in_table(self.group.table_name,
                                          f"MAX({self.group.split_fields[0]})")
        return data[0][0]

    def select_data_about_all_groups(self):
        data = self.group.select_in_table(self.group.table_name,
                                          '*')
        return data

    def select_groups_members(self, group_id):
        cmn_request = f"SELECT person_table.id, last_name, first_name " \
                      f"FROM groups_table JOIN person_table " \
                      f"ON person_table.id IN " \
                      f"(SELECT person_id FROM pers_group_table WHERE group_id = {group_id})" \
                      f"AND groups_table.id = {group_id}"
        data = self.pers.common_request_select(cmn_request)
        return data

    def select_not_groups_members(self, group_id):
        cmn_request = f"SELECT person_table.id, last_name, first_name " \
                      f"FROM groups_table JOIN person_table " \
                      f"ON person_table.id NOT IN " \
                      f"(SELECT person_id FROM pers_group_table WHERE group_id = {group_id})" \
                      f"AND groups_table.id = {group_id}"
        data = self.pers.common_request_select(cmn_request)
        return data

    def select_group_name(self, group_id):
        conditions = f"{self.group.split_fields[0]}={group_id}"
        data = self.group.select_in_table(self.group.table_name,
                                          self.group.split_fields[1],
                                          conditions)
        return data[0][0]

if __name__ == '__main__':
    data = SelectorDataDb('msg')
    data.select_groups_members(1)
