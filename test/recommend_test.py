import sys
import os
import pytest 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from recommend import get_relevant_papers, get_recommendations

# test function get_relevant_papers
def test_get_relevant_papers_1():
    result = get_relevant_papers(1)
    assert len(result) == 10

def test_get_relevant_papers_2():
    result = get_relevant_papers(250)
    assert len(result) == 10

def test_get_relevant_papers_3():
    result = get_relevant_papers(0)
    assert len(result) == 10

def test_get_relevant_papers_4(): 
    with pytest.raises(FileNotFoundError):
        get_relevant_papers(-1)

def test_get_relevant_papers_5(): 
    with pytest.raises(FileNotFoundError):
        get_relevant_papers(2000000)

def test_get_relevant_papers_5(): 
    with pytest.raises(FileNotFoundError):
        get_relevant_papers('abc')

# test function get_recommendations
def test_get_recommendations_1():
    result = get_recommendations(1)
    assert len(result[0]) == 10 and len(result[1]) == 10

def test_get_recommendations_2():
    result = get_recommendations(11)
    assert len(result[0]) == 10 and len(result[1]) == 10

def test_get_recommendations_3():
    with pytest.raises(IndexError):
        get_recommendations(-1)

def test_get_recommendations_4():
    with pytest.raises(IndexError):
        get_recommendations(2000)


def test_get_recommendations_5():
    with pytest.raises(IndexError):
        get_recommendations("abc")