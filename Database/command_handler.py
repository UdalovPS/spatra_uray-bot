from datetime import date, datetime
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


        self.command_parser()

    def command_parser(self) -> None:
        """
        Command handler algorithm:
        10 - is commands for work with <step_table>;
        10 000 + - delete fields from steps_table where chat_id = message.chat.id;
        11 000 + - insert zero step_id
        12 000 + - change tmp_personal_id;
        13 000 + - change step_id;
        14 000 - change tmp_group_id;
        15 000 - update sticker_id in step_table;
        16 000 - delete sticker_id from step_table;

        20 - is commands for work with <groups_table>;
        20 000 + - insert new row in groups_table;
        21 000 + - update group name in new group;
        22 000 + - update group_name;
        23 000 + - update group_name after choice group;
        24 000 + - add person in group;
        25 000 + - delete person in group;

        30 - is commands for work with <cart_table> and <date_time_place_table>;
        30 000 - insert new row in cart_table;
        31 000 - insert new row in date_time_place_table;
        32 000 - update delivery mod;
        33 000 - update delivery address;
        34 000 - update customer time;
        35 000 - update price_before_scores in cart_table;
        36 000 - add delivery price to price_before_scores;
        37 000 - update final price in cart_table;
        38 000 - update cart_status in cart_table;
        39 000 - update message_id in cart_table;

        40 - is commands for work with <personal_table>;
        40 000 + - insert new personal if not exists;
        41 000 + - update personal last_name;
        42 000 + - update personal first_name;
        43 000 + - update personal patronymic;
        44 000 + - update personal birthdate;
        45 000 + - update personal belt;

        50 - is commands for work with <scores_table> and <tmp_scores_table>
        50 000 - insert new row in scores_table;
        51 000 - realise scores;
        52 000 - insert new row in tmp_scores_table;

        60 - is commands for work with status of carts;
        60 000 - insert new row in tmp_cart_customer_table;
        61 000 - update cart_status;

        90 - is commands for work with administrator;
        90 000 - update tmp_cart_id;
        91 000 - update cart_status from administrator menu;
        92 000 - converte tmp_scores in scores;
        93 000 - update tmp_user_id;
        94 000 - change black_list_status;
        95 000 - change personal discount;
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
                # if cod == 14:
                #     self.__update_tmp_group_id(value)
                # if cod == 15:
                #     self.__update_sticker_id_in_step_table(self.chat_id)
                # if cod == 16:
                #     self.__delete_sticker_id_from_step_table(self.chat_id)
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
                # if cod == 30:
                #     self.__insert_start_cart_data(self.chat_id)
                # if cod == 31:
                #     self.__insert_new_date_time_place_row(self.chat_id)
                # if cod == 32:
                #     self.__update_delivery_mode(self.chat_id, value)
                # if cod == 33:
                #     self.__update_delivery_address(self.chat_id)
                # if cod == 34:
                #     self.__update_customer_time(self.chat_id)
                # if cod == 35:
                #     self.__update_price_before_scores(self.chat_id)
                # if cod == 36:
                #     self.__add_delivery_price(self.chat_id, self.sub_text)
                # if cod == 37:
                #     self.__update_final_price(self.chat_id, SelectorDataDb(self.message).select_price_before_scores())
                # if cod == 38:
                #     self.__update_cart_status(self.__select_max_cart_id(self.chat_id), value)
                # if cod == 39:
                #     self.__update_message_id_in_step_table(self.chat_id)
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
                # if cod == 50:
                #     self.__insert_new_row_in_scores_table(self.chat_id)
                # if cod == 51:
                #     self.__realise_scores_for_cart(self.chat_id)
                # if cod == 52:
                #     self.__insert_new_row_in_tmp_scores_table(self.chat_id)
                # if cod == 60:
                #     self.__add_new_row_in_tmp_customer_cart_table(self.chat_id, self.message_text)
                # if cod == 61:
                #     self.__update_cart_status(self.sub_text, value)
                # if cod == 90:
                #     self.__update_tmp_cart_id(self.message_text)
                # if cod == 91:
                #     self.__update_cart_status(SelectorDataDb(self.message).select_tmp_cart_id_from_admin_table(), value)
                # if cod == 92:
                #     self.__converte_tmp_scores_in_scores(SelectorDataDb(self.message).select_tmp_cart_id_from_admin_table())
                # if cod == 93:
                #     self.__update_tmp_user_id(self.message_text)
                # if cod == 94:
                #     self.__update_black_list_status(SelectorDataDb(self.message).select_tmp_customer_id(), value)
                # if cod == 95:
                #     self.__update_personal_discount(self.sub_text[0], self.sub_text[1])

    def __delete_data_from_step_id(self, chat_id) -> None:
        """+"""
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.delete_data_from_table(self.steps.table_name, conditions)

    def __insert_zero_step_id(self, chat_id) -> None:
        """+"""
        self.steps.insert_data_in_table(self.steps.table_name,
                                        f"{self.steps.split_fields[0]},"
                                        f"{self.steps.split_fields[1]}",
                                        f'({chat_id},0)'
                                        )

    def __change_style_id(self, value, chat_id) -> None:
        field_value = f'{self.steps.split_fields[2]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __change_step_id(self, value, chat_id) -> None:
        """+"""
        field_value = f'{self.steps.split_fields[1]}={value}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    # def __update_tmp_group_id(self, value) -> None:
    #     """+"""
    #     conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
    #     field_value = f"{self.steps.split_fields[3]}={value}"
    #     self.steps.update_fields(self.steps.table_name,
    #                              field_value, conditions)

    def __add_members_in_group(self, person_id, group_id) -> None:
        """+"""
        self.pers_group.insert_data_in_table(self.pers_group.table_name,
                                             f"{self.pers_group.fields}",
                                             f"({group_id}, {person_id})")

    def __delete_members_in_group(self, person_id, group_id) -> None:
        """+"""
        conditions = f"{self.pers_group.split_fields[0]}={group_id} AND {self.pers_group.split_fields[1]}={person_id}"
        self.pers_group.delete_data_from_table(self.pers_group.table_name,
                                               conditions)

    def __delete_one_group(self, group_id) -> None:
        """+"""
        conditions = f"{self.group.split_fields[0]}={group_id}"
        self.group.delete_data_from_table(self.group.table_name,
                                          conditions)

    def __insert_start_cart_data(self, chat_id) -> None:
        self.cart.insert_data_in_table(self.cart.table_name,
                                       f'{self.cart.split_fields[1]},'
                                       f'{self.cart.split_fields[2]}',
                                       f'({chat_id},0)'
                                       )

    def __update_sticker_id_in_step_table(self, chat_id) -> None:
        field_value = f'{self.steps.split_fields[3]}={self.message_id}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __delete_sticker_id_from_step_table(self, chat_id) -> None:
        field_value = f'{self.steps.split_fields[3]}={0}'
        conditions = f'{self.steps.split_fields[0]}={chat_id}'
        self.steps.update_fields(self.steps.table_name, field_value,
                                 conditions
                                 )

    def __select_max_cart_id(self, chat_id) -> None:
        conditions = f'{self.cart.split_fields[1]}={chat_id}'
        data = self.cart.select_in_table(self.cart.table_name,
                                         f'MAX({self.cart.split_fields[0]})',
                                         conditions)
        return data[0][0]

    def __insert_new_row_in_group_table(self) -> None:
        """+"""
        self.group.insert_data_in_table(self.group.table_name,
                                        self.group.split_fields[1],
                                        f"('new group')")

    def __update_tmp_group_id(self, group_id, chat_id):
        """+"""
        field_value = f"{self.steps.split_fields[3]}={group_id}"
        conditions = f"{self.steps.split_fields[0]}={chat_id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __update_group_name(self, group_id, value) -> None:
        """+"""
        field_value = f"{self.group.split_fields[1]}='{value}'"
        conditions = f"{self.group.split_fields[0]}={group_id}"
        self.group.update_fields(self.group.table_name,
                                 field_value, conditions)

    def __update_product_count_in_cart_table(self, chat_id, value) -> None:
        cart_product_id = self.select_last_cart_product_id(chat_id)
        conditions = f'{self.cart_prod.split_fields[0]}={cart_product_id}'
        field_value = f"{self.cart_prod.split_fields[3]}={value}," \
                      f"{self.cart_prod.split_fields[5]}=1"
        self.cart_prod.update_fields(self.cart_prod.table_name,
                                     field_value, conditions
                                     )

    def __insert_new_customer(self) -> None:
        """+"""
        self.pers.insert_data_in_table(self.pers.table_name,
                                       f"{self.pers.split_fields[1]}",
                                       f"('New student')"
                                       )
        self.__update_tmp_person_id(SelectorDataDb(self.message).select_last_personal_id())

    def __update_tmp_person_id(self, persond_id):
        """+"""
        field_value = f"{self.steps.split_fields[2]}={persond_id}"
        conditions = f"{self.steps.split_fields[0]}={self.message.chat.id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __update_personal_last_name(self, person_id, value) -> None:
        """+"""
        conditions = f'{self.pers.split_fields[0]}={person_id}'
        field_value = f"{self.pers.split_fields[1]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __delete_data_about_one_person(self, person_id):
        """+"""
        conditions = f'{self.pers.split_fields[0]}={person_id}'
        self.pers.delete_data_from_table(self.pers.table_name,
                                         conditions)

    def __update_personal_first_name(self, personal_id, value) -> None:
        """+"""
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[2]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_patronymic(self, personal_id, value) -> None:
        """+"""
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[3]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_birthdate(self, personal_id, value) -> None:
        """+"""
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[4]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_personal_belt(self, personal_id, value) -> None:
        """+"""
        conditions = f'{self.pers.split_fields[0]}={personal_id}'
        field_value = f"{self.pers.split_fields[5]}='{value}'"
        self.pers.update_fields(self.pers.table_name,
                                field_value, conditions)

    def __update_delivery_mode(self, chat_id, value) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        date_now = date.today()
        time_now = datetime.now().time()
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[1]}='{date_now}'," \
                      f"{self.date_place.split_fields[2]}='{time_now}'," \
                      f"{self.date_place.split_fields[3]}={value}"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)

    def __insert_new_date_time_place_row(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        self.cart.insert_data_in_table(self.date_place.table_name,
                                       f'{self.date_place.split_fields[0]}',
                                       f'({cart_id})'
                                       )

    def __update_price_before_scores(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        money_sum = 0
        list_data = SelectorDataDb(self.message).select_intermediate_data_about_cart()
        for item in list_data:
            money_sum += item[3]
        field_value = f"{self.cart.split_fields[3]}={money_sum}"
        conditions = f"{self.cart.split_fields[0]}={cart_id}"
        self.cart.update_fields(self.cart.table_name,
                                field_value, conditions)

    def __add_delivery_price(self, chat_id, value) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        field_value = f"{self.cart.split_fields[3]}={value}"
        conditions = f"{self.cart.split_fields[0]}={cart_id}"
        self.cart.update_fields(self.cart.table_name,
                                field_value, conditions)

    def __update_delivery_address(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[4]}='{self.message_text}'"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)

    def __update_customer_time(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        conditions = f'{self.date_place.split_fields[0]}={cart_id}'
        field_value = f"{self.date_place.split_fields[5]}='{self.message_text}'"
        self.date_place.update_fields(self.date_place.table_name,
                                      field_value, conditions)


    def __update_final_price(self, chat_id, value) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        conditions = f'{self.cart.split_fields[0]}={cart_id}'
        field_value = f"{self.cart.split_fields[4]}={value}"
        self.cart.update_fields(self.cart.table_name,
                                field_value, conditions)

    def __realise_scores_for_cart(self, chat_id) -> None:
        scores = SelectorDataDb(self.message).select_personal_scores(chat_id)
        price_before_scores = SelectorDataDb(self.message).select_price_before_scores()
        if scores > price_before_scores:
            self.__update_final_price(chat_id, 0)
            self.__update_scores(chat_id, scores - price_before_scores)
        else:
            self.__update_scores(chat_id, 0)
            self.__update_final_price(chat_id, price_before_scores - scores)

    def __insert_new_row_in_scores_table(self, chat_id) -> None:
        self.scores.insert_data_in_table(self.scores.table_name,
                                         self.scores.fields,
                                         f"({chat_id},0,10)")

    def __update_scores(self, chat_id, value) -> None:
        conditions = f"{self.scores.split_fields[0]}={chat_id}"
        field_value = f"{self.scores.split_fields[1]}={value}"
        self.scores.update_fields(self.scores.table_name,
                                  field_value, conditions)

    def __update_cart_status(self, cart_id, value) -> None:
        conditions = f'{self.cart.split_fields[0]}={cart_id}'
        field_value = f"{self.cart.split_fields[2]}={value}"
        self.cart.update_fields(self.cart.table_name,
                                field_value, conditions)

    def __insert_new_row_in_tmp_scores_table(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        db = SelectorDataDb(self.message)
        percent = db.select_scores_percent(chat_id)
        tmp_price = db.select_price_before_scores()
        value = percent * tmp_price / 100
        self.tmp_sc.insert_data_in_table(self.tmp_sc.table_name,
                                         self.tmp_sc.fields,
                                         f"({chat_id},{value},{cart_id})")

    def __update_message_id_in_step_table(self, chat_id) -> None:
        field_value = f"{self.steps.split_fields[4]}={self.message_id}"
        conditions = f"{self.steps.split_fields[0]}={chat_id}"
        self.steps.update_fields(self.steps.table_name,
                                 field_value, conditions)

    def __delete_garbage_from_db(self, chat_id) -> None:
        cart_id = self.__select_max_cart_id(chat_id)
        cart_conditions = f'{self.cart.split_fields[2]}=0 AND {self.cart.split_fields[1]}={chat_id}'
        cart_prod_conditions = f'{self.cart_prod.split_fields[1]}={cart_id} AND {self.cart_prod.split_fields[5]}=0'
        self.cart_prod.delete_data_from_table(self.cart_prod.table_name, cart_prod_conditions)
        self.cart.delete_data_from_table(self.cart.table_name, cart_conditions)

    def __add_new_row_in_tmp_customer_cart_table(self, chat_id, cart_id) -> None:
        conditions = f"{self.tmp_cart.split_fields[0]}={chat_id}"
        self.tmp_cart.delete_data_from_table(self.tmp_cart.table_name,
                                             conditions)
        self.tmp_cart.insert_data_in_table(self.tmp_cart.table_name,
                                           self.tmp_cart.fields,
                                           f"({chat_id}, {cart_id})")

    def __update_tmp_cart_id(self, new_cart_id) -> None:
        field_value = f"{self.admin.split_fields[1]}={new_cart_id}"
        self.admin.update_fields(self.admin.table_name, field_value)

    def __converte_tmp_scores_in_scores(self, cart_id) -> None:
        db = SelectorDataDb(self.message)
        chat_id_value = db.select_tmp_scores_and_chat_id(cart_id)
        chat_id = chat_id_value[0]
        tmp_scores = chat_id_value[1]
        personal_scores = db.select_personal_scores(chat_id)
        conditions = f"{self.scores.split_fields[0]}={chat_id}"
        field_value = f"{self.scores.split_fields[1]}={personal_scores + tmp_scores}"
        self.scores.update_fields(self.scores.table_name,
                                  field_value, conditions)

    def __update_tmp_user_id(self, user_id) -> None:
        field_value = f"{self.admin.split_fields[2]}={user_id}"
        self.admin.update_fields(self.admin.table_name,
                                 field_value)

    def __update_black_list_status(self, user_id, value) -> None:
        field_value = f"{self.customer.split_fields[3]}={value}"
        conditions = f"{self.customer.split_fields[0]}={user_id}"
        self.customer.update_fields(self.customer.table_name,
                                    field_value, conditions)

    def __update_personal_discount(self, user_id, value) -> None:
        field_value = f"{self.scores.split_fields[2]}={value}"
        conditions = f"{self.scores.split_fields[0]}={user_id}"
        self.scores.update_fields(self.scores.table_name,
                                  field_value, conditions)
