class View:

    def show_message(self, message):
        print(message)

    def get_input(self, input_message):
        try:
            inp = input(input_message)
        except Exception as e:
            print(f"Error uccored: {e}")
            inp = None
        return inp

    def display_users(self, users):
        print("\nList of Users:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}")

    def display_restaurants(self, restaurants):
        """Виведення списку ресторанів"""
        if restaurants:
            for restaurant in restaurants:
                print(f"ID: {restaurant[0]}, Name: {restaurant[1]}, Table Quantity: {restaurant[2]}")
        else:
            print("No restaurants to display.")

    def show_restaurant_tables(self, restaurant_tables):
        """Виведення списку таблиць ресторану"""
        if restaurant_tables:
            for table in restaurant_tables:
                print(f"Table ID: {table[0]}, Capacity: {table[1]}, Restaurant ID: {table[2]}")
        else:
            print("No restaurant tables to display.")

    def show_reservations(self, reservations):
        """Виведення списку бронювань"""
        if reservations:
            for reservation in reservations:
                print(f"Reservation ID: {reservation[0]}, User ID: {reservation[1]}, Table ID: {reservation[2]}, Date: {reservation[3]}, Duration: {reservation[4]} minutes")
        else:
            print("No reservations to display.")

    def show_contacts(self, contacts):
        """Виведення списку контактів"""
        if contacts:
            for contact in contacts:
                print(f"Contact ID: {contact[0]}, User ID: {contact[1]}, Email: {contact[2]}, Phone: {contact[3]}")
        else:
            print("No contacts to display.")

