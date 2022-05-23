################### IMPORTING ALL THE LIBRARIES  ################


from http.client import HTTPResponse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
import json
import plotly.express as px
from sklearn.cluster import KMeans
import pickle
from nltk.corpus import stopwords
import re
import warnings
warnings.filterwarnings("ignore")
from nltk.stem.porter import PorterStemmer
df_main = pd.read_csv("cars_engage_2022.csv")
df_main['car'] = df_main.Make + ' ' + df_main.Model
c = ['Make','Model','car','Variant','Body_Type','Fuel_Type','Fuel_System','Type','Drivetrain','Ex-Showroom_Price','Displacement','Cylinders',
     'ARAI_Certified_Mileage','Power','Torque','Fuel_Tank_Capacity','Height','Length','Width','Doors','Seating_Capacity','Wheelbase','Number_of_Airbags']

df_main['Ex-Showroom_Price'] = df_main['Ex-Showroom_Price'].str.replace('Rs. ','',regex=False)
df_main['Ex-Showroom_Price'] = df_main['Ex-Showroom_Price'].str.replace(',','',regex=False)
df_main['Ex-Showroom_Price'] = df_main['Ex-Showroom_Price'].astype(int)
df_main = df_main[c]
df_main = df_main[~df_main.ARAI_Certified_Mileage.isnull()]
df_main = df_main[~df_main.Make.isnull()]
df_main = df_main[~df_main.Width.isnull()]
df_main = df_main[~df_main.Cylinders.isnull()]
df_main = df_main[~df_main.Wheelbase.isnull()]
df_main = df_main[~df_main['Fuel_Tank_Capacity'].isnull()]
df_main = df_main[~df_main['Seating_Capacity'].isnull()]
df_main = df_main[~df_main['Torque'].isnull()]
df_main['Height'] = df_main['Height'].str.replace(' mm','',regex=False).astype(float)
df_main['Length'] = df_main['Length'].str.replace(' mm','',regex=False).astype(float)
df_main['Width'] = df_main['Width'].str.replace(' mm','',regex=False).astype(float)
df_main['Wheelbase'] = df_main['Wheelbase'].str.replace(' mm','',regex=False).astype(float)
df_main['Fuel_Tank_Capacity'] = df_main['Fuel_Tank_Capacity'].str.replace(' litres','',regex=False).astype(float)
df_main['Displacement'] = df_main['Displacement'].str.replace(' cc','',regex=False)
df_main.loc[df_main.ARAI_Certified_Mileage == '9.8-10.0 km/litre','ARAI_Certified_Mileage'] = '10'
df_main.loc[df_main.ARAI_Certified_Mileage == '10kmpl km/litre','ARAI_Certified_Mileage'] = '10'
df_main['ARAI_Certified_Mileage'] = df_main['ARAI_Certified_Mileage'].str.replace(' km/litre','',regex=False).astype(float)
df_main.Number_of_Airbags.fillna(0,inplace= True)
df_main['price'] = df_main['Ex-Showroom_Price'] * 0.014
df_main.drop(columns='Ex-Showroom_Price', inplace= True)
df_main.price = df_main.price.astype(int)
HP = df_main.Power.str.extract(r'(\d{1,4}).*').astype(int) * 0.98632
HP = HP.apply(lambda x: round(x,2))
TQ = df_main.Torque.str.extract(r'(\d{1,4}).*').astype(int)
TQ = TQ.apply(lambda x: round(x,2))
df_main.Torque = TQ
df_main.Power = HP

df_main.Doors = df_main.Doors.astype(int)
df_main.Seating_Capacity = df_main.Seating_Capacity.astype(int)
df_main.Number_of_Airbags = df_main.Number_of_Airbags.astype(int)
df_main.Displacement = df_main.Displacement.astype(int)
df_main.Cylinders = df_main.Cylinders.astype(int)
df_main.columns = ['make', 'model','car', 'variant', 'body_type', 'fuel_type', 'fuel_system','type', 'drivetrain', 'displacement', 'cylinders',
              'mileage', 'power', 'torque', 'fuel_tank','height', 'length', 'width', 'doors', 'seats', 'wheelbase','airbags', 'price']
#########################################preprocession the data#################################


########################################FUNCTION FOR HOME PAGE#################################
def index(request):
    
    return render(request , 'index.html')

####################################### FAKE REVIEWS  #########################################

ps = PorterStemmer()
# Load model and vectorizer
model = pickle.load(open('model2.pkl', 'rb'))
tfidfvect = pickle.load(open('tfidfvect2.pkl', 'rb'))


