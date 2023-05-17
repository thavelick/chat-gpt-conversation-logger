#!/usr/bin/python3
import sqlite3


def create_tables():
    conn = sqlite3.connect("chatgpt.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS chatgpt_conversation (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    create_time REAL,
                    moderation_results TEXT,
                    current_node TEXT,
                    plugin_ids TEXT
                )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS chatgpt_message (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT REFERENCES chatgpt_conversation(id),
                    author_role TEXT,
                    author_metadata TEXT,
                    create_time REAL,
                    content TEXT,
                    end_turn INTEGER,
                    weight REAL,
                    metadata TEXT,
                    recipient TEXT
                )"""
    )

    conn.commit()
    conn.close()


create_tables()
