# CarSamjho.com

# About The Project

The automobile industry is flooded with options, it is a dream for a middle-class family to buy a car, and with this incentive, the company is doing everything possible to give a smooth ride utilising analytics. As a result, I'm attempting to develop an analytical tool to provide Data-Analysis for User given Dataset for the automotive sector as per Manufacturing Industry Employees as a user to take informed decisions.

# X-factor

As the manufacturing industry must make selections based on car reviews. The dataset is being harmed by FAKE/Misleading Reviews, which is a big problem. It must be identified and extracted from the data in order to make excellent business decisions.

Hence my Project will also solve this Problem by doing Real-time Fake Review Detection.

# Built With

* Django
* Html/css/javascript
* Dbsqlite Database
* bootstrap



# Prerequisites

Install Requirnment.txt file using Pip.

# Installation

1. Clone the repo
2. Cd <project directory>(check where manage.py must be present)
   
3. Use python manage.py makemigrations
4. Followed by python manage.py migrate
5. The project setup is completed and ready to start. Use python manage.py runserver to Start the project in local Host.

   
# Features

   * Home Page - DashBoard
   * Data Analysis Tool (for custom dataset)
      * Exploratory Data-Analysis
      * Cluster Analysis
      * Correlation Analysis
   
   * Command-line Query for Generating graphs
   * Fake-Review Detection  (Real-time)
      * Web Scraping From Amazon review to Train model.
   * SignUp/SignIn (for particular user)
   
   
   
   
### Home Page - DashBoard
   ![image](https://user-images.githubusercontent.com/64836894/169657542-b1f34b79-4ac7-4edf-a657-c0eed1cfd7fc.png)
   
### Footer:
   ![image](https://user-images.githubusercontent.com/64836894/169657592-894e098b-d81f-4c61-b42e-050543050e39.png)
   
### Hover Section (User can insert Dataset)
   
   ![image](https://user-images.githubusercontent.com/64836894/169657678-a1eea54e-85a7-41fa-b2a3-92dffacd06e4.png)


### Data-Analysis-Tool

   
* In addition, I will provide a default analysis of the given dataset, including client groups, the most popular automobile specification combinations (engine type, fuel, mileage, and so on), the ideal time to introduce a new car, and so on. as it is capable of:
   
* After that, the user must Insert Dataset. It will take the user to the next page, where they can view the dataset and its features.
   
   ![image](https://user-images.githubusercontent.com/64836894/169657701-ec1572b5-596d-45de-add1-c112461d3d8a.png)
   
* Three options are available in the navigation bar. This will traverse according to the user's actions
   
   ![image](https://user-images.githubusercontent.com/64836894/169657791-6bf7a291-4373-4728-aebb-12aa5c321504.png)
   
   ![image](https://user-images.githubusercontent.com/64836894/169657812-57ddb393-b417-4864-be49-540fa2f326a9.png)



   
### Exploratory Data analysis Tab
   ![image](https://user-images.githubusercontent.com/64836894/169657958-5191f796-292d-47fc-89cb-85d309d2c178.png)
   * Histogram of Price
   * Dominating car BodyType
   * BoxPlot for Price (Outlier analysis)
   * engine size comparision
   * Relationship for Price and Power

   
### Cluster analysis Tab
   ![image](https://user-images.githubusercontent.com/64836894/169657989-17accc53-d604-4d1a-b12e-8d8e56016c42.png)
   * Cluster the cars types and cars using k-means algorithm
   * Price  and horse power with cluster price
   * Power and Mileage after clustering
   * Engine size with Fuel tanks
   * Average price with each cluster
   * Finding potential stretegic groups
   * Cars body type with each cluster

   
### Correlation Grid
   
   ![image](https://user-images.githubusercontent.com/64836894/169658029-76e8cdca-3319-432f-8d89-49239441b358.png)
  
   * Correlation Matrix (to know which features all strongly correlated)
   * Extensive scatter plot grid of more numerical variable to investigate the realtion in more detail


   
   
## Command-line Query for Generating graphs
  * A command line tool where the user can dynamically enter a query.
    ![image](https://user-images.githubusercontent.com/64836894/169658096-6a05251a-d9a2-440d-b790-acfde9fda413.png)
  * the required visualisation will be generated with its inference, allowing the user to understand what the graph is doing.
   ![image](https://user-images.githubusercontent.com/64836894/169658056-f503346f-6b8b-4a02-b538-6ae1c55c879b.png)
  * Currently which option is limited to only 3 graphs as per prototype(line,scatter,bar)
  
   
   ![image](https://user-images.githubusercontent.com/64836894/169658145-b1fb878a-ba51-4884-a74c-fa5b03de188c.png)


   
   
   
   
## Fake Reviews Detection 
Fake reviews make it extremely difficult for manufacturers to make informed judgments, therefore I decided to write a function to detect and remove fake reviews from the dataset for accurate demand and feature forecasts.

* TEXT box where user can Write its Query Whether it is Fake or Not.
  
   ![image](https://user-images.githubusercontent.com/64836894/169658180-41356a07-03a9-474a-896f-85c08b7dfaad.png)
  
* Result Page with decisions:
   
   ![image](https://user-images.githubusercontent.com/64836894/169658211-a3ee8894-a3fc-4d24-b013-1e28918c7d22.png)

   
   
## Login/Logout- to have profiles based on user and track their work.
   
   ![image](https://user-images.githubusercontent.com/64836894/169658234-60cd2df0-1dbc-449e-b803-156338fa61c9.png)
   
## Login with a success message
   
   ![image](https://user-images.githubusercontent.com/64836894/169658262-d8f72251-4456-4e99-baa3-156a47169963.png)

   

