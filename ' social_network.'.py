import sqlite3
from faker import Faker
from datetime import datetime
import pandas as pd

# Function to create and populate the database
def create_and_populate_database():
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()

    # Create the people table
    create_ppl_tbl_query = """
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        province TEXT NOT NULL,
        bio TEXT,
        age INTEGER,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    );
    """
    cur.execute(create_ppl_tbl_query)

    # Instantiate Faker for generating fake data
    fake = Faker("en_CA")

    # Insert 200 fake people into the people table
    for _ in range(200):
        new_person = (
            fake.name(),
            fake.email(),
            fake.address(),
            fake.city(),
            fake.administrative_unit(),
            fake.text(max_nb_chars=200),
            fake.random_int(min=1, max=100),
            datetime.now(),
            datetime.now()
        )
        add_person_query = """
        INSERT INTO people (
            name, email, address, city, province, bio, age, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(add_person_query, new_person)

    con.commit()
    con.close()

# Function to query the database for old people and save the results to a CSV file
def query_and_save_old_people():
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()

    # Query the database for people who are at least 50 years old
    query = "SELECT name, age FROM people WHERE age >= 50"
    cur.execute(query)
    old_people = cur.fetchall()

    # Print the name and age of each person in the query result within a sentence
    for person in old_people:
        print(f"{person[0]} is {person[1]} years old.")

    # Save the names and ages of all old people to a CSV file
    df = pd.DataFrame(old_people, columns=['Name', 'Age'])
    df.to_csv('old_people.csv', index=False)

    con.close()

# Main function to run the script
def main():
    create_and_populate_database()
    query_and_save_old_people()

if __name__ == "__main__":
    main()
