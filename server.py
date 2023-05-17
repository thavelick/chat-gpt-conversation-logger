#!/usr/bin/python3

import json
import sqlite3

from http.server import BaseHTTPRequestHandler, HTTPServer


class ChatGPTRequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "https://chat.openai.com")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")



    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        raw_data = self.rfile.read(content_length)
        data = json.loads(raw_data)

        if "/insert" in self.path:
            table = self.path.split("/")[-3]
            print("table", table)
            if table == "chatgpt_conversation":
                self.insert_conversation(data)
            elif table == "chatgpt_message":
                self.insert_messages(data)

        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"status": "success"}
        self.wfile.write(json.dumps(response).encode())

    def insert_conversation(self, data):
        conn = sqlite3.connect("chatgpt.db")
        c = conn.cursor()

        row = data["row"]

        c.execute(
            """INSERT OR REPLACE INTO chatgpt_conversation
                      (id, title, create_time, moderation_results, current_node, plugin_ids)
                      VALUES (?, ?, ?, ?, ?, ?)""",
            (
                row["id"],
                row["title"],
                row["create_time"],
                row["moderation_results"],
                row["current_node"],
                row.get("plugin_ids"),
            ),
        )
        conn.commit()
        conn.close()

    def insert_messages(self, data):
        conn = sqlite3.connect("chatgpt.db")
        c = conn.cursor()

        for row in data["rows"]:
            if not row.get("create_time") and row.get("content") == "":
                print("skipping row as it has no useful content or time")
                continue

            c.execute(
                """INSERT OR REPLACE INTO chatgpt_message
                          (id, conversation_id, author_role, author_metadata, create_time, content,
                           end_turn, weight, metadata, recipient)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    row["id"],
                    row["conversation_id"],
                    row["author_role"],
                    row["author_metadata"],
                    row["create_time"],
                    row["content"],
                    row.get("end_turn", False),
                    row["weight"],
                    row["metadata"],
                    row["recipient"],
                ),
            )
        conn.commit()
        conn.close()


def run_server():
    server_address = ("localhost", 5000)
    httpd = HTTPServer(server_address, ChatGPTRequestHandler)
    print("Server started on http://localhost:5000")
    httpd.serve_forever()


run_server()
