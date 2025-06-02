Telegram parser from one channel, translate and write a post to another choosen channel.

To make it work you'd create telegram app, use active user account (NOT bot), subscribe that user to scrap channel and make him admin at target channel.

Features: 
- Message scrapping;
- Media scrapping;
- Post message and media as one post;
- Links positioning at message correctly if message is without translation;

In progress:
- Translation using LLM API;
- Links positioning correctly after translation;
- Quoted part of the message should be quoted at translated message;
