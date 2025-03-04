from datetime import datetime
import time
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


class Email:
    def __init__(self, mailbox, sender, subject, body, timestamp):
        self.mailbox = mailbox
        self.sender = sender
        self.subject = subject
        self.body = body
        self.timestamp = timestamp


freeID = 1000
def createID():
    global freeID
    id = freeID
    freeID += 1
    return id


def listEmails(mailbox_name: str):
    query = f"""
    SELECT email.id, mailbox.name, contact.name, subject, body, timestamp FROM
    (email INNER JOIN mailbox ON email.mailbox = mailbox.id)
    INNER JOIN contact ON email.sender = contact.id WHERE mailbox.name = '{mailbox_name}' ORDER BY timestamp DESC
    """

    result = {}
    for (id, mailbox, sender, subject, body, timestamp) in connection.execute(query).fetchall():
        localtime = datetime.fromtimestamp(timestamp)
        result[id] = Email(mailbox, sender, subject, body, localtime.strftime('%d.%m.%Y - %H:%M:%S'))
    return result


def createEmail(email):
    id = createID()
    query = f"""
            INSERT INTO email (id, mailbox, sender, subject, body, timestamp)
            VALUES (
                {id},
                (SELECT id FROM mailbox WHERE name = '{email.mailbox}'),
                (SELECT id FROM contact WHERE name = '{email.sender}'),
                "{email.subject}",
                "{email.body}",
                {int(time.mktime(time.strptime(email.timestamp, "%d.%m.%Y - %H:%M:%S")))});
            """
    connection.execute(query)
    connection.commit()
    return id


connection.execute("""insert into mailbox (id, name) values (7, "Inbox");""")
connection.execute("""insert into mailbox (id, name) values (8, "Studium");""")
connection.execute("""insert into contact (id, address, name) values (11, "a@example.com", "Alice");""")
connection.execute("""insert into contact (id, address, name) values (13, "c@example.com", "Charlie");""")
connection.execute("""insert into contact (id, address, name) values (12, "b@example.com", "Bob");""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (50, 7, 12, "Hallo!", "Hi, wie geht es Dir?", 1766602800);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (51, 7, 12, "Re: Re: Hallo!", "Bei mir auch alles gut.", 1766602860);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (52, 8, 11, "Mensa", "Hunger???", 1766599200);""")
connection.execute("""insert into email (id, mailbox, sender, subject, body, timestamp) values (53, 8, 13, "Projekt", "Können wir am Mittwoch über das Projekt sprechen?", 1766602980);""")
connection.commit()

id = createEmail(Email("Inbox", "Alice", "Phishing", "Click this link immediately to avoid bankruptcy!", "24.12.2025 - 20:00:50"))
print("ID der neu erstellten EMail:", id)
print("Inbox content:")
for id, email in listEmails("Inbox").items():
    print(id, email.mailbox, email.sender, email.subject, email.body, email.timestamp)
