from flask import Flask, render_template, request, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Paper, Author, AuthorPaper
from recommend import get_relevant_papers, get_recommendations
import pickle
import json

app = Flask(__name__)

# --- CONNECT DATABASE --- 
# Configure SQLite database
engine = create_engine('sqlite:///my_database.sqlite3', echo=True)    
# Create table
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Clear Database and load data from csv (need to run only 1st time)
"""
session.query(Paper).delete()
session.query(Author).delete()
session.query(AuthorPaper).delete()
session.query(AuthorCitePaper).delete()
session.commit()
load_paper_csv('data/Paper.csv', session)
load_author_csv('data/Author.csv', session)
load_author_paper_csv('data/Author_Paper.csv', session)
load_author_cite_paper_csv('data/Author_Cite_Paper.csv', session)
"""

"""
    Databased has been built
"""
# --- END CONNECT DATABASE ---

# --- HELPER FUNCTIONS ---

min_year = 1951
max_year = 2005
def get_reversed_dict(dict):
    reversed_dict = {}
    items = dict.items()
    for key, value in items:
        reversed_dict[value] = key 
    return reversed_dict

def get_or_404_db(table, id):
    result = session.get(table, id)
    if result is None:
        abort(404)
    return result

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def id_not_found(id_mapping, id):
    if id not in id_mapping.values():
        return True 
    return False

# --- END HELPER FUNCTIONS ---

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get mapping_id dict
        with open('data/trained_LightGCN/author_mapping.pickle', 'rb') as f:
            author_mapping = pickle.load(f)
        with open('data/trained_LightGCN/paper_mapping.pickle', 'rb') as f:
            paper_mapping = pickle.load(f)
        paper_mapping_reverse = get_reversed_dict(paper_mapping)
        # check id is found
        user_id = request.form['user_id']
        if not is_number(user_id):
            return jsonify({'error': 'The requested resource could not be found'}), 404
        user_id = int(user_id)
        if id_not_found(author_mapping, user_id):
            return jsonify({'error': 'The requested resource could not be found'}), 404
        # get recommendations
        interested_paper_ids, recommend_paper_ids = get_recommendations(user_id)

        interested_paper_ids = [paper_mapping_reverse[paper_id] for paper_id in interested_paper_ids]
        interested_paper_ids = [int(id) for id in interested_paper_ids]
        interestings = session.query(Paper).filter(Paper.id.in_(interested_paper_ids)).all()
    
        recommend_paper_ids = [paper_mapping_reverse[paper_id] for paper_id in recommend_paper_ids]
        recommend_paper_ids = [int(id) for id in recommend_paper_ids]
        recommendations = session.query(Paper).filter(Paper.id.in_(recommend_paper_ids)).all()

        # create response in json
        interestings_json = json.dumps([{'id': paper.id, 'title': paper.title, 'published_year': paper.published_year} for paper in interestings])
        recommendations_json = json.dumps([{'id': paper.id, 'title': paper.title, 'published_year': paper.published_year} for paper in recommendations]) 
        response = {'interestings': interestings_json, 'recommendations': recommendations_json}
        return jsonify(response), 200
    return render_template('home.html')

@app.route('/papers', methods=['GET', 'POST'])
def papers():
    if request.method == 'POST':
        # preprocessing input
        data = request.get_json()
        from_year = data['from_year']
        to_year = data['to_year']
        if from_year != "None" and not is_number(from_year):
            return jsonify({'error': 'Published year is invalid'}), 404
        if to_year != "None" and not is_number(to_year):
            return jsonify({'error': 'Published year is invalid'}), 404
        if (from_year == "None" and to_year == "None"):
            papers = session.query(Paper).filter(Paper.published_year != r'\N').all()
            papers = sorted(papers, key=lambda x: x.published_year, reverse=True)
            papers = [paper.to_dict() for paper in papers]
            return jsonify(papers)
        if (from_year == "None"):
            from_year = min_year
        else:
            from_year = int(from_year)
        if (to_year == "None"):
            to_year = max_year
        else: 
            to_year = int(to_year)
        # remove papers with unknown published_year
        papers = session.query(Paper).filter(Paper.published_year != r'\N').all()
        # filter by published_year and sort
        papers = [paper for paper in papers if int(paper.published_year) >= from_year and int(paper.published_year) <= to_year]
        papers = sorted(papers, key=lambda x: x.published_year, reverse=True)
        papers = [paper.to_dict() for paper in papers]
        return jsonify(papers)      
    else:
        papers = session.query(Paper).filter(Paper.published_year != r'\N').all()
        papers = sorted(papers, key=lambda x: x.published_year, reverse=True)
        return render_template('papers.html',papers=papers)

@app.route('/papers/<int:id>')
def view_paper(id):
    # check id
    curr_paper = get_or_404_db(Paper, id)
    paper_id = id
    # load id_mapping dict and get its reverse
    with open('data/trained_CosineSim/author_id_mapping_CB.pickle', 'rb') as f:
       id_mapping = pickle.load(f)
    reversed_id_mapping = get_reversed_dict(id_mapping)
    # get relevant papers
    paper_ids = get_relevant_papers(id_mapping[paper_id])
    paper_ids = [reversed_id_mapping[id] for id in paper_ids]
    paper_ids = [int(id) for id in paper_ids]
    # create result-list
    papers = session.query(Paper).filter(Paper.id.in_(paper_ids)).all()
    return render_template('view_paper.html', curr_paper=curr_paper, papers=papers)

@app.route('/authors')
def authors():
    authors = session.query(Author).all()
    return render_template('authors.html', authors=authors)

@app.route('/authors/<int:id>')
def view_author(id):
    # check id
    author = get_or_404_db(Author, id)
    author_id = id
    # get published papers of this author
    paper_id_col = session.query(AuthorPaper.paper_id).filter(AuthorPaper.author_id == author_id).all()
    paper_ids = [int(row[0]) for row in paper_id_col]
    papers = session.query(Paper).filter(Paper.id.in_(paper_ids)).all()
    return render_template('view_author.html', author=author, papers=papers, count=len(papers))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == "__main__":
    app.run(debug=True)