# Data_Reconciliation_Tool
 
## Project Desciption:

-  A User friendly web based data reconciliation tool where user will be able to compare the data from two different dynamic sources.
- User can easily configure the sources by inserting the connection credentials of the sources.
- User can also use the tool to compare two local files like excel sheets with each other by giving path to those sheets to the tool and can get useful insights for further computation. 
- User can look up to the local history of previous comparisons and can perform the same comparison again and again, if required.


## Tech Stack:

<img src="https://drive.google.com/uc?export=view&id=1fbe3u4AWNAZGskB2DrdUqCTu6bs_ussh" alt="Tech Stack" width="500" />

## Dependancies 
~~~python:
  pip install flask
  pip install pymongo
  pip install pandas
  pip install dnspython
~~~

## Starting the App
~~~python
  git clone "https://github.com/SaurabhRKSAGAR/Data_Reconciliation_Tool.git"
  cd Data_Reconciliation_Tool/
  python main_logic.py
~~~

## Using the App
~~~python
  127.0.0.1:5000/api
~~~

## Configuring the sources
~~~python
  127.0.0.1:5000/api/config
~~~

## Future Enhancements
- Provide an option to the user for referencing the data using multiple sources namely SQL DB, Oracle DB or via APIs. 
- Incorporate data visualization tools including charts and figures for better analysis of comparison results.
- Include searching and sorting functionality for the history of comparison queries previously triggered by the user. 
