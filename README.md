# movie-club-engage-new

## video demo url: - https://drive.google.com/file/d/1A3my5dSVmF8NvCp7KsrkWKEE_OdF70_A/view?usp=sharing

requirements: - 
1. Visual Studio Code/ pycharm
2. Xampp(phpMyAdmin)
3. MySQL
4. visual studio c++ updated version(more than 14.0)
5. need to install surprise package successfully.
<br />

Steps to Clone repository : - <br />
1. Open Visual Studio and go to terminal and clone this repository.You can use this command " git clone https://github.com/premsagarkushwaha/movie-club-engage-new.git".
2. now open cloned project in vs code.(folder name should be movie-club-engage-new)
3. Go to Xampp(phpMyadmin) and create new database and name it as "newmed".<br />
3.1 note: - You Need xampp mysql server for xampp databse connection with app that  can be done by two way<br />
3.2 first way :- if you have already using xampp mysql then create database on your phpMyadmin  and update ip address and port number on of databse on app.py file of the project.<br />
you can find your phpmyadmin ip and port on admin dashboard. below is screenshot.<br />
![alt text](https://raw.githubusercontent.com/premsagarkushwaha/Greenwindow/main/ipport.png?token=GHSAT0AAAAAABUN4BWKIB57UEAXR6G7PUL6YUY6DKQ)<br />
3.3 second way : - or create mysql connection on ip address 127.0.0.2 and use port 3307 and then go to phpMyadmin and create database.
you can see screenshot below:- <br />
![alt text](https://raw.githubusercontent.com/premsagarkushwaha/Greenwindow/main/dbu.png?token=GHSAT0AAAAAABUN4BWLHZZXDCRT3C2UTL6GYUY6I6A)<br />
4. now go to database and click on import then select newmwd.sql file which is in mysql folder of project-"movie-club-engage-new" that is cloned by you.
5. after successfully importing database and establishing connection(or updating ip address and port and making connection successfully) go to project terminal and install all required package and library. use command "pip install -r requirements.txt"
6. now run this project.
