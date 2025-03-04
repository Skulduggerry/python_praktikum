import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute(f"""
CREATE TABLE poll (
    id int primary key,
    title text
);
""")
connection.execute(f"""
CREATE TABLE option (
    id int primary key,
    name text,
    pollId int
);
""")
connection.execute(f"""
CREATE TABLE participant (
    id int primary key,
    name text
);
""")
connection.execute(f"""
CREATE TABLE answer (
    optionId int,
    participantId int,
    value text,
    primary key (optionId, participantId)
);
""")
connection.commit()

freeID = 1000
def createID():
    global freeID
    id = freeID
    freeID += 1
    return id

def listPolls():
    polls = {}
    for id, title in connection.execute("SELECT * FROM poll").fetchall():
        polls[id] = title
    return polls

def createPoll(title, options):
    pollId = createID()
    connection.execute(f"INSERT INTO poll (id, title) VALUES ({pollId}, '{title}')")
    for option in options:
        optionId = createID()
        connection.execute(f"INSERT INTO option (id, name, pollId) VALUES ({optionId}, '{option}', {pollId})")
    return pollId

def fillPoll(poll_id: int, participant: str, answers: list):
    options_cursor = connection.execute(f"SELECT id, pollId from option where pollID = {poll_id}")
    rows = connection.execute(f"""
    SELECT option.id, answer.participantId FROM
     participant JOIN answer ON participant.id = answer.participantId
     JOIN option ON answer.optionID = option.id
     WHERE participant.name = '{participant}' and option.pollId = {poll_id}
    """).fetchall()
    if len(rows) == 0:
        # new participant
        p_id = createID()
        connection.execute(f"INSERT INTO participant (id, name) VALUES ({p_id}, '{participant}')")
        for row, answer in zip(options_cursor, answers):
            o_id = row[0]
            connection.execute(f"INSERT INTO answer (optionId, participantId, value) VALUES ({o_id}, {p_id}, '{answer}')")
    else:
        # existing participant
        for row, answer in zip(rows, answers):
            o_id = row[0]
            p_id = row[1]
            connection.execute(f"UPDATE answer SET value = '{answer}' WHERE optionId = {o_id} AND participantId = {p_id}")
    connection.commit()

def pollStatus(poll_id):
    poll_cursor = connection.execute(f"SELECT title FROM poll WHERE id = {id}")
    for row in poll_cursor:
        title = row[0]

    options_cursor = connection.execute(f"SELECT id, name from option where pollId = {poll_id} ORDER BY id")
    options = []
    for row in options_cursor:
        options.append(row[1])

    participants = []
    answers = []
    participant_cursor = connection.execute(f"SELECT DISTINCT participant.id, participant.name FROM participant JOIN answer ON participant.id = answer.participantId JOIN option ON answer.optionId = option.id")
    for row in participant_cursor:
        p_id = row[0]
        name = row[1]
        participants.append(name)
        a = []
        answer_cursor = connection.execute(f"SELECT optionID, value FROM answer JOIN option ON answer.optionID = option.id WHERE participantId = {p_id} and pollID = {id} ORDER BY optionId")
        for a_row in answer_cursor:
            a.append(a_row[1])
        answers.append(a)

    return (title, options, participants, answers)


id = createPoll("Schokolade", ["Nuss", "Alpenmilch", "Kaffee Sahne"])
fillPoll(id, "Kasper", ["ja", "ja", "nein"])
print(pollStatus(id))
fillPoll(id, "Seppel", ["nein", "ja", "ja"])
print(pollStatus(id))
fillPoll(id, "Kasper", ["ja", "nein", "ja"])
print(pollStatus(id))


