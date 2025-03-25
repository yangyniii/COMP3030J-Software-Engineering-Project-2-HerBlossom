import bcrypt
import pymysql

class Mysql(object):
    # connect to the database
    def __init__(self):
        """
        Initializes the database connection and cursor object.

        This method attempts to connect to a specified database (default is 'librarydb'). If the connection is successful,
        it creates a cursor object for executing SQL statements. If the connection fails, an error message is printed.

        Note:
            - The connection parameters (host, user, password, database) are hardcoded.
            - The character set used is "utf8mb3".
        """
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='librarydb',
                                        charset="utf8mb3")
            self.cursor = self.conn.cursor()
            # print("Connect Successfully")
        except:
            print("Connect failed")

    def getItems(self, page, keyword=None):
        """
        Fetches a list of items from the database based on the specified page and optional keyword.

        This method constructs and executes an SQL query to retrieve book information from the database.
        It supports pagination and keyword search functionality.

        Parameters:
        - page (int): The current page number used to calculate the LIMIT offset.
        - keyword (str, optional): A search term to filter results by title or author.

        Returns:
        - list: A list of items (books) matching the query criteria.
        """
        sql = "SELECT * FROM books"
        params = []

        if keyword:
            # Add conditions to the SQL query if a keyword is provided
            sql += " WHERE title LIKE %s OR author LIKE %s"
            params = ['%' + keyword + '%', '%' + keyword + '%']  # for security

        start = (int(page) - 1) * 10
        sql += " LIMIT %s, %s"
        params.append(start)
        params.append(10)  # how many items displayed in one page

        self.cursor.execute(sql, params)
        items = self.cursor.fetchall()
        return items

    def get_user_id(self, email):
        sql = "SELECT id FROM users WHERE email = %s"
        self.cursor.execute(sql, (email,))
        user_id = self.cursor.fetchone()
        if user_id:
            return user_id[0]  # 返回元组的第一个元素，即整数
        return None

    def get_losts(self):
        """
        Retrieve a list of all losts from the database.

        Returns:
        - list: A list of dictionaries containing lost information.
        """
        sql = "SELECT * FROM lost"
        self.cursor.execute(sql)
        losts = self.cursor.fetchall()
        lost_list = []
        for lost in losts:
            lost_list.append({
                'id': lost[0],
                'name': lost[1],
                'date': lost[2],
                'location': lost[3],
                'description': lost[4],
                'thumbnail_url': lost[5]
            })
        return lost_list

    def get_lost_by_id(self, lost_id):
        """
        Retrieve a lost by its ID from the database.

        Returns:
        - dict: A dictionary containing lost information.
        """
        sql = "SELECT * FROM lost WHERE id = %s"
        self.cursor.execute(sql, (lost_id,))
        lost = self.cursor.fetchone()
        if lost:
            return {
                'id': lost[0],
                'name': lost[1],
                'date': lost[2],
                'location': lost[3],
                'description': lost[4],
                'thumbnail_url': lost[5]
            }
        return None

    def get_books(self):
        """
        Retrieve a list of all books from the database.

        Returns:
        - list: A list of dictionaries containing book information.
        """
        sql = "SELECT * FROM books"
        self.cursor.execute(sql)
        books = self.cursor.fetchall()
        book_list = []
        for book in books:
            book_list.append({
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'publisher': book[3],
                'edition': book[4],
                'isbn': book[5],
                'tag': book[6],
                'description':book[7],
                'collections':book[8],
                'borrowed': book[9],
                'thumbnail_url': book[10]
            })
        return book_list

    def get_book_by_id(self, book_id):
        """
        Retrieve a book by its ID from the database.

        Returns:
        - dict: A dictionary containing book information.
        """
        sql = "SELECT * FROM books WHERE id = %s"
        self.cursor.execute(sql, (book_id,))
        book = self.cursor.fetchone()
        if book:
            print(book[10])
            return {
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'publisher': book[3],
                'edition': book[4],
                'isbn': book[5],
                'tag': book[6],
                'description':book[7],
                'collections':book[8],
                'borrowed': book[9],
                'thumbnail_url': book[10]
            }
        return None

    def update_book(self, book_id, updated_info):
        try:
            # Validate ISBN
            if 'isbn' in updated_info:
                isbn = updated_info['isbn']
                self.cursor.execute("SELECT id FROM books WHERE isbn = %s AND id != %s", (isbn, book_id))
                if self.cursor.fetchone():
                    print("ISBN already exists.")
                    return {
                        'success': False,
                        'message': 'ISBN already exists.'
                    }

            # Update the book information in the database
            set_clause = ", ".join([f"{key} = %s" for key in updated_info.keys()])
            query = f"UPDATE books SET {set_clause} WHERE id = %s"
            values = list(updated_info.values()) + [book_id]
            print(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Book updated successfully.")

            return {
                'success': True
            }
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating book: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

    def update_book_thumbnail(self, book_id, thumbnail_url):
        try:
            # Validate the thumbnail URL
            if not thumbnail_url.startswith('/static/photo/'):
                print("Invalid thumbnail URL.")
                return {
                    'success': False,
                    'message': 'Invalid thumbnail URL. Must be under /static/photo/.'
                }

            # Update the thumbnail in the database
            query = "UPDATE books SET thumbnail_url = %s WHERE id = %s"
            values = (thumbnail_url, book_id)

            print(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Thumbnail updated successfully.")

            return {
                'success': True,
                'message': 'Thumbnail updated successfully.'
            }
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating thumbnail: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

    def update_lost_thumbnail(self, lost_id, thumbnail_url):
        try:
            # Validate the thumbnail URL
            if not thumbnail_url.startswith('/static/photo/'):
                print("Invalid thumbnail URL.")
                return {
                    'success': False,
                    'message': 'Invalid thumbnail URL. Must be under /static/photo/.'
                }

            # Update the thumbnail in the database
            query = "UPDATE lost SET thumbnail_url = %s WHERE id = %s"
            values = (thumbnail_url, lost_id)

            print(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Thumbnail updated successfully.")

            return {
                'success': True,
                'message': 'Thumbnail updated successfully.'
            }
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating thumbnail: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    def update_lost(self, lost_id, updated_info):
        try:
            # Update the lost information in the database
            set_clause = ", ".join([f"{key} = %s" for key in updated_info.keys()])
            query = f"UPDATE lost SET {set_clause} WHERE id = %s"
            values = list(updated_info.values()) + [lost_id]
            print(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Lost updated successfully.")

            return {
                'success': True
            }
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating lost: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

    def delete_lost(self, lost_id):
        query = "DELETE FROM lost WHERE id = %s"
        self.cursor.execute(query, (lost_id,))
        self.conn.commit()
        return True

    def add_book(self, book_data):
        try:
            self.cursor.execute('''
                INSERT INTO books (title, author, publisher, edition, isbn, tag, description, collections, borrowed, thumbnail_url, read_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                book_data['title'],
                book_data['author'],
                book_data['publisher'],
                book_data['edition'],
                book_data['isbn'],
                book_data['tag'],
                book_data['description'],
                book_data['collections'],
                book_data['borrowed'],
                book_data['thumbnail_url'],
                book_data['read_count'],
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding book: {e}")
            return False

    def add_lost(self, lost_data):
        try:
            self.cursor.execute('''
                INSERT INTO lost (name, date, location, description,thumbnail_url)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                lost_data['name'],
                lost_data['date'],
                lost_data['location'],
                lost_data['description'],
                lost_data['thumbnail_url'],
            ))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding lost: {e}")
            return False

    def isbn_exists(self, isbn):
        query = "SELECT COUNT(*) FROM books WHERE isbn = %s"
        self.cursor.execute(query, (isbn,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def lend_book(self, book_id, borrower_id, time_till_return):
        try:
            # Update the borrowed count and read_count in the books table
            self.cursor.execute("""
                        UPDATE books 
                        SET borrowed = borrowed + 1, 
                            read_count = read_count + 1 
                        WHERE id = %s
                    """, (book_id,))
            self.conn.commit()

            # update the borrower's read_count
            self.cursor.execute("""
                        UPDATE users 
                        SET read_count = read_count + 1 
                        WHERE id = %s
                    """, (borrower_id,))
            self.conn.commit()

            # Insert a new record into the borrow table
            self.cursor.execute("INSERT INTO borrow (book_id, borrower_id, time_till_return) VALUES (%s, %s, %s)",
                                (book_id, borrower_id, time_till_return))
            self.conn.commit()

            # Get the updated borrowed count
            self.cursor.execute("SELECT borrowed FROM books WHERE id = %s", (book_id,))
            new_borrowed_count = self.cursor.fetchone()[0]

            return {
                'success': True,
                'new_borrowed_count': new_borrowed_count
            }
        except Exception as e:
            self.conn.rollback()
            return {
                'success': False,
                'message': str(e)
            }
        finally:
            self.cursor.close()

    def return_book(self, book_id):
        try:
            # Update the borrowed count in the books table
            self.cursor.execute("UPDATE books SET borrowed = borrowed - 1 WHERE id = %s", (book_id,))
            self.conn.commit()

            # Get the updated borrowed count
            self.cursor.execute("SELECT borrowed FROM books WHERE id = %s", (book_id,))
            new_borrowed_count = self.cursor.fetchone()[0]

            return {
                'success': True,
                'new_borrowed_count': new_borrowed_count
            }
        except Exception as e:
            self.conn.rollback()
            return {
                'success': False,
                'message': str(e)
            }
        finally:
            self.cursor.close()

    def search_books_by_title(self, title):
        query = ("SELECT id, title, author, publisher, collections, borrowed, thumbnail_url FROM books WHERE title "
                 "LIKE %s")
        self.cursor.execute(query, (f"%{title}%",))
        columns = [desc[0] for desc in self.cursor.description]  # 获取列名
        results = self.cursor.fetchall()
        books = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
        return books

    def search_losts_by_name(self, name):
        query = "SELECT id, name, date, location, description , thumbnail_url FROM lost WHERE name LIKE %s"
        self.cursor.execute(query, (f"%{name}%",))
        columns = [desc[0] for desc in self.cursor.description]  # 获取列名
        results = self.cursor.fetchall()
        losts = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
        return losts

    def search_losts_by_date(self, date):
        query = "SELECT id, name, date, location, description, thumbnail_url FROM lost WHERE date = %s"
        self.cursor.execute(query, (date,))
        columns = [desc[0] for desc in self.cursor.description]  # 获取列名
        results = self.cursor.fetchall()
        losts = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
        return losts

    def search_books_by_tag(self, tag):
        query = "SELECT id, title, author, publisher, collections, borrowed , thumbnail_url FROM books WHERE tag = %s"
        self.cursor.execute(query, (tag,))
        columns = [desc[0] for desc in self.cursor.description]  # 获取列名
        results = self.cursor.fetchall()
        books = [{columns[i]: row[i] for i in range(len(columns))} for row in results]  # 将元组转换为包含键值对的列表
        return books

    def register_user(self, name, password, email, avatar, cover):
        """
        Registers a new user in the database.

        This function inserts a new record into the `users` table with the provided details.
        If a user with the given email already exists, it returns an error message.

        Parameters:
        - name (str): The name of the user.
        - password (str): The user's password.
        - email (str): The user's email address.
        - avatar (str): The path or URL of the user's avatar.
        - cover (str): The path or URL of the user's cover image.

        Returns:
        - str: A message indicating whether the user was successfully registered or if the email already exists.
        """
        if self.exist_user(email):
            return "User already exists"

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        sql = "INSERT INTO users(username, email, password, avatar, cover) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (name, email, hashed_password, avatar, cover))
        self.conn.commit()
        return "User registered successfully"


    def signin_user(self, identification, email, password):
        query = "SELECT id, name, password, identification, email, avatar, is_banned, ban_reason, ban_end_time FROM users WHERE identification = %s AND email = %s"

        values = (identification, email)
        self.cursor.execute(query, values)
        user_tuple = self.cursor.fetchone()
        if user_tuple:
            column_names = [desc[0] for desc in self.cursor.description]
            print("Column names:", column_names)  # Debug message to check column names
            user_dict = dict(zip(column_names, user_tuple))

            if bcrypt.checkpw(password.encode('utf-8'), user_dict['password'].encode('utf-8')):
                print("User data:", user_dict)  # Debug message to inspect user data
                return user_dict
            else:
                return None


    @staticmethod
    def exist_user(email):
        """
        Checks if a user exists in the database by their email.

        This static method queries the database to determine whether a user with the given email exists.

        Parameters:
        - email (str): The email address to check.

        Returns:
        - bool: True if the user exists, False otherwise.
        """
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='librarydb', charset="utf8mb3")
        cursor = conn.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        return result is not None

    def get_user_info(self, email):
        """
        Retrieve user information based on the user's email.

        Parameters:
        - email (str): The email address of the user to query.

        Returns:
        - dict: A dictionary containing the user's information including name, password, identification, email, and avatar.
                If the user is not found, returns None.
        """
        sql = "SELECT id,name, password, identification, email, avatar FROM users WHERE email = %s"
        self.cursor.execute(sql, (email,))
        user_info = self.cursor.fetchone()
        if user_info:
            avatar = user_info[5] if user_info[5] else '../static/photo/default_avatar.png'
            return {
                'id': user_info[0],
                'name': user_info[1],
                'password': user_info[2],
                'identification': user_info[3],
                'email': user_info[4],
                'avatar': avatar
            }
        return None

    def get_avatar(self, email):
        """
        Retrieves the user's avatar path from the database based on the email.

        Parameters:
        - email (str): The user's email address, used to query the corresponding avatar.

        Returns:
        - str: The file path of the avatar.
               If no avatar is found, returns None.
        """
        sql = "SELECT avatar FROM users WHERE email = %s"
        self.cursor.execute(sql, (email,))
        avatar = self.cursor.fetchone()
        return avatar[0] if avatar else None

    def update_password(self, email, new_password):
        """
        Update the user's password.

        This function updates the password for a user identified by their email address in the database.

        Parameters:
        - email (str): The email address of the user whose password is to be updated.
        - new_password (str): The new password to set for the user.

        Returns:
        - str: A success message indicating that the password has been updated successfully.
        """
        sql = "UPDATE users SET password = %s WHERE email = %s"
        self.cursor.execute(sql, (new_password, email))
        self.conn.commit()
        return "Password updated successfully"

    def update_user_avatar(self, email, avatar_url):
        """
        Update user avatar.

        This function updates the avatar URL for a user identified by their email address in the database.

        Parameters:
        - email (str): The email address of the user, used to locate the user record in the database.
        - avatar_url (str): The new avatar URL to replace the old one.

        Returns:
        - str: If the avatar URL is updated successfully, returns "Avatar updated successfully".
               Otherwise, returns "Error updating avatar".
        """
        try:
            sql = "UPDATE users SET avatar = %s WHERE email = %s"
            self.cursor.execute(sql, (avatar_url, email))
            self.conn.commit()
            print(f"User {email} photo has been changed to {avatar_url}")
            return "Avatar updated successfully"
        except Exception as e:
            print(f"Update avatar failed: {e}")
            return "Error updating avatar"



    def get_all_users(self):
        """
        Fetches all users from the database.

        Returns:
        - list: A list of dictionaries, each representing a user. If no users are found, returns an empty list.
        """
        try:
            sql = "SELECT name, password, identification, email, avatar FROM users"
            self.cursor.execute(sql)
            users = self.cursor.fetchall()

            # Retrieve column names for creating a dictionary for each user
            column_names = [desc[0] for desc in self.cursor.description]

            # Map the fetched data to a list of dictionaries
            user_list = [
                {
                    column: (value if column != "avatar" or value else "../static/photo/default_avatar.png")
                    for column, value in zip(column_names, user)
                }
                for user in users
            ]
            return user_list

        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def get_users_by_role_from_db(self, role):
        """
        Fetches users from the database based on their role.

        Parameters:
        - role (str): The role of the user (e.g., 'Student', 'Staff', 'Administrator').

        Returns:
        - list: A list of dictionaries, each representing a user with the specified role.
        """
        try:
            sql = "SELECT name, password, identification, email, avatar FROM users WHERE identification = %s"
            self.cursor.execute(sql, (role,))
            users = self.cursor.fetchall()

            # Retrieve column names for creating a dictionary for each user
            column_names = [desc[0] for desc in self.cursor.description]

            # Map the fetched data to a list of dictionaries
            user_list = [
                {
                    column: (value if column != "avatar" or value else "../static/photo/default_avatar.png")
                    for column, value in zip(column_names, user)
                }
                for user in users
            ]
            return user_list

        except Exception as e:
            print(f"Error fetching users by role '{role}': {e}")
            return []

    def delete_account(self, email):
        """
        Deletes a user account from the database based on their identification.

        Parameters:
        - Email (str): The unique email of the user to be deleted.

        Returns:
        - bool: True if the account was successfully deleted, False otherwise.
        """
        try:
            # SQL query to delete a user account based on identification
            sql = "DELETE FROM users WHERE email = %s"
            self.cursor.execute(sql, (email,))

            # Commit the transaction
            self.conn.commit()

            # Check if the account was deleted by checking if any row was affected
            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            # If an error occurs, rollback the transaction and return False
            self.conn.rollback()
            print(f"Error deleting account: {e}")
            return False

    def update_user_info(self, email, name, new_email, password):
        """
        Update user information in the database.

        Parameters:
        - email (str): The current email of the user.
        - name (str): The new name of the user.
        - new_email (str): The new email of the user.
        - password (str): The new password of the user.

        Returns:
        - bool: True if the update was successful, False otherwise.
        """
        try:
            sql = "UPDATE users SET name = %s, email = %s, password = %s WHERE email = %s"
            self.cursor.execute(sql, (name, new_email, password, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user info: {e}")
            self.conn.rollback()
            return False

    def get_users_by_name(self, name):
        """
        Fetches users from the database based on their name.

        Parameters:
        - name (str): The name of the user to search for.

        Returns:
        - list: A list of dictionaries, each representing a user with the specified name.
        """
        try:
            sql = "SELECT name, password, identification, email, avatar FROM users WHERE name LIKE %s"
            self.cursor.execute(sql, ('%' + name + '%',))
            users = self.cursor.fetchall()

            # Retrieve column names for creating a dictionary for each user
            column_names = [desc[0] for desc in self.cursor.description]

            # Map the fetched data to a list of dictionaries
            user_list = [
                {
                    column: (value if column != "avatar" or value else "../static/photo/default_avatar.png")
                    for column, value in zip(column_names, user)
                }
                for user in users
            ]
            return user_list

        except Exception as e:
            print(f"Error fetching users by name '{name}': {e}")
            return []

    def ban_user(self, email, reason, end_time):
        """
        Bans a user by setting the is_banned flag to True, storing the ban reason, and setting the ban end time.

        Parameters:
        - email (str): The email address of the user to be banned.
        - reason (str): The reason for banning the user.
        - end_time (datetime): The datetime when the ban will end.

        Returns:
        - bool: True if the user was successfully banned, False otherwise.
        """
        try:
            sql = "UPDATE users SET is_banned = TRUE, ban_reason = %s, ban_end_time = %s WHERE email = %s"
            self.cursor.execute(sql, (reason, end_time, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error banning user: {e}")
            self.conn.rollback()
            return False

    def exist_log_user(self, email):
        sql = "SELECT COUNT(*) FROM users WHERE email = %s"
        self.cursor.execute(sql, (email,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def get_reading_ranking(self):
        """
        Retrieve books ranked by reading volume from the database.

        Returns:
        - list: A list of dictionaries containing ranked book information.
        """
        sql = """
        SELECT id, title, author, thumbnail_url, read_count
        FROM books
        ORDER BY read_count DESC
        """
        self.cursor.execute(sql)
        books = self.cursor.fetchall()

        ranked_books = []
        for book in books:
            ranked_books.append({
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'thumbnail_url': book[3],
                'read_count': book[4]
            })
        return ranked_books

    def get_user_reading_ranking(self):
        """
        Retrieve users ranked by reading volume for the current month from the database.

        Returns:
        - list: A list of dictionaries containing ranked user information.
        """
        sql = """
        SELECT id, name, avatar, read_count
        FROM users
        ORDER BY read_count DESC
        """
        self.cursor.execute(sql)
        users = self.cursor.fetchall()

        ranked_users = []
        for user in users:
            ranked_users.append({
                'id': user[0],
                'name': user[1],
                'avatar': user[2],
                'read_count': user[3]
            })
        return ranked_users
