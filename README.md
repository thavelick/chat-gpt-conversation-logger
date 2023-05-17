# ChatGPT Conversation Logger

This project allows you to intercept and log OpenAI's ChatGPT conversation data and messages. The logged data is stored in an SQLite database. The project uses a JavaScript snippet for the client side, which intercepts fetch requests from the browser. It also includes a Python server to receive the intercepted data and store it in the database.

## Files in the Project

1. `client.js`: A JavaScript file which is used to intercept the fetch requests in the browser. If the request is sent to the ChatGPT backend API, it sends the conversation data to the Python server.

2. `create_tables.py`: A Python script to create the SQLite database and the necessary tables to store the data.

3. `server.py`: A Python HTTP server to receive the data from the client side and store it in the SQLite database.

## Setup

1. First, ensure you have both Python and SQLite installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the project folder in your terminal and run the `create_tables.py` script to setup the SQLite database:

```bash
python3 create_tables.py
```

4. Run the Python server:

```bash
python3 server.py
```

5. Open the developer tools in your browser and paste the contents of `client.js` into the console. This script will intercept the fetch requests from the browser.

## Usage

Once everything is set up, use ChatGPT as you normally would. The client script will intercept the fetch requests to the backend API and send the data to the Python server, which will store it in the SQLite database. 

You can check the logged data by querying the SQLite database. The data is stored in two tables: `chatgpt_conversation` and `chatgpt_message`. The `chatgpt_conversation` table stores data about each conversation, and the `chatgpt_message` table stores data about each message in the conversations.

## Credit

Inspiration and a bunch of code for this project came from: [A post from Simon Willison](https://simonwillison.net/2023/Mar/27/ai-enhanced-development/).
Lots of code and much of this README was written with the assistance of, you guessed it, ChatGPT.

## Note

Please make sure to use this responsibly and respect all privacy considerations. This script logs all conversations and messages sent from your browser to the ChatGPT backend API, including potentially sensitive data.

This project is for educational and research purposes only. It is not officially associated with or endorsed by OpenAI. Use at your own risk.

