-Server used and secure

-Guests can't visit the website without creating an account. Only login/register page will be accessible.

-Members have accounts and restricted areas accessible only by them    (myblog, private journal, account pages)

-Database in use and securely deployed (python flask SQLite alchemy),   passwords are stored securely and hashed/encrypted using bcrypt module.

-Blogs and journals can be maintained and updated (owners of blogs and  journals can update titles and content and also the file attached,  members can also delete their posts/journals)

-Media can be utilised (members can attach video/image/audio files to their posts/journals and also can update their avatars).

-Validation checks and basic security (passwords/logins require specific length, posts can be edited only by their owners, forgot email function requires registered email, can't access other user's pages etc.

-Advanced security - Fernet encryption used to store posts   and journals securely in the database ( titles and content encrypted, date posted not encrypted to easier locate posts/journals ).

-member public functionality - registers users can view home page which displays all users blog posts , users can download files uploaded by other users or share their files with everyone, users can also view other users profiles to see all their blog posts.

-Member private functionality -registered users can access theirs myblog/private journal/account pages ,upload posts and journals and attach files to them, view other users profiles, download shared files, request password recovery, upload avatars etc.

-Logs, stats and user security functions - logs are stored in a database every time user logins; ip address and location (country) are saved to the database. I let to run the app my friend in UK and a friend from Pakistan, both ip addresses and countries were collected successfully, I also tried running app on a different device it gave me different IP output successfully. For user security function I created the function to reset user's password using email verification link.



Home page: localhost:5000/home

app secret key = "5791628bb0b13ce0c676dfde280ba245"

smtp used for "Forgot password" function = smtp.googlemail.com
sample gmail account create for this function = flaskismine@gmail.com

Main Technologies used: Python, Python Flask, SQLALCHEMY sqlite, html + support languages and bootstrap.

Fernet (https://cryptography.io/en/latest/fernet/) module was used for encryption.


Bootstrap used in the project.
source: https://getbootstrap.com/docs/4.2/components

