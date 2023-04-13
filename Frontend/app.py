from flask import Flask, render_template, request, url_for
import numpy as np
import pickle

model = pickle.load(open('Frontend/popular.pkl', 'rb'))
final_data_required = pickle.load(
    open('Frontend/final_data_required.pkl', 'rb'))
similarity_score = pickle.load(open('Frontend/similarity_score.pkl', 'rb'))
book_with_rating = pickle.load(open('Frontend/book_with_rating_new.pkl', 'rb'))


app = Flask(__name__)


@app.route('/')
def show_options():
    rounded_list = [round(item, 2) for item in model["avg_rating"].values]
    return render_template('index.html', author=list(model["Book-Author"].values), title=list(model["Book-Title"].values), image=list(model["Image"].values), rating=rounded_list)
    # return render_template('dash.html',options=list(model["Book-Title"].values))


@app.route('/recommend')
def recommend():
    return render_template('xyz.html', options=list(book_with_rating["Book-Title"].unique()))


@app.route('/final', methods=['post'])
def final():
    input = request.form.get("user")
    index = np.where(final_data_required.index == input)[0][0]
    similar_book = sorted(
        list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]
    data = []
    for i in similar_book:
        temp = book_with_rating[book_with_rating["Book-Title"]
                                == final_data_required.index[i[0]]]
        variable = []
        variable.extend(list(temp.drop_duplicates(
            "Book-Title")["Book-Title"].values))
        variable.extend(list(temp.drop_duplicates(
            "Book-Title")["Book-Author"].values))
        variable.extend(
            list(temp.drop_duplicates("Book-Title")["Image"].values))
        variable.extend(list(temp.drop_duplicates(
            "Book-Title")["Publisher"].values))
        # print(final_data_required.index[i[0]])

        data.append(variable)

    return render_template("xyz.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
