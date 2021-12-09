from Database.databases import *
from Database.data_selector import SelectorDataDb


class CommandHandler:
    def __init__(self, commands, message, sub_text=None) -> None:
        self.message = message
        self.sub_text = sub_text
        self.commands = commands.split(',')

        self.admin = AdminTable()
        self.steps = StepTable()
        self.pers = PersonTable()
        self.belt = BeltsTable()
        self.quest = QuestionsTable()
        self.dialog = DialogsTable()
        self.group = GroupsTable()
        self.pers_group = PersonalWithGroupTable()
        self.period = PeriodTable()
        self.pay = PayTable()


        self.command_parser()

    def command_parser(self) -> None:
        """
        Command handler algorithm:
        10 - is commands for work with <step_table>;
        10 000 + - delete fields from steps_table where chat_id = message.chat.id;
        11 000 + - insert zero step_id
        12 000 + - change tmp_personal_id;
        13 000 + - change step_id;
        14 000 + - change tmp_period_id;

        20 - is commands for work with <groups_table>;
        20 000 + - insert new row in groups_table;
        21 000 + - update group name in new group;
        22 000 + - update group_name;
        23 000 + - update tmp_group_id;
        24 000 + - add person in group;
        25 000 + - delete person in group;

        30 - is commands for work with <period_table> and <pay_table>;
        30 000 + - insert new row in pay_period_table;
        31 000 + - update period name;
        32 000 +  - update tmp_period_id after insert new row;
        33 000 + - delete period;
        34 000 + - insert new row in pay_table;
        35 000 + - delete  1 row in pay_table;

        40 - is commands for work with <personal_table>;
        40 000 + - insert new personal if not exists;
        41 000 + - update personal last_name;
        42 000 + - update personal first_name;
        43 000 + - update personal patronymic;
        44 000 + - update personal birthdate;
        45 000 + - update personal belt;
        """
        for command in self.commands:
            if command:
                int_cmd = int(command)
                cod = int_cmd // 1000
                value = int_cmd % 1000
                if cod == 10:
                    self.__delete_data_from_step_id(self.message.chat.id)
                if cod == 11:
                    self.__insert_zero_step_id(self.message.chat.id)
                if cod == 12:
                    self.__update_tmp_person_id(value)
                if cod == 13:
                    self.__change_step_id(value, self.message.chat.id)
                if cod == 14:
                    self.__update_tmp_period_id(self.message.chat.id, value)
                if cod == 20:
                    self.__insert_new_row_in_group_table()
                if cod == 21:
                    self.__update_tmp_group_id(SelectorDataDb(self.message).select_last_group_id(),
                                               self.message.chat.id)
                if cod == 22:
                    self.__update_group_name(SelectorDataDb(self.message).select_tmp_group_id(),
                                             self.message.text)
                if cod == 23:
                    self.__update_tmp_group_id(value, self.message.chat.id)
                if cod == 24:
                    self.__add_members_in_group(value, SelectorDataDb(self.message).select_tmp_group_id())
                if cod == 25:
                    self.__delete_members_in_group(value, SelectorDataDb(self.message).select_tmp_group_id())
                if cod == 26:
                    self.__delete_one_group(SelectorDataDb(self.message).select_tmp_group_id())
                if cod == 30:
                    self.__insert_new_row_in_period_table()
                if cod == 31:
                    self.__update_period_name(SelectorDataDb(self.message).select_tmp_period_id(),
                                              self.message.text)
                if cod == 32:
                    self.__update_tmp_period_id(self.message.chat.id,
                                                SelectorDataDb(self.message).select_last_period_id())
                if cod == 33:
                    self.__delete_period(SelectorDataDb(self.message).select_tmp_period_id())
                if cod == 34:
                    self.__insert_new_row_in_pay_table(value)
                if cod == 35:
                    self.__delete_one_row_in_pay_table(value)
                if cod == 40:
                    self.__insert_new_customer()
                if cod == 41:
                    self.__update_personal_last_name(SelectorDataDb(self.message).select_tmp_personal_id(),
                                                     self.message.text)
                if cod == 42:
                    self.__update_personal_first_name(SelectorDataDb(self.message).select_tmp_personal_id(),
                                                      self.message.text)
                if cod == 43:
                    self.__update_personal_patronymic(SelectorDataDb(self.message).select_tmp_personal_id(),
                                                      self.message.text)
                if cod == 44:
                    self.__update_personal_birthdate(SelectorDataDb(self.message).select_tmp_personal_id(),
                                                     self.message.text)
                if cod == 45:
                    self.__update_personal_belt(SelectorDataDb(self.message).select_tmp_personal_id(),
                                                self.message.text)
                if cod == 46:
                    self.__delete_data_about_one_person(SelectorDataDb(self.message).select_tmp_personal_id())

    def __delete_one_row_in_pay_table(self, person_id):
        db = SelectorDataDb(self.message)
        group_id = db.select_tmp_group_id()
        period_id = db.select_tmp_period_id()
        conditions = f"{self.pay.split_fields[0]}={person_id} " \
                     f"AND {self.pay.split_fields[1]}={group_id}" \
                     f"AND {self.pay.split_fields[2]}={period_id}"
        self.pay.delete_data_from_table(self.pay.table_name,
                                        conditions)

    def __insert_new_row_in_pay_table(self, person_id):
        db = SelectorDataDb(self.message)
        group_id = db.select_tmp_group_id()
        period_id = db.select_tmp_period_id()
        self.pay.insert_data_in_table(self.pay.table_name,
                                      f"{self.pay.fields}",
                                      f"({person_id}, {group_id}, {period_id})")


    def __delete_data_from_step_id(self, chat_id) -> None:
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name, conditions)

    def __insert_zero_step_id(self, chat_id) -> None:
        self.steps.insert_data_in_table(self.steps.table_name,
                                        f"{self.steps.split_fields[0]},"
                                        f"{self.steps.split_fields[1]}",
                                        f'({chat_id},0)'
                                        )

    def __change_step_id(self, value, chat_id) -> None:
        field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __add_members_in_group(self, person_id, group_id) -> None:
        self.pers_group.insert_data_in_table(self.pers_group.table_name,
                                             f"{self.pers_group.fields}",
                                             f"({group_id}, {person_id})")

    def __delete_members_in_group(self, person_id, group_id) -> None:
        conditions = f"{self.pers_group.split_fields[0]}={group_id} AND {self.pers_group.split_fields[1]}={person_id}"
        self.pers_group.delete_data_from_table(self.pers_group.table_name,
                                               conditions)

    def __delete_one_group(self, group_id) -> None:
        conditions = f"{self.group.split_fields[0]}={group_id}"
        self.group.delete_data_from_table(self.group.table_name,
                                          conditions)

    def __insert_new_row_in_period_table(self) -> None:
        self.period.insert_data_in_table(self.period.table_name,
                                         self.period.split_fields[1],
                                         f"('new period')")

    def __insert_new_row_in_group_table(self) -> None:
        self.group.insert_data_in_table(self.group.table_name,
                                        self.group.split_fields[1],
                                        f"('new group')")

    def __update_tmp_group_id(self, group_id, chat_id):
        field_value = f"{self.steps.split_fields[3]}={group_id}"
        conditions = f"{self.steps.split_fields[0]}={chat_id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __update_group_name(self, group_id, value) -> None:
        field_value = f"{self.group.split_fields[1]}='{value}'"
        conditions = f"{self.group.split_fields[0]}={group_id}"
        self.group.update_fields(self.group.table_name,
                                 field_value, conditions)

    def __update_tmp_period_id(self, chat_id, period_id) -> None:
        field_value = f"{self.steps.split_fields[4]}={period_id}"
        conditions = f"{self.steps.split_fields[0]}={chat_id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __insert_new_customer(self) -> None:
        self.pers.insert_data_in_table(self.pers.table_name,
                                       f"{self.pers.split_fields[1]}",
                                       f"('New student')"
                                       )
        self.__update_tmp_person_id(SelectorDataDb(self.message).select_last_personal_id())

    def __update_tmp_person_id(self, persond_id):
        field_value = f"{self.steps.split_fields[2]}={persond_id}"
        conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __update_personal_last_name(self, person_id, value) -> None:
        conditions = f'{self.pers.split_fields[0]}={person_id}'
        field_value = f"{self.pers.split_fields[1]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __delete_data_about_one_person(self, person_id):
        conditions = f'{self.pers.split_fields[0]}={person_id}'
        self.pers.delete_data_from_table(self.pers.table_name,
                                         conditions)

    def __update_personal_first_name(self, personal_id, value) -> None:
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[2]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_patronymic(self, personal_id, value) -> None:
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[3]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_birthdate(self, personal_id, value) -> None:
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[4]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_belt(self, personal_id, value) -> None:
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[5]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_period_name(self, period_id, value) -> None:
        conditions = f"{self.period.split_fields[0]}={period_id}"
        fields_value = f"{self.period.split_fields[1]}='{value}'"
        self.period.update_fields(self.period.table_name,
                                  fields_value, conditions)

    def __delete_period(self, period_id) -> None:
        conditions = f"{self.period.split_fields[0]}={period_id}"
        self.period.delete_data_from_table(self.period.table_name,
                                           conditions)

