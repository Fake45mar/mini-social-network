# mini-social-network

I know that every key, every config, every private information is excess(db too) in git repository, also about another rep with license and etc.
Everything here has been done to show my skills, show my abilities with django, with jwt, with writing and testing RestApi.

To start this project you need python at least 3.8.
You must run following command:
pip install requirements.txt
Next step is run django by python manage.py runserver 127.0.0.1:8000
After that you can test this project by manual requesting in console or you can use a bot.
Bot is located in folder bot_tester. You should correct config file to your wish, after that you can see magic.
If you want to clear db, you have to run following sequence:
DELETE FROM liked_post;
DELETE FROM post;
DELETE FROM user;
