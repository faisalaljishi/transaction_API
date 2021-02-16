##Table of contents
* [Directory](#directory)
* [API Quickstart](#api-quickstart)
    * [Background](#background)
    * [List](#List)
    * [Create](#create)
    * [Deduct](#deduct) 
* [Task Description](#task-description)
* [General Design Info](#general-design-info)
* [Technologies](#technologies)
* [Demo](#demo)
* [Setup](#setup)
* [Admin](#admin)
* [Proof of Concept](#proof-of-concept)
* [About Me](#about-me)

####About and Directory
   This is a Django REST API built to manage a database

####API Quickstart
    
   #####Background:
   To quickly get started with this project visit this [link](http://127.0.0.1:8085/api/), 
   which links all the API requests possible. Reading the [Admin](#admin) section is also recommended to easily view any changes to the database.
   
   First, we have the All Fields link, which details all the data the database currently contains. Note that most of these are not meant to be modified by the API, the API should only list transactions, award a user points, or charge a user points.
   
   There are 3 main API calls: List, Detail and Filter. The first two support all models (User, Payer, Balance, Transaction and FundQueue) but Filter is restricted to models that can be filtered.
   
   Read the [Design Info](#general-design-info) section to learn more about the models.
   
   #####List:
   List is supported by all the models. List simply returns all objects in the database of that type.
   
   #####Detail:
   Detail is supported by all the models. Detail simply returns a given object in the database based on a primary key. You must know the primary key of the object you are trying to find.
   
   User's primary key is simply the name of that user.
   
   Payer's primary key is simply the name of that payer.
   
   Balance's primary key is the string "Payer, User" containing the names of each to find the balance of that user from that payer.
   
   Transaction's primary key is simply the ID number assigned to that transaction.
   
   FundQueue's primary key is simply the ID number assigned to that fundQueue.
   
   #####Filter:
   Filter is supported by (Balance, Transaction, FundQueue). Filter currently only supports filtering by User.
   
   If you pass a user into a Transaction Filter like so: transaction-filter/"User" (without quotations and with the name of the user), this will return all the Transactions that are recorded under that User.
   
   #####Create:
   Create makes a transaction adding points to user and updates all necessary values.
   
   To use create simply visit the page, and supply a JSON of this structure:
   
    {
        "user": "Joe Schmoe",
        "payer": "DANNON",
        "points": 300
    }
   
   This will create a transaction in the database, and update the user's total balance and the user's balance with that payer.
   
   If the user or payer do not exist,(or the user does not have a balance with that payer) they will be initialized. The transaction will then be written to the database, and the user's total balance and the user's payer balance will be initialized to the transaction amount.
   
   Note: Create only takes positive values. Negative values or zero are not permitted.
   
   #####Deduct:
   Deduct makes a transaction deducting points from user and updates all necessary values.
   
   To use deduct simply visit the page, and supply a JSON of this structure:
   
    {
        "user": "Joe Schmoe",
        "points": -200
    }
   
   This will deduct the points from the total balance of the user. It will spend the oldest points earned first, 
   and none of the user's payer balances will go negative.
   
   Note: Deduct only takes negative values. Positive values or zero are not permitted. The value also must equal or be less than the user's total balance. Submitting an invalid value or if the user is does not exist Deduct will return 400 Bad Request.

####Task Description
   Users only see a single balance in their account. These points come from certain payers. The accounting team wants to keep track of where the points are coming from and how they are being spent.
   Design a system that follows these constraints:
   * Oldest points are spent first
   * No payer's balance for a user should go negative.

####General Design Info
   The database stores 5 types. (User, Payer, Balance, Transaction and FundQueue)
   
   User stores all the names of users.
   
   Payer stores all the names of payers.
   
   Balance stores all the balances of users for a specific payer. 
   Each payer has a balance sheet, which contains all users who have transactions with that payer. This model is that balance sheet.
   
   Transaction stores a history of all transactions. Each transaction object has the user, payer, points, date and an ID.
   
   FundsQueue is simply a transaction clone that houses a queue of funds to be spent in order. The main difference is that FundsQueue objects can only contain positive points, (these are points to spend) and can be modified and deleted, but Transactions contains a history that cannot be modified and also records deducted points.
    
   Here is a diagram of the above models:
   
   ![pointAPI](./files/pointAPI.png)
   
   Django REST framework is accessed by utilizing serializers, which provides a convenient way to convert a model to a json
    which provides the frontend to display and test the backend without using a tool like Postman.
    
   Signals are also utilized to update the balances or create prerequisite objects by listening for when a Transaction is about to be created.
   
   The admin panel is mostly user generated, but is customized to include related objects.
    
####Demos
   
   When using the website in a browser, the below should be the first thing you see.
   
   Assuming that the database is empty. Most calls will return a 404 as there is nothing in the database to display.
   
   ![overview](./files/overview.png)
   
   
   Let us add a transaction to the database. Navigate to the create link near the bottom in the overview response. 
   We supply a json with a user, payer and points for the transaction. 
   
   ![jamie_1](./files/jamie_1.png)
    
   This is the response we get:
   
   ![jamie_response_1](./files/jamie_response_1.png)
   
   What happens under the hood? As we know out database was empty. Lets look at our new user's admin panel. The user and payer did not exist, and they got created. They are initialized to the transaction amount, as they gained that amount from that transaction. 
   
   ![jamie_admin_1](./files/jamie_admin_1.png)
   
   Let us another two transaction to the database. The responses are similar to before.
   
   ![jamie_2](./files/jamie_2.png)
   
   ![jamie_3](./files/jamie_3.png)
    
   The user now has 2000 points, 3 Transactions and FundQueues, 2 Payers and 2 Balances of 1000 for the first payer, and 1000 for the second. Lets look at the admin panel displaying this information:
   
   ![jamie_admin_2](./files/jamie_admin_2.png)
   
   Now, lets deduct from the user. We navigate to the deduct page from overview, and supply a json with the user and the points.
   
   ![jamie_4](./files/jamie_4.png)
    
   The response:
   
   ![jamie_response_4](./files/jamie_response_4.png)
   
   Looking at the admin page below, we notice that we took 600 from the first payer, and 400 from the second, rather than taking the entire 1000 from a single payer. This is because we want to spend the oldest points first. Also notice how the Transaction contains a history of what occurred, but FundQueue is now altered. We took the first FundQueue object, spent it entirely, then discarded it, as we can no longer spend it. Then we moved on to the second FundQueue object, took 400 out of it, and kept it, as it still has 600 points we can spend. Finally notice how the total balance is deducted by the amount.
   
   ![jamie_admin_3](./files/jamie_admin_3.png)
    
   Let us deduct by 1000 again:
   
   ![jamie_5](./files/jamie_5.png)
   
   Here is our admin page after this operation. What is notable here is that our FundQueue is empty, as we have no points to spend, and all balances are 0.
   
   ![jamie_admin_4](./files/jamie_admin_4.png)
   
####Technologies
   Project created with the following technologies:

    Python 3.7
    Django 3.1.6
    Django REST Framework 3.12.2

####Setup
   To setup this project, simply download the files, install the requirements and in the ./points/points/ directory, run the following command :
   
    python manage.py runserver
    
   Then navigate to http://127.0.0.1:8085/api/ on your web browser of your choice.

####Admin
   Django provides a wonderful admin panel that can display objects in the database. It also allows you to display all information and  other objects related to an object directly on that same page, in a nice GUI that is quickly generated along with any changes you make.
   
   If quickly trying to demo/try the project, and you have been given access to the admin panel, the recommended method is accessing the user which you are modifying which will provide a nice view of all the Payers, Balances, Transactions, and FundQueues. 
   
   Open a tab with the admin panel, another with the create and deduct links, and you can quickly view what is occurring under the hood after making an API call. 
   
   If you do not have access to the admin panel, it is recommended to setup your own instance or open the all fields link. The latter achieves the same result but is less concise and readable. 
   
   ![admin](./files/admin.png)

####About Me
   This was my first project in Django