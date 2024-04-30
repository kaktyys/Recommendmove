from flask import Flask, render_template, request
import requests
import json
import pandas as pd
from io import BytesIO
from random import choice

app = Flask(__name__)
colums_n = ['id', 'name', 'rating', 'poster', 'genres', 'top10', 'top250', 'ageRating', 'year', 'movieLength']
headers = {
    "accept": "application/json",
    "X-API-KEY": "2VGVM8B-9KHM1FV-HHNFKEK-T895BDJ"
}

selected_genres = []
checkboxes = ['a', 'b', 'c']


def get_kino_data(year, genre1, genre2, genre3):
    # формируем ссылку с запросом
    url = f"https://api.kinopoisk.dev/v1.4/movie?year={year - 3}-{year}&genres.name={genre1}&genres.name={genre2}&genres.name={genre3}&movie?rating.imdb=7-10&rating.kp=7-10"

    # url = "https://api.kinopoisk.dev/v1.4/movie?year=2021&genres.name=криминал&genres.name=драма&movie?rating.imdb=7-10&rating.kp=7-10"
    # определеям заголовки и ключ

    response = requests.get(url, headers=headers)
    df = pd.read_json(BytesIO(response.content))

    film = df['docs'][0]
    film.items()
    da = pd.DataFrame.from_dict(film, orient='index').reset_index()
    data = da.transpose().reset_index()
    len(data.columns)
    convert_data = data
    drop_c = []
    for i in range(0, len(data.columns) - 1):
        cn = data[i][0]
        if cn not in colums_n:
            drop_c.append(i)

    drop_c
    convert_data = convert_data.drop(columns=drop_c)
    convert_data = convert_data.drop(columns=['index'])
    cn = []
    for i in convert_data.columns:
        cn.append(convert_data[i][0])

    convert_data.columns = cn
    convert_data = convert_data[colums_n]
    rt = convert_data.iloc[1]['rating']
    rs = []
    for ele in rt.values():
        rs.append(ele)
    avg_rt = int((rs[0] * 10 + rs[1] * 10 + rs[2] * 10 + rs[3]))
    convert_data.iloc[1]['rating'] = avg_rt
    gen = []
    genre = convert_data.iloc[1]['genres']
    for ele in genre:
        gen.append(ele.values())
    convert_data.iloc[1]['genres'] = gen
    for i in range(1, len(df.index)):
        film_t = df['docs'][i]
        film_t.items()
        da_t = pd.DataFrame.from_dict(film_t, orient='index').reset_index()
        data_t = da_t.transpose().reset_index()
        convert_data_t = data_t
        drop_c = []
        for j in range(0, len(data_t.columns) - 1):
            cn = data_t[j][0]
            if cn not in colums_n:
                drop_c.append(j)

        convert_data_t = convert_data_t.drop(columns=drop_c)
        convert_data_t = convert_data_t.drop(columns=['index'])
        cn = []
        for j in convert_data_t.columns:
            cn.append(convert_data_t[j][0])

        convert_data_t.columns = cn
        convert_data_t = convert_data_t[colums_n]
        convert_data_t = convert_data_t.drop(index=0)
        rt = convert_data_t.iloc[0]['rating']
        rs = []
        for ele in rt.values():
            rs.append(ele)
        avg_rt = int((rs[0] * 10 + rs[1] * 10 + rs[2] * 10 + rs[3]))
        convert_data_t.iloc[0]['rating'] = avg_rt
        genre = convert_data_t.iloc[0]['genres']
        for ele in genre:
            gen.append(ele.values())
        convert_data_t.iloc[0]['genres'] = gen

        frames = [convert_data, convert_data_t]
        convert_data = pd.concat(frames)
    return convert_data


def names(year, first, second, thried):
    data_set1 = get_kino_data(year, first, second, thried)
    nam = data_set1['name'].tolist()
    return nam


def posters(year, first, second, thried):
    data_set1 = get_kino_data(year, first, second, thried)
    post = data_set1['poster'].tolist()
    return post


@app.route('/', methods=['POST', 'GET'])
def index():
    global genres
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        sex = request.form['sex']
        genres = request.form.getlist('genres')
        film = names(int(age), genres[0], genres[1], genres[2])
        film1 = film[1:6]
        film2 = film[6:]
        full_filename = posters(int(age), genres[0], genres[1], genres[2])
        full_filename = full_filename[1:]
        poster = []
        for elem in full_filename:
            poster.append(elem['previewUrl'])
        poster1 = poster[:5]
        poster2 = poster[5:]
        return render_template('second.html', checkboxes1=film1, checkboxes2=film2, user_image1=poster1, user_image2=poster2)


@app.route('/result', methods=['POST', 'GET'])
def result():
    global genres
    recom = names(2023, genres[0], genres[1], genres[2])
    recom = recom[1:]
    recoment = []
    for i in range(3):
        recoment.append(choice(recom))
    return render_template('result.html', recoment=recoment)


if __name__ == '__main__':
    app.run(debug=True)
