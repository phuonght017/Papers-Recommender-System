import json
import pandas as pd
import numpy as np
import pickle
import os

## --- GET RELEVANT PAPERS --- ##
def open_file_json(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)
    
def get_relevant_papers(idx):
    try:
        sim_scores = open_file_json(f'data/trained_CosineSim/sim_scores/sim_score_{idx}.json')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"file data/trained_CosineSim/sim_scores/sim_score_{idx}.json does not exist")
    # Get top 12 paper id
    sim_scores = sim_scores[1:11]
    paper_ids = [i[0] for i in sim_scores]
    # Return the top 10 most similar papers
    return paper_ids

## --- END GET RELEVANT PAPERS --- ##

## --- GET RECOMMENDATIONS FOR USER --- ##
    # Helper functions
with open('data/trained_LightGCN/author_mapping.pickle', 'rb') as f:
    author_mapping = pickle.load(f)
with open('data/trained_LightGCN/paper_mapping.pickle', 'rb') as f:
    paper_mapping = pickle.load(f)
data = pd.read_csv('data/Author_Cite_Paper.csv')

def load_edge_csv(data, src_index_col, src_mapping, dst_index_col, dst_mapping):
    """Loads csv containing edges between users and items

    Args:
        data (dataframe): dataframe converted from csv file
        src_index_col (str): column name of users
        src_mapping (dict): mapping between row number and user id
        dst_index_col (str): column name of items
        dst_mapping (dict): mapping between row number and item id
    Returns:
        torch.Tensor: 2 by N matrix containing the node ids of N user-item edges
    """
    df = data
    src = [src_mapping[index] for index in df[src_index_col]]
    dst = [dst_mapping[index] for index in df[dst_index_col]]

    edge_index = [[], []]
    for i in range(df.shape[0]):
        edge_index[0].append(src[i])
        edge_index[1].append(dst[i])

    return edge_index

edge_index = load_edge_csv(
    data,
    src_index_col='author_id',
    src_mapping=author_mapping,
    dst_index_col='paper_id',
    dst_mapping=paper_mapping,
)

def get_user_positive_items(edge_index):
    """Generates dictionary of positive items for each user
    Args:
        edge_index: 2 by N list of edges

    Returns:
        dict: dictionary of positive items for each user
    """
    user_pos_items = {}
    for i in range(len(edge_index[0])):
        user = edge_index[0][i]
        item = edge_index[1][i]
        if user not in user_pos_items:
            user_pos_items[user] = []
        user_pos_items[user].append(item)
    return user_pos_items

user_pos_items = get_user_positive_items(edge_index)

# Load embedding matrixes
items_emb = np.load('data/trained_LightGCN/light_gcn_items_embeddings.npy')
users_emb = np.load('data/trained_LightGCN/light_gcn_users_embeddings.npy')

def get_recommendations(idx, num_recs = 10):
    # using inner product to calculate scores for items
    user_id = idx
    if isinstance(user_id, int) and user_id >= 0 and user_id < len(users_emb):
        e_u = users_emb[user_id]
    else:
        raise IndexError(f"ID {user_id} is out of range or invalid")    
    scores = items_emb @ e_u

    # get top scores
    ranked_scores = list(enumerate(scores))
    ranked_scores = sorted(ranked_scores, key=lambda x: x[1], reverse=True)
    k_top = len(user_pos_items[user_id]) + num_recs
    ranked_scores = ranked_scores[1:(k_top + 1)]

    # get interested papers
    interested_paper_ids = [ranked_score[0] for ranked_score in ranked_scores if ranked_score[0] in user_pos_items[user_id]][:num_recs]
    # get recommended papers
    recommend_paper_ids = [ranked_score[0] for ranked_score in ranked_scores if ranked_score[0] not in user_pos_items[user_id]][:num_recs]
    return interested_paper_ids, recommend_paper_ids
