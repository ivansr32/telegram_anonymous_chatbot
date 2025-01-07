import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                sender TEXT,
                message TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id INTEGER PRIMARY KEY
            )
        """)
        self.conn.commit()

    def save_message(self, user_id, sender, message):
        self.cursor.execute("""
            INSERT INTO messages (user_id, sender, message)
            VALUES (?, ?, ?)
        """, (user_id, sender, message))
        self.conn.commit()

    def register_agent(self, agent_id):
        self.cursor.execute("""
            INSERT OR IGNORE INTO agents (agent_id)
            VALUES (?)
        """, (agent_id,))
        self.conn.commit()

    def get_agents(self):
        self.cursor.execute("SELECT agent_id FROM agents")
        return [row[0] for row in self.cursor.fetchall()]

    def get_assigned_user(self, agent_id):
        self.cursor.execute("""
            SELECT user_id FROM messages WHERE sender='user'
            LIMIT 1
        """)
        result = self.cursor.fetchone()
        return result[0] if result else None
