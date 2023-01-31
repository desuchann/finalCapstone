'''
Task 48 - Final project - Databases
Desc: Create a program that can be used by a bookstore clerk.
'''

import sqlite3
from tabulate import tabulate


def restore_bookstore():
    ''' Put the db back to the original state. '''

    data = [
        ('3001', 'A Tale of Two Cities', 'Charles Dickens', 30),
        ('3002', 'The Lord of The Rings', 'J.R.R. Tolkein', 37),
        ('3003', 'Flatland', 'Edwin A. Abbott', 314),
        ('3004', 'Black Ivy', 'Jason Jules', 0),
        ('3005', 'We', 'Yevgeny Zamyatin', 1984),
    ]
    c.executemany(
        '''INSERT INTO book_store VALUES (?,?,?,?)''', data)
    db.commit()


try:
    # set up the db and table
    db = sqlite3.connect('the_highstreet')
    c = db.cursor()
    try:
        c.execute('''CREATE TABLE book_store (
            id char PRIMARY KEY,
            title varchar,
            author varchar,
            qty int
        )''')
        restore_bookstore()
    except sqlite3.OperationalError:
        # table already exists
        pass

    def _update_or_delete(typ):

        # choose the entry by the primary key
        print('Do you have the id? If not, enter no and return to the main menu to search the database.')
        id = input('Otherwise, provide the id: ')
        if id == 'no':
            print('Returning to main menu...')
            return
        elif not id.isnumeric():
            print('That\'s not an id. Returning to main menu anyway...')
            return
        else:
            # check if the provided id is in the table
            c.execute('''SELECT * from book_store WHERE id = ?''', (id,))
            res = [row for row in c]
            if res:
                # delete an entry
                if typ == 'delete':
                    c.execute(
                        '''DELETE FROM book_store WHERE id = ?''', (id,))
                # update an entry
                elif typ == 'update':
                    # run through each option for updating
                    for col in ['title', 'author', 'qty']:
                        choice = input(
                            'Do you want to update the %s? yes or no: ' % col).lower()
                        if choice == 'no':
                            continue  # move to the next option
                        elif choice == 'yes':
                            change = input('Please enter the new value: ')
                            if col == 'title':
                                c.execute(
                                    '''UPDATE book_store SET title = ? WHERE id = ?''', (change, id))
                            elif col == 'author':
                                c.execute(
                                    '''UPDATE book_store SET author = ? WHERE id = ?''', (change, id))
                            elif col == 'qty':
                                c.execute(
                                    '''UPDATE book_store SET qty = ? WHERE id = ?''', (change, id))
                            else:
                                choice = input(
                                    'That\'s not one of the options. Try again pls: ')
                db.commit()
                print('Book successfully updated.')
            else:
                print('No entry matching that id. Exiting to main menu...')
                return

    while True:

        # present the menu to the user
        menu = input('''\nPlease select one of the following options:

                        1 - Enter a book
                        2 - Update a book
                        3 - Delete a book
                        4 - Search books
                        5 - View all books
                        6 - Restore the store
                        0 - Exit

                        : ''')

        # === add a new book ===#
        if menu == '1':
            title = input('What\'s the name of the book?: ')
            author = input('Who wrote the book?: ')

            # check if we have the book in stock already
            c.execute('''SELECT title, author from book_store''')
            rows = [row for row in c]
            if any((title, author) == pair for pair in rows):
                print('This book is already in the book store!')
                continue
            else:
                # assign a unique id
                c.execute('''SELECT id from book_store''')
                ids = [id for x in c.fetchall() for id in x]
                for x in range(3001, 100000):
                    x = str(x)
                    if x not in ids:
                        id = x
                        break
                # update the table
                qty = int(input('How many of this book do you have?: '))
                c.execute('''INSERT INTO book_store VALUES (?,?,?,?)''',
                          (id, title, author, qty))
                db.commit()
                print('Book successfully added.')

        # === update an exising book entry ===#
        elif menu == '2':
            _update_or_delete('update')

        # === delete a book entry ===#
        elif menu == '3':
            _update_or_delete('delete')

        # === search the database ===#
        elif menu == '4':
            point = input(
                'Input anything and every entry matching it will be returned: ')
            c.execute(
                """SELECT * from book_store WHERE id LIKE ? OR title LIKE ? OR author LIKE ? OR qty LIKE ?""", (point, point, point, point))
            print('\n', tabulate([row for row in c], headers=[
                  'id', 'Title', 'Author', 'Qty']))  # return the output ina nice table

        # === view the database ===#
        elif menu == '5':
            c.execute('''SELECT * from book_store''')
            print(tabulate([row for row in c], headers=[
                  'id', 'Title', 'Author', 'Qty']))  # return the output ina nice table

        # === restore the database ===#
        elif menu == '6':
            choice = input('Are you sure? yes or no: ').lower()
            if choice == 'yes':
                c.execute(
                    '''DELETE from book_store''')  # delete all data from the table
                restore_bookstore()
                print('The book store is back as it was.')
            else:
                print('Not a resounding yes. Returning to main menu...')

        # === a hasty exit ===#
        elif menu == '0':
            print('The store is now closed.')
            exit()

        else:
            print('That\'s not one of the options...')

finally:
    db.close()
