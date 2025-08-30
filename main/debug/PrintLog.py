import datetime
import inspect
import os
import sqlite3


def log(message: str, result = None, e: Exception = None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    frame = inspect.stack()[1]
    filename = os.path.basename(frame.filename)
    function_name = frame.function
    print(f"\n[Log Info] ({now})" + ("-" * 50))
    print(f"< {filename}:{frame.lineno} | {function_name} > {message}")
    if e is not None:
        print("- Exception Info:" + str(e))
    print(f"- Returns:")
    _unpack_print(result)


def log_w(func_name, args, kwargs, result = None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caller = inspect.stack()[2]
    print(f"\n[Log Info | with_connection] ({now})" + ("-" * 50))
    if result is not None and type(result) is Exception:
        print(f"[!] EXCEPTION INFO : {result}")
    print(f"Called from {caller.function} in {caller.filename}:{caller.lineno}")
    print(f"Executing {func_name} with args={args}, kwargs={kwargs}")
    print(f"Returned:")
    _unpack_print(result)

def _unpack_print(data):
    if type(data) is Exception:
        print(f"Exception :{data}\n")
    else:
        try:
            iter(data)
            # str, list, tuple, dict(key 반복), set, range, ...
            if type(data) is str:
                print(f"{type(data)} : {data}\n")
            elif type(data) is dict:
                for key, value in data.items():
                    print(f"\t{key} : {value}")
            elif type(data) is sqlite3.Row:
                data = dict(data)
                for key, value in data.items():
                    print(f"\t{key} : {value}")
                print(" ")
            else:
                for _ in data:
                    _unpack_print(_)
        except TypeError: # int, float, bool, NoneType
            print(f"{type(data)} : {data}\n")