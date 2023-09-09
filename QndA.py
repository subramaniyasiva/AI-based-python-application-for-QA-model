import sqlite3 as sq3
from transformers import pipeline, DistilBertTokenizer
from fuzzywuzzy import fuzz

# Connect to the SQLite database
con = sq3.connect("qa.db")
cur = con.cursor()
5
# Create the table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS STEMPI(
        ID INT NOT NULL,
        QUESTION TEXTNOT NULL,
        ANSWER TEXT NOT NULL)
    ''')

# Insert sample data
cur.execute("INSERT INTO STEMPI (ID, QUESTION, ANSWER) VALUES (?, ?, ?)",
            (1, "What is the birth date of Mahatma Gandhi?", "OCT 2 1869"))
cur.execute("INSERT INTO STEMPI (ID, QUESTION, ANSWER) VALUES (?, ?, ?)",
            (2, "When did Sundar Pichai become CEO of Alphabet?", "In the year 2019"))
cur.execute("INSERT INTO STEMPI (ID, QUESTION, ANSWER) VALUES (?, ?, ?)",
            (3, "When did India become independent?", "In the year 1947"))

print("Values inserted")

# Load the pre-trained question-answering model from Transformers
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")

while True:
    user_input = input("Ask your question (type 'exit' to quit): ")
    
    if user_input.lower() == "exit":
        print("***SESSION OVER***")
        break

    best_score = 0
    best_answer = None

    for stored_question in cur.execute("SELECT QUESTION, ANSWER FROM STEMPI"):
        db_question, db_answer = stored_question
        similarity_score = fuzz.ratio(user_input.lower(), db_question.lower())
        
        if similarity_score > best_score:
            best_score = similarity_score
            best_answer = db_answer

    if best_answer:
        print("Answer:", best_answer)
    else:
        print("No data found.")

con.commit()
con.close()