################################### RESULT PAGE FOR THE REVIEWS ##################################

def result(request):
  #Get the text
    djtext = request.POST.get('text', 'default')
    text = djtext
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review_vect = tfidfvect.transform([review]).toarray()
    prediction = 'FAKE' if model.predict(review_vect) == 0 else 'REAL'
    print(prediction)
    

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    numberremover = request.POST.get('numberremover','off')

    #Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
                

        params = {'purpose':'Removed Punctuations', 'analyzed_text': analyzed,'pred':prediction}
        djtext = analyzed

    if(fullcaps=="on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed,'pred':prediction}
        djtext = analyzed

    if(extraspaceremover=="on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            # It is for if a extraspace is in the last of the string
            if char == djtext[-1]:
                    if not(djtext[index] == " "):
                        analyzed = analyzed + char

            elif not(djtext[index] == " " and djtext[index+1]==" "):                        
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed,'pred':prediction}
        djtext = analyzed

    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext:
            if char != "\n" and char!="\r":
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed,'pred':prediction}
    
    if (numberremover == "on"):
        analyzed = ""
        numbers = '0123456789'

        for char in djtext:
            if char not in numbers:
                analyzed = analyzed + char
        
        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed,'pred':prediction}
        djtext = analyzed
    
    
    if(removepunc != "on" and newlineremover!="on" and extraspaceremover!="on" and fullcaps!="on" and numberremover != "on"):
        return HttpResponse("please select any operation and try again")

    return render(request, 'result.html', params)

######################################## Result page for User input dataset for fake reviews ###################################



def result2(request):
    if request.method == 'POST':
        file = request.FILES['fileupload']
        df = pd.read_csv(file)
        
        corpus = []
        for i in range(0, len(df)):
            review = re.sub('[^a-zA-Z]', ' ', df['Review'][i])
            review = review.lower()
            review = review.split()
            
            
            
            review = ' '.join(review)
            review_vect = tfidfvect.transform([review]).toarray()
            prediction = 'FAKE' if model.predict(review_vect) == 0 else 'REAL'
            corpus.append(prediction)
        df['prediction']  = corpus
        context = {'dataframe':df}


    return render(request,'result2.html',context)


######################################## FAKE PAGE WHERE USER CAN SEE IT'S INPUT REVIEWS AND DO REAL TIME PREDICTION

def fake(request):
    

    return render(request,'fake.html')

######################################## DATA ANALYSIS PAGE  WITH DATASET OUTPUT #######################################################

def static(request):
    if request.method == 'POST':
        file = request.FILES['fileupload']
        df = pd.read_csv(file,index_col=0)
        df['car'] = df.Make + ' ' + df.Model
        c = ['Make','Model','car','Variant','Body_Type','Fuel_Type','Fuel_System','Type','Drivetrain','Ex-Showroom_Price','Displacement','Cylinders',
             'ARAI_Certified_Mileage','Power','Torque','Fuel_Tank_Capacity','Height','Length','Width','Doors','Seating_Capacity','Wheelbase','Number_of_Airbags']
        
        df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace('Rs. ','',regex=False)
        df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace(',','',regex=False)
        df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].astype(int)
        df = df[c]
        df = df[~df.ARAI_Certified_Mileage.isnull()]
        df = df[~df.Make.isnull()]
        df = df[~df.Width.isnull()]
        df = df[~df.Cylinders.isnull()]
        df = df[~df.Wheelbase.isnull()]
        df = df[~df['Fuel_Tank_Capacity'].isnull()]
        df = df[~df['Seating_Capacity'].isnull()]
        df = df[~df['Torque'].isnull()]
        df['Height'] = df['Height'].str.replace(' mm','',regex=False).astype(float)
        df['Length'] = df['Length'].str.replace(' mm','',regex=False).astype(float)
        df['Width'] = df['Width'].str.replace(' mm','',regex=False).astype(float)
        df['Wheelbase'] = df['Wheelbase'].str.replace(' mm','',regex=False).astype(float)
        df['Fuel_Tank_Capacity'] = df['Fuel_Tank_Capacity'].str.replace(' litres','',regex=False).astype(float)
        df['Displacement'] = df['Displacement'].str.replace(' cc','',regex=False)
        df.loc[df.ARAI_Certified_Mileage == '9.8-10.0 km/litre','ARAI_Certified_Mileage'] = '10'
        df.loc[df.ARAI_Certified_Mileage == '10kmpl km/litre','ARAI_Certified_Mileage'] = '10'
        df['ARAI_Certified_Mileage'] = df['ARAI_Certified_Mileage'].str.replace(' km/litre','',regex=False).astype(float)
        df.Number_of_Airbags.fillna(0,inplace= True)
        df['price'] = df['Ex-Showroom_Price'] * 0.014
        df.drop(columns='Ex-Showroom_Price', inplace= True)
        df.price = df.price.astype(int)
        HP = df.Power.str.extract(r'(\d{1,4}).*').astype(int) * 0.98632
        HP = HP.apply(lambda x: round(x,2))
        TQ = df.Torque.str.extract(r'(\d{1,4}).*').astype(int)
        TQ = TQ.apply(lambda x: round(x,2))
        df.Torque = TQ
        df.Power = HP
        df.Doors = df.Doors.astype(int)
        df.Seating_Capacity = df.Seating_Capacity.astype(int)
        df.Number_of_Airbags = df.Number_of_Airbags.astype(int)
        df.Displacement = df.Displacement.astype(int)
        df.Cylinders = df.Cylinders.astype(int)
        df.columns = ['make', 'model','car', 'variant', 'body_type', 'fuel_type', 'fuel_system','type', 'drivetrain', 'displacement', 'cylinders',
              'mileage', 'power', 'torque', 'fuel_tank','height', 'length', 'width', 'doors', 'seats', 'wheelbase','airbags', 'price']
        ##^ preprocession the data
        
        cols = list(df.columns)
        df10 = df.head(15)
        context = {'d': df10,'columns':cols}

    return render(request, 'static.html', context)

