import sys
import os
import pytest 
import json
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from app import app

@pytest.fixture
def client():
    """
    Create a Flask test client to test the app
    """
    return app.test_client()

# TEST 1: HOME -> GET RECOMMEND (USER_ID = 1) -> VIEW_PAPER 
def test_1(client):
    # HOME
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>SciPaper | Home</title>' in response.data
    # GET RECOMMEND
    form_data = {
        'user_id': '1'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 200
    response_json = json.loads(response.text)    
    assert "interestings" in response_json
    assert "recommendations" in response_json
    interestings = json.loads(response_json["interestings"])
    recommendations = json.loads(response_json["recommendations"])
    assert len(interestings) == 10
    assert len(recommendations) == 10
    # VIEW_PAPER
    id = recommendations[0]['id']
    response = client.get(f'/papers/{id}')
    assert response.status_code == 200
    assert b'<title>SciPaper | Paper</title>'
    assert b'title' in response.data
    assert b'abstract' in response.data

# TEST 2: HOME -> GET RECOMMEND (404 ERROR) -> GET RECOMMEND (USE_ID = 2)
def test_2(client):
    # HOME
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>SciPaper | Home</title>' in response.data
    # GET RECOMMEND - 404
    form_data = {
        'user_id': 'abc'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 404
    # GET RECOMMEND - USER_ID = 2
    form_data = {
        'user_id': '2'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 200
    response_json = json.loads(response.text)    
    assert "interestings" in response_json
    assert "recommendations" in response_json
    interestings = json.loads(response_json["interestings"])
    recommendations = json.loads(response_json["recommendations"])
    assert len(interestings) == 10
    assert len(recommendations) == 10

# TEST 3: AUTHORS -> VIEW_AUTHOR -> VIEW_PAPER
def test_3(client):
    # AUTHORS
    response = client.get('/authors')
    assert response.status_code == 200
    assert b'<title>SciPaper | Authors</title>' in response.data
    # VIEW AUTHOR
    response = client.get('/authors/26')
    assert response.status_code == 200
    assert b'<title>SciPaper | Author</title>' in response.data
    # VIEW PAPER
    response = client.get('/papers/115288')
    assert response.status_code == 200
    assert b'<title>SciPaper | Paper</title>' in response.data

# TEST 4: PAPERS -> PAPERS (2003 - 2005) -> VIEW PAPER
def test_4(client):
    # PAPERS
    response = client.get('/papers')
    assert response.status_code == 200
    assert b'<title>SciPaper | Papers</title>' in response.data
    # PAPERS 2003 - 2005
    form_data = {
        "from_year": "2003",
        "to_year": "2005"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data=json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    papers = json.loads(response.text)  
    assert len(papers) > 0
    for paper in papers:
        assert 'title' in paper and 'published_year' in paper
    # VIEW_PAPER
    id = papers[0]['id']
    response = client.get(f'/papers/{id}')
    assert response.status_code == 200
    assert b'<title>SciPaper | Paper</title>'
    assert b'title' in response.data
    assert b'abstract' in response.data

# TEST 5: PAPERS -> PAPERS (2003 - 2005) -> PAPERS (None - 1960)
def test_5(client):
    # PAPERS
    response = client.get('/papers')
    assert response.status_code == 200
    assert b'<title>SciPaper | Papers</title>' in response.data
    # PAPERS 2003 - 2005
    form_data = {
        "from_year": "2003",
        "to_year": "2005"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data=json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    papers = json.loads(response.text)  
    assert len(papers) > 0
    for paper in papers:
        assert 'title' in paper and 'published_year' in paper
    # PAPERS None - 1960
    form_data = {
        "from_year": "None",
        "to_year": "1960"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data=json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    papers = json.loads(response.text)  
    assert len(papers) > 0
    for paper in papers:
        assert 'title' in paper and 'published_year' in paper

# TEST 6: PAPERS -> PAPERS (2004 - 2003) -> PAPERS (2003 - 2004)
def test_6(client):
    # PAPERS
    response = client.get('/papers')
    assert response.status_code == 200
    assert b'<title>SciPaper | Papers</title>' in response.data
    # PAPERS 2004 - 2003
    form_data = {
        "from_year": "2004",
        "to_year": "2003"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data=json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    papers = json.loads(response.text)  
    assert len(papers) == 0
    # PAPERS 2003 - 2004
    form_data = {
        "from_year": "2003",
        "to_year": "2004"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data=json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    papers = json.loads(response.text)  
    assert len(papers) > 0
    for paper in papers:
        assert 'title' in paper and 'published_year' in paper