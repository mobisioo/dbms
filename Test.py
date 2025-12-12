import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable
exitt_code = 0
while exitt_code == 0:
    
    def list_columns(table_name):
        try:
            table_row_names=[]
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()


            for column in columns:

                #print(column[1]) 
                table_row_names.append(column[1])

            return table_row_names
        except sqlite3.Error as e:
            print("Error retrieving columns:", e)

        finally:
            if con:
                con.close()

    def count_columns(table_name):
        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()
            column_count = len(columns)
            return column_count

        except sqlite3.Error as e:
            print("Error retrieving column count:", e)

        finally:
            if con:
                con.close()



    def create_table():
        print("_________________________________________")
        print("\nCreate Database Table\n")
        table_name = input("[Enter table's name]: ")
        col_number = int(input("[Number of columns]: "))
        columns = []

        for i in range(col_number):
            print("_________________________________________")
            col_name = input(f"[Enter Column {i + 1}'s name]: ")
            print("\n1: Integer \n2: Text \n3: Boolean")
            user_input = input(f"[Enter Column {i + 1}'s data type (1, 2, or 3)]: ")

            col_type_number = int(user_input)
            if col_type_number == 1:
                col_type = "INTEGER"
            elif col_type_number == 2:
                col_type = "TEXT"
            elif col_type_number == 3:
                col_type = "BOOLEAN"
            else:
                print("Invalid type, setting to TEXT by default.")
                col_type = "TEXT"


            columns.append(f"{col_name} {col_type}")

        columns_string = ", ".join(columns)
        create_table_query = f"CREATE TABLE {table_name} ({columns_string});"
        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(create_table_query)
            con.commit()
            print("_________________________________________")
            print("\nTable Created Successfully!")
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()



    def list_tables():
        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            print("_________________________________________")
            print("\nTables in the database:")
            for index, table in enumerate(tables, start=1): 
                print(f"{index}. {table[0]}")

        except sqlite3.Error as e:
            print("Error retrieving tables:", e)

        finally:
            if con:
                con.close()
    def list_tables_v():
        try:
            values = []
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()

            
            for table in tables: 
                values.append(table[0])
            return values
        except sqlite3.Error as e:
            print("Error retrieving tables:", e)

        finally:
            if con:
                con.close()


    def insert_row():
        list_tables()
        values = list_tables_v()
        table_id_in = int(input("\n[Enter table's id]: "))
        table_id_in = table_id_in - 1
        table_name_in = values[table_id_in]
        table_row_count = count_columns(table_name_in)
        table_row_names = list_columns(table_name_in)

        table_row_values = []
        for i in range(table_row_count):
            value = input(f"\n[Enter value of '{table_row_names[i]}' row]: ")
            table_row_values.append(value)

        placeholders = ', '.join(['?'] * table_row_count)
        columns_string = ', '.join(table_row_names)

        insert_query = f"INSERT INTO {table_name_in} ({columns_string}) VALUES ({placeholders});"

        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(insert_query, table_row_values)
            con.commit()
            print("_________________________________________")
            print("\nData inserted successfully.")
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

    def select_rows():
        list_tables()
        values = list_tables_v()
        table_id_in = int(input("\n[Enter table's id]: "))
        table_id_in = table_id_in - 1
        table_name_in = values[table_id_in]

        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {table_name_in};")
            rows = cur.fetchall()

            
            columns = [description[0] for description in cur.description]

            
            table = PrettyTable(columns)
            for row in rows:
                table.add_row(row)

            print(table)

        except Error as e:
            print(f"Error retrieving data: {e}")

        finally:
            if con:
                con.close()

    def drop_table():
        

        list_tables()
        values = list_tables_v()
        table_id_in = int(input("\n[Enter table's id]: "))
        table_id_in = table_id_in - 1
        table_name_in = values[table_id_in]

        sure = input(f"\nAre you sure yo want to drop '{table_name_in}' table? (y/n): ")
        if sure == "y":
            try:
                con = sqlite3.connect('my.db')
                cur = con.cursor()
                cur.execute(f"DROP TABLE IF EXISTS {table_name_in};")
                con.commit()
                print("_________________________________________")
                print("\nTable Dropped successfully.")
            except Error as e:
                print(e)
            finally:
                if con:
                    con.close()
        else :
            print("Table deletion cancelled.")
    
    def delete_row():
        list_tables()
        values = list_tables_v()
        table_id_in = int(input("\n[Enter table's id]: "))
        table_id_in = table_id_in - 1
        table_name_in = values[table_id_in]
        table_row_names = list_columns(table_name_in)
        for index, rows in enumerate(table_row_names, start=1): 
                print(f"{index}. {rows}")
        filter_option_in = int(input("\nSelect Filter Column: "))
        filter_option_in = filter_option_in -1
        filter_option = table_row_names[filter_option_in]
        print(f"\nFiltering On '{filter_option}'...")
        filter_value = int(input("\nEnter Filter Value: "))
        try:
            con = sqlite3.connect('my.db')
            cur = con.cursor()
            cur.execute(f"DELETE FROM {table_name_in} WHERE {filter_option} = ?;", (filter_value,))
            con.commit()

            if cur.rowcount > 0:
                print(f"Row With '{filter_option}' Filter Context And '{filter_value}' Value Delete from '{table_name_in}' Table")
            else:
                print(f"There is not any rows with '{filter_option}' Filter Context And '{filter_value}' Value Delete in '{table_name_in}' Table")

        except Error as e:
            print(f"Error deleting row: {e}")

        finally:
            if con:
                con.close()
    #insert_row()


    #select_rows()
    #create_table()


    print("\nDatabase Management System")
    print("\n1. Create Table \n2. Enter Data\n3. Drop Table\n4. View Data\n5. Delete Rows\n6. Exit\n")
    option_choice = int(input("[Select Option]: "))
    while option_choice == 1:
        exit_code = 0
        while exit_code == 0:
            create_table()
            print("_________________________________________")
            print("\n1. Back To Menu\n2. Create Another Table\n")
            ch = int(input("[Select Option]: "))
            if ch == 1:
                exit_code = 1
            else: 
                exit_code = 0
        break
    while option_choice == 2:
        
        exit_code = 0
        while exit_code == 0:
            
            insert_row()
            print("_________________________________________")
            print("\n1. Back To Menu\n2. Add More Data\n")
            ch = int(input("[Select Option]: "))
            if ch == 1:
                exit_code = 1
            else: 
                exit_code = 0
        break
    while option_choice == 3:
        
        exit_code = 0
        while exit_code == 0:
            
            drop_table()
            print("_________________________________________")
            print("\n1. Back To Menu\n2. Drop Another Table\n")
            ch = int(input("[Select Option]: "))
            if ch == 1:
                exit_code = 1
            else: 
                exit_code = 0
        break
    while option_choice == 4:
        
        exit_code = 0
        while exit_code == 0:
            
            select_rows()
            print("_________________________________________")
            print("\n1. Back To Menu\n2. Select Another Table\n")
            ch = int(input("[Select Option]: "))
            if ch == 1:
                exit_code = 1
            else: 
                exit_code = 0
        break
    while option_choice == 5:
        
        exit_code = 0
        while exit_code == 0:
            
            delete_row()
            print("_________________________________________")
            print("\n1. Back To Menu\n2. Select Another Table\n")
            ch = int(input("[Select Option]: "))
            if ch == 1:
                exit_code = 1
            else: 
                exit_code = 0
        break
    while option_choice == 6:
        exitt_code = 1
        break
