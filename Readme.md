nuBank Challenge
================

Description
-----------

The first step to solve this challenge is prepare the data that will be in the tree, so the tree creation could be easier. So, I created the rules that will define who can be invited and created a objects list where each item will be an user and his data.
  
Based on this list, I created a tree to make easier the points definitions.

To enable HTTP access, I used the Flask Python package which is a light HTTP web server. 

How to run
----------

This project use Python 2.7 and depends on Flask package. It came with a python virtualenv where you can run it. In a linux evironment, you need to install python-pip and virtualenv before start:

    $ sudo apt-get install python-pip
   
With PIP installed, now you need to install virtualenv:

    $ sudo pip install virtualenv
   
Now, you can can activate the virtualenv from this project folder:

    $ source venv/bin/activate

Finally, to run the application type:
    
    $ python run.py
    
Open a web broser and go to the URL http://localhost:8081

In this folder has the input.txt file to use in this challenge.

Tests
-----

The unit tests are in tests folder. To run it, on a terminal, in the project folder and with the virtualenv activated type:
 
    $ nosetests
