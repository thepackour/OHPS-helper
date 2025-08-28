from main.db.database import *


class QuitWhilePrompting(Exception):
    pass

class NoSuchData(Exception):
    pass


@with_connection
def add_level_clear(cursor, user_id, level_id):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :user_id)''', user_id)
    if cursor.fetchone()[0] is None: raise NoSuchUser()

    cursor.execute('''SELECT EXISTS (SELECT * FROM levels WHERE id = :level_id)''', level_id)
    if cursor.fetchone()[0] is None: raise NoSuchLevel()

    cursor.execute("INSERT INTO level_clears(user_id, level_id) VALUES (:user_id, :level_id)",
                   {"user_id": user_id, "level_id": level_id})
    console_log(f"Successfully added level_clear (user_id: {user_id}, level_id: {level_id})")

@with_connection
def add_quest_clear(cursor, user_id, quest_id):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :user_id)''', user_id)
    if cursor.fetchone()[0] is None: raise NoSuchUser()

    cursor.execute('''SELECT EXISTS (SELECT * FROM quests WHERE id = :quest_id)''', quest_id)
    if cursor.fetchone()[0] is None: raise NoSuchQuest()

    cursor.execute("INSERT INTO level_clears(user_id, quest_id) VALUES (:user_id, :quest_id)",
                   {"user_id": user_id, "quest_id": quest_id})
    console_log(f"Successfully added quest_clear (user_id: {user_id}, level_id: {quest_id})")

@with_connection
def harddeleteuser(cursor, id):
    cursor.execute('''SELECT EXISTS (SELECT * FROM users WHERE id = :id)''', id)
    if cursor.fetchone()[0]:
        cursor.execute("DELETE FROM users WHERE id = :id", {"id": id})
        console_log(f"Successfully hard-deleted an existing user with id: {id}")
    else:
        raise NoSuchUser()

@with_connection
def harddeletelevelclear(cursor, id):
    cursor.execute('''SELECT * FROM level_clears WHERE id = :id''', id)
    res = cursor.fetchone()[0]
    if res is not None:
        user_id = res.user_id
        level_id = res.level_id
        cursor.execute("DELETE FROM level_clears WHERE id = :id", {"id": id})
        console_log(f"Successfully hard-deleted a level_clear (user_id: {user_id}, level_id: {level_id})")
    else:
        raise NoSuchData()

@with_connection
def harddeletequestclear(cursor, id):
    cursor.execute('''SELECT * FROM quest_clears WHERE id = :id''', id)
    res = cursor.fetchone()[0]
    if res is not None:
        user_id = res.user_id
        quest_id = res.quest_id
        cursor.execute("DELETE FROM quest_clears WHERE id = :id", {"id": id})
        console_log(f"Successfully hard-deleted a quest_clear (user_id: {user_id}, level_id: {quest_id})")
    else:
        raise NoSuchData()

def prompt(param):
    s = input(param + f' ("wq" to quit) : ')
    if s == 'wq': raise QuitWhilePrompting()
    return s

def users():
    while True:
        print("---------- /users/ ---------- \n")
        print("1. add_user \n")
        print("2. add_details \n")
        print("3. delete_user \n")
        print("4. hard-delete_user \n")
        print("0. exit \n")

        cmd = input("> ")

        if cmd == 0:
            break
        elif cmd == 1:
            print("---------- /users/add_user ---------- \n")
            try:
                user_id = prompt("id")
                user_username = prompt("username")

                add_user({'id': user_id, 'username': user_username})

            except QuitWhilePrompting:
                print('Exit the process... \n')

        elif cmd == 2:
            print("---------- /users/add_details ---------- \n")
            try:
                id = prompt("id")
                main_hand = prompt("main hand")
                number_of_keys = prompt("number of keys")
                multi_input_direction = prompt("multiple input direction")
                details = prompt("details")

                details_dict = {
                    'main_hand': main_hand,
                    'number_of_keys': number_of_keys,
                    'multi_input_direction': multi_input_direction,
                    'details': details
                }
                add_details(id, details_dict)

            except QuitWhilePrompting:
                print('Exit the process... \n')

        elif cmd == 3:
            print("---------- /users/delete_user ---------- \n")
            try:
                user_id = prompt("id")

                delete_user(user_id)

            except QuitWhilePrompting:
                print('Exit the process... \n')

        elif cmd == 4:
            print("---------- /users/hard-delete_user ---------- \n")
            try:
                user_id = prompt("id")

                user = find_user({'id': user_id})
                if user is None:
                    print("No such user \n")
                    raise QuitWhilePrompting()
                else:
                    for key, value in user.items():
                        print(f"{key}: {value} \n")

                while (True):
                    confirmation = input("Are you sure? (y/n): ")
                    if confirmation == 'y':
                        harddeleteuser(user_id)
                    elif confirmation == 'n':
                        raise QuitWhilePrompting()

            except QuitWhilePrompting:
                print('Exit the process... \n')

def clears():
    while True:
        print("---------- /clears/ ---------- \n")
        print("1. add_level_clear \n")
        print("2. add_quest_clear \n")
        print("3. hard-delete_level_clear \n")
        print("4. hard-delete_quest_clear \n")
        print("0. exit")

        cmd = input("> ")

        if cmd == 0:
            break
        elif cmd == 1:
            print("---------- /clears/add_level_clear ---------- \n")
            try:
                user_id = prompt("user_id")
                level_id = prompt("level_id")

                add_level_clear({'user_id': user_id, 'level_id': level_id})

            except QuitWhilePrompting:
                print('Exit the process... \n')
            except NoSuchLevel:
                print('No such level \n')
            except NoSuchUser:
                print('No such user \n')

        elif cmd == 2:
            print("---------- /clears/add_quest_clear ---------- \n")
            try:
                user_id = prompt("user_id")
                quest_id = prompt("quest_id")

                add_quest_clear({'user_id': user_id, 'level_id': quest_id})

            except QuitWhilePrompting:
                print('Exit the process... \n')
            except NoSuchLevel:
                print('No such level \n')
            except NoSuchUser:
                print('No such user \n')

        elif cmd == 3:
            print("---------- /clears/hard-delete_level_clear ---------- \n")
            try:
                id = prompt("id")

                while (True):
                    confirmation = input("Are you sure? (y/n): ")
                    if confirmation == 'y':
                        harddeletelevelclear(id)
                    elif confirmation == 'n':
                        raise QuitWhilePrompting()

            except QuitWhilePrompting:
                print('Exit the process...')
        elif cmd == 4:
            print("---------- /clears/hard-delete_quest_clear ---------- \n")
            try:
                id = prompt("id")

                while (True):
                    confirmation = input("Are you sure? (y/n): ")
                    if confirmation == 'y':
                        harddeletequestclear(id)
                    elif confirmation == 'n':
                        raise QuitWhilePrompting()

            except QuitWhilePrompting:
                print('Exit the process...')

def levels():
    pass

def quests():
    pass

def main():
    while True:
        print("---------- / ---------- \n")
        print("1. users \n")
        print("2. clears \n")
        print("3. levels \n")
        print("4. quests \n")
        print("0. exit \n")

        cmd = input("> ")

        if cmd == 0: break
        elif cmd == 1: users()
        elif cmd == 2: clears()
        elif cmd == 3: levels()
        elif cmd == 4: quests()

main()
