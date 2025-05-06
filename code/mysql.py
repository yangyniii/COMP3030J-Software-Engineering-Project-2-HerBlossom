import bcrypt
import pymysql
import time
from datetime import datetime


class Mysql(object):
    # connect to the database
    def __init__(self):
        """
        Initializes the database connection and cursor object.

        This method attempts to connect to a specified database (default is 'herblossom'). If the connection is successful,
        it creates a cursor object for executing SQL statements. If the connection fails, an error message is printed.

        Note:
            - The connection parameters (host, user, password, database) are hardcoded.
            - The character set used is "utf8mb3".
        """
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='herblossom',
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

    def get_post_by_id(self, post_id):
        """
        Retrieve a post by its ID from the database.

        Returns:
        - dict: A dictionary containing post information.
        """
        sql = "SELECT * FROM post WHERE post_id = %s"
        self.cursor.execute(sql, (post_id,))
        post = self.cursor.fetchone()
        if post:
            print(post[2])
            return {
                'id': post[0],
                'user_id': post[1],
                'title': post[2],
                'content': post[3],
                'tags': post[4],
                'category': post[5],
                'comment_count': post[6],
                'create_time': post[7],
                'image_urls': post[8],
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


    def register_user(self, name, password, email, avatar, cover, follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location):
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
        try:
            if self.exist_user(email):
                return "User already exists"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            sql = "INSERT INTO users(username, email, avatar, cover, password,follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (name, email, avatar, cover, hashed_password,follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location))
            self.conn.commit()
            return "User registered successfully"
        except Exception as e:
            print(f"Error during registration: {e}")
            return "Error during registration"

    def signin_user(self, email, password):
        query = "SELECT user_id, username, email, avatar, cover, password,follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location FROM users WHERE email = %s"

        self.cursor.execute(query, email)
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
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='herblossom', charset="utf8mb3")
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
        sql = "SELECT user_id, username, email, avatar, cover, password,follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location FROM users WHERE email = %s"
        self.cursor.execute(sql, (email,))
        user_info = self.cursor.fetchone()

        if user_info:
            avatar = user_info[3] if user_info[3] else '../static/images/chiikawa.jpg'
            cover = user_info[4] if user_info[4] else '../static/images/chiikawa.jpg'
            return {
                'user_id': user_info[0],
                'username': user_info[1],
                'email': user_info[2],
                'avatar': user_info[3] or '../static/images/chiikawa.jpg',  # 避免 avatar 为 None
                'cover': user_info[4] or '../static/images/chiikawa.jpg',
                'password': user_info[5],
                'follower_count': user_info[6],
                'followee_count': user_info[7],
                'following_topic_count': user_info[8],
                'post_count': user_info[9],
                'comment_count': user_info[10],
                'bio': user_info[11],
                'company': user_info[12],
                'location': user_info[13]

            }

        return None


    def get_user_info_by_id(self, user_id):
        """
        Retrieve user information based on the user's email.

        Parameters:
        - email (str): The email address of the user to query.

        Returns:
        - dict: A dictionary containing the user's information including name, password, identification, email, and avatar.
                If the user is not found, returns None.
        """
        sql = "SELECT user_id, username, email, avatar, cover, password,follower_count,followee_count,following_topic_count,post_count,comment_count,bio,company,location FROM users WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        user_info = self.cursor.fetchone()
        if user_info:
            avatar = user_info[3] if user_info[3] else '../static/images/chiikawa.jpg'
            cover = user_info[4] if user_info[4] else '../static/images/chiikawa.jpg'
            return {
                'user_id': user_info[0],
                'username': user_info[1],
                'email': user_info[2],
                'avatar': avatar,
                'cover': cover,
                'password': user_info[5],
                'follower_count': user_info[6],
                'followee_count': user_info[7],
                'following_topic_count': user_info[8],
                'post_count': user_info[9],
                'comment_count': user_info[10],
                'bio': user_info[11],
                'company': user_info[12],
                'location': user_info[13]
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
                    column: (value if column != "avatar" or value else "../static/images/chiikawa.jpg")
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
                    column: (value if column != "avatar" or value else "../static/images/chiikawa.jpg")
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
                    column: (value if column != "avatar" or value else "../static/images/chiikawa.jpg")
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

    def get_posts(self):
        """
        Retrieve a list of all books from the database.

        Returns:
        - list: A list of dictionaries containing book information.
        """
        sql = "SELECT * FROM post ORDER BY create_time DESC"
        self.cursor.execute(sql)
        posts = self.cursor.fetchall()
        posts_list = []
        for post in posts:
            posts_list.append({
                'post_id': post[0],
                'user_id': post[1],
                'title': post[2],
                'content': post[3],
                'tags': post[4],
                'category': post[5],
                'comment_count': post[6],
                'create_time': post[7],
                'image_urls': post[8],
            })
        return posts_list

    def search_posts_by_title(self, title):
        query = """
            SELECT p.post_id, p.user_id, p.title, p.content, p.tags, p.category, 
                   p.comment_count, p.create_time, p.image_urls, u.username
            FROM post p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.title LIKE %s 
               OR p.content LIKE %s
               OR p.tags LIKE %s
               OR u.username LIKE %s
        """
        search_term = f"%{title}%"
        self.cursor.execute(query, (search_term, search_term, search_term, search_term))
        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        posts = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
        return posts

    def insert_post(self, user_id, title, content, tags, category, image_urls):
        sql = """
            INSERT INTO post (user_id, title, content, tags, category, comment_count, create_time, image_urls)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute(sql, (user_id, title, content, tags, category, 0, create_time, image_urls))
            self.conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()

    def get_all_blogs(self):
        """
        获取所有博客信息
        
        Returns:
            list: 博客列表
        """
        try:
            sql = "SELECT * FROM blog ORDER BY create_time DESC"
            self.cursor.execute(sql)
            blogs = self.cursor.fetchall()
            return blogs
        except Exception as e:
            print(f"获取博客列表失败: {e}")
            return []
            
    def get_blogs_by_category(self, category):
        """
        根据分类获取博客信息
        
        Parameters:
            category (str): 博客分类
            
        Returns:
            list: 博客列表
        """
        try:
            sql = "SELECT * FROM blog WHERE category = %s ORDER BY create_time DESC"
            self.cursor.execute(sql, (category,))
            blogs = self.cursor.fetchall()
            return blogs
        except Exception as e:
            print(f"获取分类博客列表失败: {e}")
            return []
            
    def get_featured_blog(self):
        """
        获取特色博客信息
        
        Returns:
            tuple: 特色博客信息
        """
        try:
            sql = "SELECT * FROM blog WHERE is_featured = 1 ORDER BY create_time DESC LIMIT 1"
            self.cursor.execute(sql)
            blog = self.cursor.fetchone()
            return blog
        except Exception as e:
            print(f"获取特色博客失败: {e}")
            return None
            
    def add_blog(self, blog_data):
        """
        添加博客信息
        
        Parameters:
            blog_data (dict): 博客数据
            
        Returns:
            bool: 是否添加成功
        """
        try:
            current_time = int(time.time())
            sql = """
                INSERT INTO blog (title, content, image_url, category, read_time, 
                                 author_name, author_avatar, publish_date, link_url, 
                                 is_featured, create_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (
                blog_data.get('title'),
                blog_data.get('content'),
                blog_data.get('image_url'),
                blog_data.get('category'),
                blog_data.get('read_time'),
                blog_data.get('author_name'),
                blog_data.get('author_avatar'),
                blog_data.get('publish_date'),
                blog_data.get('link_url'),
                blog_data.get('is_featured', 0),
                current_time
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"添加博客失败: {e}")
            self.conn.rollback()
            return False
            
    def get_blog_by_id(self, blog_id):
        """
        根据ID获取博客信息
        
        Parameters:
            blog_id (int): 博客ID
            
        Returns:
            tuple: 博客信息
        """
        try:
            sql = "SELECT * FROM blog WHERE blog_id = %s"
            self.cursor.execute(sql, (blog_id,))
            blog = self.cursor.fetchone()
            return blog
        except Exception as e:
            print(f"获取博客详情失败: {e}")
            return None
            
    def update_blog(self, blog_id, blog_data):
        """
        更新博客信息
        
        Parameters:
            blog_id (int): 博客ID
            blog_data (dict): 博客数据
            
        Returns:
            bool: 是否更新成功
        """
        try:
            sql = """
                UPDATE blog 
                SET title = %s, content = %s, image_url = %s, category = %s, 
                    read_time = %s, author_name = %s, author_avatar = %s, 
                    publish_date = %s, link_url = %s, is_featured = %s
                WHERE blog_id = %s
            """
            self.cursor.execute(sql, (
                blog_data.get('title'),
                blog_data.get('content'),
                blog_data.get('image_url'),
                blog_data.get('category'),
                blog_data.get('read_time'),
                blog_data.get('author_name'),
                blog_data.get('author_avatar'),
                blog_data.get('publish_date'),
                blog_data.get('link_url'),
                blog_data.get('is_featured', 0),
                blog_id
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"更新博客失败: {e}")
            self.conn.rollback()
            return False
            
    def delete_blog(self, blog_id):
        """
        删除博客
        
        Parameters:
            blog_id (int): 博客ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            sql = "DELETE FROM blog WHERE blog_id = %s"
            self.cursor.execute(sql, (blog_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"删除博客失败: {e}")
            self.conn.rollback()
            return False
            
    def search_blogs(self, keyword):
        """
        搜索博客
        
        Parameters:
            keyword (str): 搜索关键词
            
        Returns:
            list: 博客列表
        """
        try:
            sql = "SELECT * FROM blog WHERE title LIKE %s OR content LIKE %s ORDER BY create_time DESC"
            self.cursor.execute(sql, (f'%{keyword}%', f'%{keyword}%'))
            blogs = self.cursor.fetchall()
            return blogs
        except Exception as e:
            print(f"搜索博客失败: {e}")
            return []

    def get_all_unique_tags(self):
        """獲取所有帖子中不重複的標籤"""
        query = """
            SELECT DISTINCT TRIM(tag) as tag
            FROM (
                SELECT tags, 
                       SUBSTRING_INDEX(SUBSTRING_INDEX(tags, ',', numbers.n), ',', -1) as tag
                FROM post
                JOIN (
                    SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
                    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
                ) numbers ON CHAR_LENGTH(tags) - CHAR_LENGTH(REPLACE(tags, ',', '')) >= numbers.n - 1
                WHERE tags IS NOT NULL AND tags != ''
            ) extracted_tags
            WHERE TRIM(tag) != ''
            ORDER BY tag ASC
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [row[0] for row in results]

    def get_all_jobs(self):
        sql = "SELECT job_id, title, location, salary, company, experience, education, short_desc, full_desc, tags, latitude, longitude FROM job"
        try:
            self.cursor.execute(sql)
            jobs = self.cursor.fetchall()
            job_list = []

            for job in jobs:
                job_list.append({
                    'job_id': job[0],
                    'title': job[1],
                    'location': job[2],
                    'salary': job[3],
                    'company':job[4],
                    'experience': job[5],
                    'education': job[6],
                    'short_desc': job[7],
                    'full_desc': job[8],
                    'tags': job[9],
                    'latitude': job[10],
                    'longitude': job[11]
                })
            print(job_list)
            return job_list
        except Exception as e:
            print(f"查询 job 表失败: {e}")
            return []

    def search_jobs_by_keyword(self, keyword, location='', title='', salary='', education='', tag='',company=''):
        """
        根據多個條件搜索職位
        
        Parameters:
            keyword (str): 關鍵字
            location (str): 地點
            title (str): 職位名稱
            salary (str): 薪資範圍
            education (str): 學歷要求
            tag (str): 標籤
            
        Returns:
            list: 職位列表
        """
        conditions = []
        params = []
        
        base_query = """
            SELECT job.job_id,
                   job.title,
                   job.location,
                   job.salary,
                   job.company,
                   job.experience,
                   job.education,
                   job.short_desc,
                   job.full_desc,
                   job.tags,
                   job.latitude,
                   job.longitude
            FROM job
            WHERE 1=1
        """
        
        if keyword:
            conditions.append("""
                (job.title LIKE %s
                OR job.location LIKE %s
                OR job.company LIKE %s
                OR job.experience LIKE %s
                OR job.education LIKE %s
                OR job.short_desc LIKE %s
                OR job.full_desc LIKE %s
                OR job.tags LIKE %s)
            """)
            search_term = f"%{keyword}%"
            params.extend([search_term] * 8)
            
        if location:
            conditions.append("job.location LIKE %s")
            params.append(f"%{location}%")
            
        if title:
            conditions.append("job.title LIKE %s")
            params.append(f"%{title}%")
            
        if salary:
            # 處理薪資範圍
            if salary == "0-5k":
                conditions.append("job.salary BETWEEN 0 AND 10000")
            elif salary == "5k-10k":
                conditions.append("job.salary BETWEEN 5000 AND 10000")
            elif salary == "10k-15k":
                conditions.append("job.salary BETWEEN 10000 AND 15000")
            elif salary == "15k-20k":
                conditions.append("job.salary BETWEEN 20000 AND 20000")
            elif salary == "20k+":
                conditions.append("job.salary > 20000")
            
        if education:
            conditions.append("job.education LIKE %s")
            params.append(f"%{education}%")
            
        if tag:
            conditions.append("job.tags LIKE %s")
            params.append(f"%{tag}%")

        if company:
            conditions.append("job.company LIKE %s")
            params.append(f"%{company}%")
            
        if conditions:
            query = base_query + " AND " + " AND ".join(conditions)
        else:
            query = base_query
            
        query += " ORDER BY job.job_id DESC"
        
        try:
            self.cursor.execute(query, params)
            columns = [desc[0] for desc in self.cursor.description]
            results = self.cursor.fetchall()
            jobs = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
            return jobs
        except Exception as e:
            print(f"搜索職位失敗: {e}")
            return []

    def get_comments_by_post_id(self, post_id):
        sql = """
              SELECT comment.*, users.username
              FROM comment
                       JOIN users ON comment.user_id = users.user_id -- 修正为 users.user_id
              WHERE post_id = %s
              ORDER BY create_time ASC \
              """
        self.cursor.execute(sql, (post_id,))
        comments = self.cursor.fetchall()
        author_comments = []
        other_comments = []

        for c in comments:
            comment_data = {
                'id': c[0],
                'post_id': c[1],
                'user_id': c[2],
                'content': c[3],
                'create_time': c[4],
                'is_author': c[5],
                'username': c[6]
            }
            if c[5]:  # is_author = 1
                author_comments.append(comment_data)
            else:
                other_comments.append(comment_data)
        return author_comments, other_comments





