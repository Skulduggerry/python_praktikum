import sqlite3
connection = sqlite3.connect(":memory:")

connection.execute("""
CREATE TABLE mailbox (
    id int primary key ,
    name text
);
""")
connection.execute("""
CREATE TABLE contact (
    id int primary key,
    address text,
    name text 
);
""")
connection.execute("""
CREATE TABLE email (
    id int primary key ,
    mailbox int,
    sender int,
    subject text,
    body text,
    timestamp int
);
""")
connection.commit()

#################
# TEST THE CODE #
#################
connection.execute("""insert into mailbox (id, name) values (7, "Inbox");""")
connection.execute("""insert into mailbox (id, name) values (8, "Studium");""")
connection.execute("""insert into contact (id, address, name) values (11, "a@example.com", "Alice");""")
connection.execute("""insert into contact (id, address, name) values (12, "b@example.com", "Bob");""")
connection.execute("""insert into contact (id, address, name) values (13, "c@example.com", "Charlie");""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (50, 7, 12, "Hallo!", "Hi, wie geht es Dir?", 1766602800);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (51, 7, 12, "Re: Re: Hallo!", "Bei mir auch alles gut.", 1766602860);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (52, 8, 11, "Mensa", "Hunger???", 1766599200);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (53, 8, 13, "Projekt", "Können wir am Mittwoch über das Projekt sprechen?", 1766602980);""")
connection.commit()
