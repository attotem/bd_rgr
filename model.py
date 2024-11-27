import psycopg2, random
from math import ceil, sqrt
from psycopg2 import Error

import datetime, time, string, random
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        print(f"\nFunction '{func.__name__}' executed in {elapsed_time:.4f} milliseconds\n")
        return result
    return wrapper

class Model:

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname = 'Shinkarenko',
            user = 'postgres',
            password = 'Edlk30112003#',
            host = 'localhost',
            port = 5432
        )

    # Перегляд

    @timeit
    def get_data_in_range(self, request):
        c = self.conn.cursor()
        try:
            commands = request.split(' ')
            table_name = commands[0]
            id_field = commands[1]
            id_start = commands[2]
            id_end = commands[3]
            order_field = commands[4]
            c.execute(f'SELECT * FROM "{table_name}" WHERE {id_field} BETWEEN {id_start} AND {id_end} ORDER BY {order_field}')
            self.conn.commit()
            rows_updated = c.rowcount
            result = c.fetchall()
            print(f"\n{rows_updated} rows affected\n")
        except Error as e:
            print(f"An error occurred: {e}")
            result = None
        finally:
            self.conn.rollback()

        c.close()
        
        return result
    
    @timeit
    def get_data_by_field_like(self, request):
        c = self.conn.cursor()
        try:
            commands = request.split(' ')
            table_name = commands[0]
            req_field = commands[1]
            search_req = commands[2]
            order_field = commands[3]
            c.execute(f'SELECT * FROM "{table_name}" WHERE {req_field} LIKE \'%{search_req}%\' ORDER BY {order_field}')
            self.conn.commit()
            rows_updated = c.rowcount
            result = c.fetchall()
            print(f"\n{rows_updated} rows affected.\n")
        except Error as e:
            print(f"An error occurred: {e}")
            result = None
        finally:
            self.conn.rollback()
            c.close()

        return result

    # ВИДАЛЕННЯ

    @timeit
    def delete_data(self, table_name, field, value):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM "%s" WHERE %s = %s' % (table_name, field, value))
            self.conn.commit()
            rows_updated = c.rowcount
            print(f"\n{rows_updated} rows affected ")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

        c.close()

    def fetch_query(self, query):
        """Виконує SELECT запит і повертає результат"""
        try:
            c = self.conn.cursor()
            c.execute(query)
            result = c.fetchall()
            c.close()
            return result
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return []

    def execute_query(self, query):
        """Виконує SQL-запит на вставку або оновлення даних"""
        try:
            c = self.conn.cursor()
            c.execute(query)
            self.conn.commit()
            c.close()
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            self.conn.rollback()

    # Додавання нового користувача
    @timeit
    def add_user(self, name):
        """Додавання нового користувача до таблиці users."""
        try:
            c = self.conn.cursor()

            # Отримання останнього значення user_id
            c.execute('SELECT MAX(user_id) FROM "users"')
            latest_id = c.fetchone()[0] or 0  # Якщо таблиця порожня, latest_id = 0

            # Додавання нового користувача
            new_id = latest_id + 1
            query = f'INSERT INTO "users" (user_id, name) VALUES (%s, %s)'
            c.execute(query, (new_id, name))

            self.conn.commit()
            print(f"User '{name}' added successfully with user_id = {new_id}.")

        except Exception as e:
            print(f"Error adding user: {str(e)}")
            self.conn.rollback()

        finally:
            c.close()


    # Оновлення даних користувача
    @timeit
    def update_user(self, user_id, new_name):
        try:
            c = self.conn.cursor()
            c.execute('UPDATE users SET name = %s WHERE user_id = %s', (new_name, user_id))
            self.conn.commit()
            print("\nUser successfully updated.")
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            self.conn.rollback()
        finally:
            c.close()

    # Видалення користувача
    @timeit
    def delete_user(self, user_id):
        try:
            c = self.conn.cursor()
            c.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
            self.conn.commit()
            print("\nUser successfully deleted.")
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            self.conn.rollback()
        finally:
            c.close()

    # Генерація користувачів
    @timeit
    def generate_users(self, num_users):
        """Генерація випадкових користувачів для таблиці users."""
        try:
            # Отримуємо максимальний user_id з таблиці, щоб уникнути дублювання
            query = 'SELECT MAX(user_id) FROM "users"'
            max_user_id = self.fetch_query(query)
            max_user_id = max_user_id[0][0] if max_user_id[0][0] else 0

            # Генерація користувачів
            query = f"""
                WITH generated_users AS (
                    SELECT 
                        (ROW_NUMBER() OVER () + {max_user_id}) AS user_id,  -- Генерація ID
                        'User_' || FLOOR(RANDOM() * 100000) AS name        -- Випадкове ім'я
                    FROM generate_series(1, {num_users})
                )
                INSERT INTO "users" (user_id, name)
                SELECT user_id, name
                FROM generated_users
            """
            self.execute_query(query)
            print(f"{num_users} users generated successfully.")

        except Exception as e:
            print(f"Error generating users: {str(e)}")

    @timeit
    def generate_restaurants(self, num_restaurants):
        """Генерація нових ресторанів"""
        try:
            # Отримуємо максимальний restaurant_id з таблиці для уникнення дублювання
            query = "SELECT MAX(restaurant_id) FROM restaurants"
            max_restaurant_id = self.fetch_query(query)
            max_restaurant_id = max_restaurant_id[0][0] if max_restaurant_id[0][0] else 0

            # Генерація ресторанів
            query = f"""
                WITH generated_restaurants AS (
                    SELECT 
                        (ROW_NUMBER() OVER () + {max_restaurant_id}) AS restaurant_id,
                        'Restaurant_' || (FLOOR(RANDOM() * 1000)) AS name,  -- Випадкове ім'я
                        FLOOR(RANDOM() * 50 + 1) AS table_quantity  -- Випадкова кількість столів від 1 до 50
                    FROM generate_series(1, {num_restaurants})
                )
                INSERT INTO restaurants (restaurant_id, name, table_quantity)
                SELECT restaurant_id, name, table_quantity
                FROM generated_restaurants
            """
            self.execute_query(query)
            print(f"{num_restaurants} restaurants generated successfully.")

        except Exception as e:
            print(f"Error generating restaurants: {str(e)}")


    @timeit
    def display_restaurants(self):
        """Перегляд усіх ресторанів"""
        try:
            query = "SELECT * FROM restaurants"
            result = self.fetch_query(query)
            if result:
                for row in result:
                    print(row)
            else:
                print("No restaurants found.")
        except Exception as e:
            print(f"Error displaying restaurants: {str(e)}")

    @timeit
    def add_restaurant(self, name, table_quantity):
        """Додавання нового ресторану з перевіркою максимального restaurant_id"""
        try:
            # Заміняємо одиночні апострофи на два апострофи
            name = name.replace("'", "''")

            # Отримуємо максимальний restaurant_id з таблиці для уникнення дублювання
            query = "SELECT MAX(restaurant_id) FROM restaurants"
            max_restaurant_id = self.fetch_query(query)
            max_restaurant_id = max_restaurant_id[0][0] if max_restaurant_id[0][0] else 0

            # Вставляємо новий ресторан з наступним restaurant_id
            query = f"""
                INSERT INTO restaurants (restaurant_id, name, table_quantity)
                VALUES ({max_restaurant_id + 1}, '{name}', {table_quantity})
            """
            self.execute_query(query)
            print(f"Restaurant '{name}' added successfully.")
        except Exception as e:
            print(f"Error adding restaurant: {str(e)}")


    @timeit
    def update_restaurant(self, restaurant_id, name, table_quantity):
        """Оновлення інформації про ресторан"""
        try:
            query = f"""
                UPDATE restaurants
                SET name = '{name}', table_quantity = {table_quantity}
                WHERE restaurant_id = {restaurant_id}
            """
            self.execute_query(query)
            print(f"Restaurant with ID {restaurant_id} updated successfully.")
        except Exception as e:
            print(f"Error updating restaurant: {str(e)}")


    @timeit
    def add_restaurant_table(self, capacity, restaurant_id):
        """Додавання нової таблиці до ресторану з унікальним ID"""
        try:
            # Отримуємо максимальний table_id для уникнення дублювання
            query = "SELECT MAX(table_id) FROM restaurant_tables"
            max_table_id = self.fetch_query(query)
            max_table_id = max_table_id[0][0] if max_table_id[0][0] else 0
            
            # Додавання нової таблиці ресторану
            query = f"""
                INSERT INTO restaurant_tables (table_id, capacity, restaurant_id)
                VALUES ({max_table_id + 1}, {capacity}, {restaurant_id})
            """
            self.execute_query(query)
            print(f"Restaurant table added successfully with ID {max_table_id + 1}.")
        except Exception as e:
            print(f"Error adding restaurant table: {str(e)}")


    @timeit
    def update_restaurant_table(self, table_id, capacity, restaurant_id):
        """Оновлення таблиці ресторану"""
        try:
            query = f"""
                UPDATE restaurant_tables
                SET capacity = {capacity}, restaurant_id = {restaurant_id}
                WHERE table_id = {table_id}
            """
            self.execute_query(query)
            print(f"Restaurant table {table_id} updated successfully.")
        except Exception as e:
            print(f"Error updating restaurant table: {str(e)}")

    @timeit
    def generate_restaurant_tables(self, num_tables):
        """Генерація нових столів для ресторанів з перевіркою максимальних значень"""
        try:
            # Отримуємо максимальний table_id з таблиці для уникнення дублювання
            query = "SELECT MAX(table_id) FROM restaurant_tables"
            max_table_id = self.fetch_query(query)
            max_table_id = max_table_id[0][0] if max_table_id[0][0] else 0  # Якщо таблиця порожня, починаємо з 0
            
            # Отримуємо максимальний restaurant_id з таблиці restaurants
            query = "SELECT MAX(restaurant_id) FROM restaurants"
            max_restaurant_id = self.fetch_query(query)
            max_restaurant_id = max_restaurant_id[0][0] if max_restaurant_id[0][0] else 0  # Якщо таблиця порожня, починаємо з 0
            
            # Генерація столів
            query = f"""
                WITH generated_tables AS (
                    SELECT 
                        (ROW_NUMBER() OVER () + {max_table_id}) AS table_id,  -- Унікальний table_id
                        FLOOR(RANDOM() * 10) + 1 AS capacity,  -- Випадкова кількість місць від 1 до 10
                        FLOOR(RANDOM() * {max_restaurant_id}) + 1 AS restaurant_id  -- Випадковий restaurant_id
                    FROM generate_series(1, {num_tables}) AS gs
                )
                INSERT INTO restaurant_tables (table_id, capacity, restaurant_id)
                SELECT table_id, capacity, restaurant_id
                FROM generated_tables;
            """
            self.execute_query(query)
            print(f"{num_tables} restaurant tables generated successfully.")
        
        except Exception as e:
            print(f"Error generating restaurant tables: {str(e)}")



    @timeit
    def display_reservations(self):
        """Виведення всіх бронювань"""
        query = "SELECT reservation_id, user_id, table_id, reservation_date, duration FROM reservations"
        reservations = self.fetch_query(query)
        if reservations:
            for reservation in reservations:
                print(f"ID: {reservation[0]}, User ID: {reservation[1]}, Table ID: {reservation[2]}, Date: {reservation[3]}, Duration: {reservation[4]} mins")
        else:
            print("No reservations found.")

    @timeit
    def add_reservation(self, user_id, table_id, reservation_date, duration):
        """Додавання нового бронювання"""
        try:
            # Отримуємо максимальний id для уникнення дублювання
            query = "SELECT MAX(reservation_id) FROM reservations"
            max_table_id = self.fetch_query(query)
            max_table_id = max_table_id[0][0] if max_table_id[0][0] else 0

            query = f"""
                INSERT INTO reservations (reservation_id, user_id, table_id, reservation_date, duration)
                VALUES ({max_table_id + 1}, {user_id}, {table_id}, '{reservation_date}', {duration})
            """
            self.execute_query(query)
            print(f"Reservation added successfully for user {user_id} at table {table_id}.")
        except Exception as e:
            print(f"Error adding reservation: {str(e)}")


    @timeit
    def update_reservation(self, reservation_id, user_id, table_id, reservation_date, duration):
        """Оновлення бронювання"""
        try:
            query = f"""
                UPDATE reservations
                SET user_id = {user_id}, table_id = {table_id}, reservation_date = '{reservation_date}', duration = {duration}
                WHERE reservation_id = {reservation_id}
            """
            self.execute_query(query)
            print(f"Reservation {reservation_id} updated successfully.")
        except Exception as e:
            print(f"Error updating reservation: {str(e)}")

    def generate_reservations(self, num_reservations):
        """Генерація випадкових бронювань без циклів, через SQL"""
        try:
            # Отримуємо максимальний reservation_id для уникнення дублювань
            query = "SELECT COALESCE(MAX(reservation_id), 0) FROM reservations"
            max_reservation_id = self.fetch_query(query)
            max_reservation_id = max_reservation_id[0][0]

            # Отримуємо максимальний table_id для можливих таблиць
            query = "SELECT MAX(table_id) FROM restaurant_tables"
            max_table_id = self.fetch_query(query)
            max_table_id = max_table_id[0][0] if max_table_id[0][0] else 0

            # Отримуємо максимальний user_id для перевірки доступних користувачів
            query = "SELECT MAX(user_id) FROM users"
            max_user_id = self.fetch_query(query)
            max_user_id = max_user_id[0][0] if max_user_id[0][0] else 0

            # Генеруємо випадкові бронювання через SQL
            query = f"""
                WITH random_reservations AS (
                    SELECT
                        (ROW_NUMBER() OVER ()) + {max_reservation_id} AS reservation_id,
                        (FLOOR(RANDOM() * {max_user_id})) AS user_id,  -- Випадковий user_id
                        (FLOOR(RANDOM() * {max_table_id})) AS table_id,  -- Випадковий table_id
                        NOW() + (INTERVAL '1 day' * FLOOR(RANDOM() * 31)) AS reservation_date,  -- Випадкова дата
                        (1 + FLOOR(RANDOM() * 3)) AS duration
                    FROM generate_series(1, {num_reservations}) gs
                )
                INSERT INTO reservations (reservation_id, user_id, table_id, reservation_date, duration)
                SELECT reservation_id, user_id, table_id, reservation_date, duration
                FROM random_reservations;
            """
            self.execute_query(query)
            print(f"Successfully generated {num_reservations} reservations.")

        except Exception as e:
            print(f"Error generating reservations: {str(e)}")

    def add_contact(self, user_id, email, phone):
        """Додавання нового контакту з унікальним contact_id"""
        try:
            # Отримуємо максимальний contact_id
            query = "SELECT MAX(contact_id) FROM contacts"
            max_contact_id = self.fetch_query(query)
            max_contact_id = max_contact_id[0][0] if max_contact_id[0][0] else 0  # Якщо таблиця порожня, починаємо з 0

            # Вставляємо новий контакт з contact_id на один більше від максимального
            query = f"""
                INSERT INTO contacts (contact_id, user_id, email, phone)
                VALUES ({max_contact_id + 1}, {user_id}, '{email}', '{phone}')
            """
            self.execute_query(query)
            print(f"Contact added successfully for user {user_id}.")
        except Exception as e:
            print(f"Error adding contact: {str(e)}")


    def update_contact(self, contact_id, field, value):
        """Оновлення даних контакту"""
        try:
            query = f"""
                UPDATE contacts
                SET {field} = '{value}'
                WHERE contact_id = {contact_id}
            """
            self.execute_query(query)
            print(f"Contact with ID {contact_id} updated successfully.")
        except Exception as e:
            print(f"Error updating contact: {str(e)}")
    
    def generate_contacts(self, num_contacts):
        """Генерація випадкових контактів"""
        try:
            # Отримуємо максимальні значення user_id для створення випадкових значень
            max_user_id = self.fetch_query("SELECT MAX(user_id) FROM users")[0][0] or 0
            
            query = f"""
            WITH generated_contacts AS (
                SELECT 
                    (ROW_NUMBER() OVER () + (SELECT COALESCE(MAX(contact_id), 0) FROM contacts)) AS contact_id,
                    (FLOOR(RANDOM() * {max_user_id}) + 1) AS user_id,  -- Випадковий user_id
                    CONCAT('user', FLOOR(RANDOM() * 1000), '@mail.com') AS email,  -- Випадковий email
                    LPAD(CAST(FLOOR(RANDOM() * 1000000000) AS TEXT), 10, '0') AS phone  -- Випадковий телефон
                FROM generate_series(1, {num_contacts}) AS gs
            )
            INSERT INTO contacts (contact_id, user_id, email, phone)
            SELECT contact_id, user_id, email, phone
            FROM generated_contacts
            """
            self.execute_query(query)
            print(f"{num_contacts} contacts generated successfully.")
        except Exception as e:
            print(f"Error generating contacts: {str(e)}")