################################# GENERATE GRAPHS #####################################################

def graph(request):
    query = request.POST.get('command', 'default')
    def Convert(string):
        li = list(string.split(" "))
        return li
    Query = Convert(query)
    print(Query)
    x = Query[3]
    y = Query[5]
    
    graph_type = Query[1]
    x_axis = df_main[x]
    y_axis = df_main[y]
    
    


    k = [['x_axis', 'y_axis']]
    for x, y in zip(x_axis,y_axis):
        t = [x, y]
        k.append(t)
    coordinates = json.dumps(k)

    if(graph_type=='bargraph'):
        gtype=1
        context = {"g_type":gtype,"coords":coordinates,'a':x,'b':y}
        return render(request,'bar_graph.html',context)

    if(graph_type=='scatterplot'):
        gtype=2
        context = {"g_type":gtype,"coords":coordinates,'a':x,'b':y}
        return render(request,'scatter_graph.html',context)

    if(graph_type=='linechart'):
        gtype=3
        context = {"g_type":gtype,"coords":coordinates,'a':x,'b':y}
        return render(request,'line_graph.html',context)

############################ LOGIN PAGE ######################################

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("index")

    return HttpResponse("404- Not found")

############################## LOGOUT PAGE ###############################################

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')

############################# SIGNUP PAGE ##################################################

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " ID has been successfully created")
        return redirect('index')
    else:

        return HttpResponse("404 - Not found")

############################## FUNCTION FOR COMMAND LINE TOOL ################################

def graph1(request):
    query = request.POST.get('command', 'default')
    def Convert(string):
        li = list(string.split(" "))
        return li
    Query = Convert(query)
    print(Query)
    x = Query[3]
    y = Query[5]
    graph_type = Query[1]
    x_axis = df_main[x]
    y_axis = df_main[y]

    k = [['x_axis', 'y_axis']]
    for x, y in zip(x_axis,y_axis):
        t = [x, y]
        k.append(t)
    coordinates = json.dumps(k)
    context = {"coords":coordinates,'a':x,'b':y}


    return render(request,'line_graph.html',context)


############################## FUNCTION TO PERFORM EDA ############################################


