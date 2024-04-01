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

# TEST ROUTE "/" 
def test_home_route_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>SciPaper | Home</title>' in response.data

def test_home_route_post_1(client):
    form_data = {
        'user_id': '1'
    }
    response = client.post('/', data = form_data)
    # assert status code
    assert response.status_code == 200
    # assert data in json response
    response_json = json.loads(response.text)    
    assert "interestings" in response_json
    assert "recommendations" in response_json
    interestings = json.loads(response_json["interestings"])
    recommendations = json.loads(response_json["recommendations"])
    assert len(interestings) == 10
    assert len(recommendations) == 10

def test_home_route_post_2(client):
    form_data = {
        'user_id': '0'
    }
    response = client.post('/', data = form_data)
    # assert status code
    assert response.status_code == 200
    # assert data in json response
    response_json = json.loads(response.text)    
    assert "interestings" in response_json
    assert "recommendations" in response_json
    interestings = json.loads(response_json["interestings"])
    recommendations = json.loads(response_json["recommendations"])
    assert len(interestings) == 10
    assert len(recommendations) == 10

def test_home_route_post_3(client):
    """
    Raise 404 Error Test: out of range
    """
    form_data = {
        'user_id': '2000'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 404
    response_json = json.loads(response.text)   
    assert "error" in response_json

def test_home_route_post_4(client):
    """
    Raise 404 Error Test: negative number
    """
    form_data = {
        'user_id': '-20'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 404
    response_json = json.loads(response.text)   
    assert "error" in response_json

def test_home_route_post_4(client):
    """
    Raise 404 Error Test: string input
    """
    form_data = {
        'user_id': 'abc'
    }
    response = client.post('/', data = form_data)
    assert response.status_code == 404
    response_json = json.loads(response.text)   
    assert "error" in response_json

# TEST ROUTE "/papers" 
def test_papers_route_get(client):
    response = client.get('/papers')
    assert response.status_code == 200
    assert b'<title>SciPaper | Papers</title>' in response.data
    assert b'title' in response.data
    assert b'published_year' in response.data

def test_papers_route_post_1(client):
    form_data = {
        "from_year": "2003", 
        "to_year": "2004"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    response_json = json.loads(response.text)  
    assert len(response_json) > 0
    for paper in response_json:
        assert 'title' in paper and 'published_year' in paper

def test_papers_route_post_2(client):
    form_data = {
        "from_year": "None", 
        "to_year": "2004"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    response_json = json.loads(response.text)  
    assert len(response_json) > 0
    for paper in response_json:
        assert 'title' in paper and 'published_year' in paper

def test_papers_route_post_3(client):
    form_data = {
        "from_year": "2000", 
        "to_year": "None"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    response_json = json.loads(response.text)  
    assert len(response_json) > 0
    for paper in response_json:
        assert 'title' in paper and 'published_year' in paper

def test_papers_route_post_4(client):
    form_data = {
        "from_year": "None", 
        "to_year": "None"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 200
    response_json = json.loads(response.text)  
    assert len(response_json) > 0
    for paper in response_json:
        assert 'title' in paper and 'published_year' in paper

def test_papers_route_post_5(client):
    form_data = {
        "from_year": "Nabc",
        "to_year": "abc"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 404
    response_json = json.loads(response.text)   
    assert "error" in response_json

def test_papers_route_post_6(client):
    form_data = {
        "from_year": "Na1999",
        "to_year": "2003"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post('/papers', data = json.dumps(form_data), headers=headers)
    assert response.status_code == 404
    response_json = json.loads(response.text)   
    assert "error" in response_json

# TEST ROUTE "/authors" 
def test_authors_route(client):
    response = client.get('/authors')
    assert response.status_code == 200
    assert b'<title>SciPaper | Authors </title>' in response.data
    assert b'id' in response.data
    assert b'name' in response.data

# TEST ROUTE "/papers/id"
def test_view_paper_route_1(client):
    response = client.get('/papers/1')
    assert response.status_code == 200
    assert b'<title>SciPaper | Paper</title>'
    assert b'title' in response.data
    assert b'abstract' in response.data

def test_view_paper_route_2(client):
    response = client.get('/papers/2860')
    assert response.status_code == 200
    assert b'<title>SciPaper | Paper</title>'
    assert b'title' in response.data
    assert b'abstract' in response.data

def test_view_paper_route_3(client):
    response = client.get('/papers/2')
    assert response.status_code == 404

def test_view_paper_route_4(client):
    response = client.get('/papers/-1')
    assert response.status_code == 404

def test_view_paper_route_5(client):
    response = client.get('/papers/abc')
    assert response.status_code == 404


# TEST ROUTE "/authors/id"
def test_view_author_route_1(client):
    response = client.get('/authors/26')
    assert response.status_code == 200
    assert b'<title>SciPaper | Author</title>'
    assert b'name' in response.data
    assert b'title' in response.data

def test_view_author_route_2(client):
    response = client.get('/authors/513')
    assert response.status_code == 200
    assert b'<title>SciPaper | Author</title>'
    assert b'name' in response.data
    assert b'title' in response.data

def test_view_author_route_3(client):
    response = client.get('/authors/-12')
    assert response.status_code == 404

def test_view_author_route_4(client):
    response = client.get('/authors/1')
    assert response.status_code == 404

def test_view_author_route_5(client):
    response = client.get('/authors/abc')
    assert response.status_code == 404