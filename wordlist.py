# a class WordList to store a list of learning words in a database

import sqlite3
from datetime import datetime

class WordList:
    def __init__(self, db_name="language_learning.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()
        self.table_name = 'words'

    def _create_table(self,name='words'):
        self.table_name = name
        query = f""" 
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            translation2 TEXT NOT NULL,
            notes TEXT,
            times_seen INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            score REAL DEFAULT 0.0,
            correct_log TEXT DEFAULT "",
            date_added TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(query)
        self.conn.commit()
    def add_word(self, word, translation, translation2='', notes=None):
        # check if the word is already in the list
        query = f"""
        SELECT id, word, translation 
        FROM {self.table_name} 
        WHERE word = ?;
        """
        self.cursor.execute(query, (word,))
        result =  self.cursor.fetchall()
        if len(result) == 0:
            query = f""" 
            INSERT INTO {self.table_name} (word, translation, translation2, notes) 
            VALUES (?, ?, ?, ?);
            """
            self.cursor.execute(query, (word, translation, translation2, notes))
            self.conn.commit()
        else:
            print(f"This word: {word} is already in the list.")
    def add_word_input(self):
        word = input("Word in dutch:")
        translation = input("Translation in english:")
        translation2 = input("Translation in russian:")
        self.add_word(word, translation, translation2)
        
    def get_all_words(self):
        self.cursor.execute(f"SELECT id, word, translation, translation2, score FROM {self.table_name};")
        items = self.cursor.fetchall()
        data = []
        n = len(items)
        for i in range(n):
            word_dict = {"id":items[i][0],
                         "word":items[i][1],
                         "translation":items[i][2],
                         "translation2":items[i][3],
                         "score":items[i][4]}
            data.append(word_dict) 
        return data
    
    def delete_word(self, word_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?;", (word_id,))
        self.conn.commit()

    def empty_the_list(self):
        full_list = self.get_all_words()
        for i, item in enumerate(full_list):
            self.delete_word(item[0])
        
    
    def search_word(self, keyword):
        query = f"""
        SELECT id, word, translation, translation2
        FROM {self.table_name} 
        WHERE word LIKE ? OR translation LIKE ? OR translation2 LIKE ?;
        """
        self.cursor.execute(query, (keyword, keyword, keyword))
        return self.cursor.fetchall()
    
    def ingest_list(self, words_list):
        for item in words_list:
            self.add_word(item[0],item[1],item[2])
