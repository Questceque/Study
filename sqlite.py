import sqlite3
from typing import List, Tuple

db_path = "/content/example.sqlite"

def get_president_by_name(name: str) -> Tuple:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM presidents WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result

def add_president(name: str, age: int, country: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presidents (name, age, country) VALUES (?, ?, ?)", (name, age, country))
    conn.commit()
    conn.close()

def update_president_age(name: str, new_age: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE presidents SET age = ? WHERE name = ?", (new_age, name))
    conn.commit()
    conn.close()

def delete_president(name: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM presidents WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_all_books() -> List[Tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    conn.close()
    return result

def add_book(name: str, author: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (name, author) VALUES (?, ?)", (name, author))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Данные о президенте President1:", get_president_by_name("President1"))
    add_president("President2", 29, "USSR")
    update_president_age("President2", 32)
    delete_president("President1")
    print("Список всех книг:", get_all_books())
    add_book("Book of all studies", "Gerodot")
