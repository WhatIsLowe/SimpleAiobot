## SimpleAiobot

This project is a Telegram bot that allows users to subscribe or unsubscribe to notifications from a "spider". The bot uses an asynchronous approach and works with an SQLite database to store information about subscribers, their chat id's.

## Installation

1. Clone the repository to your computer.
2. Install the required dependencies using the command `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project and add the following environment variables:
```
BOT_TOKENT=YOUR_TOKEN
```
where `YOUR_TOKEN` is the token of your Telegram bot.

## Usage

1. Run the bot using the command `python main.py`.
2. Open a chat with your bot in Telegram and send it the `/subscribe` command.
3. The bot will send you a message with a button to subscribe or unsubscribe to notifications from the "spider".
4. Click on the button to subscribe or unsubscribe.

## License

This project is distributed under the MIT license. See the `LICENSE` file for more information.
