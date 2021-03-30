from flask import Flask, request, render_template
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = app = Flask(__name__, template_folder='templates', static_folder='static')
model = pickle.load(open('model.pkl', 'rb'))
import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

find('*.txt', '/path/to/dir')


@app.route('/')
def hello_world():
    return render_template('recommendation.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    output = []
    df1 = pd.read_csv("credits.csv")
    df2 = pd.read_csv("movies.csv")
    df1.columns = ['id', 'title', 'cast', 'crew']
    df2 = df2.merge(df1, on='id')
    req = request.form
    final1 = req.get("Temperature")
    final = final1.title()


    def get_recommendations(title, cosine_sim=model):
        indices = pd.Series(df2.index, index=df2['title_x']).drop_duplicates()
        idx = indices.get(title)
        
        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        return df2['title_x'].iloc[movie_indices]
    output.extend(get_recommendations(final, model))
    list_of_movies=output
    # print(output)

    output = (list_of_movies[3:])
    # print(output)
    url_list=[]
    if len(list_of_movies)>3:
        for i in range(3):
            movie=list_of_movies[i]
            query="https://www.imdb.com/find?q="+movie
            
            #############           SCRAPING CODE GOES HERE          ###################
            
            response=requests.get(query)
            site=response.text
            # print(site)
            
            soup=BeautifulSoup(site,'html.parser')
            # pprint(soup)
            td=soup.find(name='td',class_="result_text")
            # pprint(td)
            whatiwant=td.getText()
            # print(whatiwant)
            title=whatiwant
            url_list.append(title)
            a_tag=td.find('a')
            url=a_tag.get('href')
            # print(url)    
            link="https://www.imdb.com/"+url
            # print(link)
            new_response=requests.get(link)
            source=new_response.text
            new_soup=BeautifulSoup(source,"html.parser")
            # print(new_soup)
            target=new_soup.find('img')
            img_url=target.get('src')
            url_list.append(img_url)
        #############           SCRAPING CODE ENDS HERE          ###################
        
        #wXeWr islib nfEiy mM5pbd
        return render_template('recommendation.html', pred1=url_list[0],poster1=url_list[1],pred2=url_list[2],poster2=url_list[3],pred3=url_list[4],poster3=url_list[5],suggestion1=output[0],suggestion2=output[1],suggestion3=output[2],suggestion4=output[3],suggestion5=output[4],suggestion6=output[5],suggestion7=output[6], end='\n')
    else:
        reply="Sorry, Currently we don't have this movie our database :("
        reply2="You could instead try entering the following below!"
        reply3="Hope you Enjoy using our site :)"
        output=['Avatar','Minions','Iron Man','The Guilt Trip','Home Alone','Darling','The Godfather']
        return render_template('recommendation.html', pred1=reply,pred2=reply2,pred3=reply3,suggestion1=output[0],suggestion2=output[1],suggestion3=output[2],suggestion4=output[3],suggestion5=output[4],suggestion6=output[5],suggestion7=output[6], end='\n')
        
