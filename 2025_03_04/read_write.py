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


def createEmail(email: Email):
    id = createID()
    connection.execute(f"""
        INSERT INTO email (id, mailbox, sender, subject, body, timestamp)
        VALUES ({id}, {email.mailbox}, {email.sender}, "{email.subject}", "{email.body}", {email.timestamp});
        """)
    connection.commit()
    return id


def deleteEmail(emailID):
    connection.execute(f"DELETE FROM email WHERE id = {emailID};")
    connection.commit()


def listEmails(mailboxID):
    result = {}
    for (id, mailbox, sender, subject, body, timestamp) in connection.execute(f"SELECT * FROM email WHERE mailbox = {mailboxID} ORDER BY timestamp DESC;").fetchall():
        result[id] = Email(mailbox, sender, subject, body, timestamp)
    return result





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

id = createEmail(Email(7, 12, "Phishing", "Click this link immediately to avoid bankruptcy!", 1766602850))
print("ID der neu erstellten EMail:", id)
deleteEmail(52)
print("Inbox content:")
for id, email in listEmails(7).items():
    print(id, email.mailbox, email.sender, email.subject, email.body, email.timestamp)