def eda(request):
    c = df_main['price'].value_counts()
    k = [['K', 'V']]
    for x, y in c.iteritems():
        t = [x, y]
        k.append(t)
    price = json.dumps(k)

    #count plot for car body type
    plt.figure(figsize=(16,7))
    sns.countplot(data=df_main, y='body_type',alpha=.6,color='darkblue')
    plt.title('Cars by car body type',fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('')
    plt.ylabel('');
    plt.savefig('assets/count.png')
    #boxplot for car and its body type
    plt.figure(figsize=(12,6))
    sns.boxplot(data=df_main, x='price', y='body_type', palette='viridis')
    plt.savefig('assets/box3.png')

    #car engine size
    plt.figure(figsize=(14,6))
    sns.histplot(data=df_main, x='displacement',alpha=.6, color='darkblue',bins=10)
    plt.savefig('assets/box4.png')
    #hostogram for engine size
    c = df_main['power'].value_counts()
    k = [['K', 'V']]
    for x, y in c.iteritems():
        t = [x, y]
        k.append(t)
    power = json.dumps(k)
    #horsepower vs different body
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=df_main, x='power', y='price',hue='body_type',palette='viridis',alpha=.89, s=120 );
    plt.xticks(fontsize=13);
    plt.yticks(fontsize=13)
    plt.xlabel('power',fontsize=14)
    plt.ylabel('price',fontsize=14)
    plt.title('Relation between power and price',fontsize=20);
    plt.savefig('assets/scatter1.png')
    #jon plot
    
    plt.figure(figsize=(10,8))
    sns.jointplot(data=df_main, x='mileage', y='price',kind= 'reg', palette='viridis',height=8,  ratio=7)
    plt.savefig('assets/joinplot.png')

    context={"p":price,"p1":power}

    return render(request,'eda.html',context)


######################################### FUCNTION TO PERFORM CLUSTER ANALYSIS ############################################

def cluster(request):
    df_c = df_main.copy()
    df_c = df_c[df_c.price < 60000]
    num_cols = [ i for i in df_c.columns if df_c[i].dtype != 'object']
    km = KMeans(n_clusters=8, n_init=20, max_iter=400, random_state=0)
    clusters = km.fit_predict(df_c[num_cols])
    df_c['cluster'] = clusters
    df_c.cluster = (df_c.cluster + 1).astype('object')
    
    
    

    
    
    #plot of price and horse power after clustering
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=df_c, y='price', x='power',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of price and horsepower with clusterspclusters predicted', fontsize=18)
    plt.xlabel('power',fontsize=16)
    plt.ylabel('price',fontsize=16);
    plt.savefig('assets/c1.png')
    #power vs mileage
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df_c, x='power', y='mileage',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of milage and horsepower with clusters', fontsize=18);
    plt.xlabel('power',fontsize=16)
    plt.ylabel('mileage',fontsize=16);
    plt.savefig('assets/c2.png')
    #engine size vs fuel tank
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df_c, x='fuel_tank', y='displacement',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of milage and horsepower with clusters', fontsize=18);
    plt.xlabel('Fuel Tank Capacity ',fontsize=16)
    plt.ylabel('Engine size',fontsize=16);
    plt.savefig('assets/c3.png')
    #check the average price of each cluster
    plt.figure(figsize=(14,6))
    sns.barplot(data=df_c, x= 'cluster', ci= 'sd', y= 'price', palette='viridis',order=df_c.groupby('cluster')['price'].mean().sort_values(ascending=False).index);
    plt.yticks([i for i in range(0,65000,5000)])
    plt.title('Average price of each cluster',fontsize=20)
    plt.xlabel('Cluster',fontsize=16)
    plt.ylabel('Avg car price', fontsize=16)
    plt.xticks(fontsize=14)
    plt.savefig('assets/b1.png')
    #Now we check how many cars exists in each cluster
    plt.figure(figsize=(14,6))
    sns.countplot(data=df_c, x= 'cluster', palette='viridis',order=df_c.cluster.value_counts().index);
    # plt.yticks([i for i in range(0,65000,5000)])
    plt.title('Number of cars in each cluster',fontsize=18)
    plt.xlabel('Cluster',fontsize=16)
    plt.ylabel('Number of cars', fontsize=16)
    plt.xticks(fontsize=14)
    plt.savefig('assets/b2.png')
    return render(request,'cluster.html')


############################### FUCNTION TO PERFORM CORRELATION #######################################


def correlation(request):
    plt.figure(figsize=(22,8))
    sns.heatmap(df_main.corr(), annot=True, fmt='.2%')
    plt.title('Correlation between differet variable',fontsize=20)
    plt.xticks(fontsize=14, rotation=320)
    plt.yticks(fontsize=14);
    plt.savefig('assets/a1.png')
    sns.pairplot(df_main,vars=[ 'displacement', 'mileage', 'power', 'price'], hue= 'fuel_type',
             palette=sns.color_palette('magma',n_colors=4),diag_kind='kde',height=2, aspect=1.8);
    plt.savefig('assets/a2.png')
    
    return render(request,'correlation.html')


################################ FUNCTION FOR ABOUT US PAGE ###############################################



def aboutus(request):

    return render(request,'aboutus.html')



################################# FUNCTION FOR RETURNIG BACK TO INDEX PAGE ###################################


def index2(request):

    return render(request , 'index.html')

