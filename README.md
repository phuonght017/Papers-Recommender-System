# Papers Recommender System
## Introduction
This repository contains code for a scientific papers recommender system. The main purpose of this system is to provide users with access to a large number of scientific articles and, within these articles, to find articles that are truly relevant to their field of research and interests. 
Tasks during the work process include: 
* Performing an analysis of solutions for recommending papers;
* Training and evaluating the recommender model;
* Designing and implementing a web-app interface for the system;
* Testing the recommender system.
## GNN Recommender System
Based on the results of analysis and comparison, GNN (Graph neural network) was chosen to build the recommender system. Specifically, in this project, the LightGCN algorithm is implemented thanks to its simplicity in structure, helping to reduce the amount of computation needed to increase model training performance.
Dataset used to train the model: [Author_Cite_Paper.csv](https://github.com/phuonght017/Papers-Recommender-System/blob/main/data/Author_Cite_Paper.csv)
This file contains interaction data between researchers and papers, specifically author citations of a paper. Each sample includes 3 features:
* author_id
* paper_id
* year_citation
This data set is used to build a graph, in which the nodes are authors and papers, author and paper have an edge connected to each other if the author cites this paper.
To build and train the model, we use the PyTorch library. The code is in the notebook file [PapersRS_ver4.ipynb](https://github.com/phuonght017/Papers-Recommender-System/blob/main/data/train_model_code/PapersRS_ver4.ipynb)
## Project Structure
1. Dataset and Trained model: folder [data](https://github.com/phuonght017/Papers-Recommender-System/tree/main/data)
2. Flask app: [app.py](https://github.com/phuonght017/Papers-Recommender-System/blob/main/app.py)
3. Test cases for PyTest: folder [test](https://github.com/phuonght017/Papers-Recommender-System/tree/main/test)
## References
1. X. Bai, M. Wang, I. Lee, Z. Yang, X. Kong, F. Xia. Scientific Paper Recommendation: A Survey // IEEE Access – 2019 – P.9324-9339
2. Xiang Wang, Xiangnan He, Meng Wang, Fuli Feng, and Tat-Seng Chua. Neural Graph Collaborative Filtering // Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval – 2019 – 10p.
3. Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, Meng Wang. LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation // Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval – 2020 – 10p.
4. Hung Nghiep Tran, Tin Huynh, Kiem Hoang. A Potential Approach to Overcome Data Limitation in Scientific Publication Recommendation // KSE – 2015 – 4p. 
5. Jurij Nastran, Ermin Omeragić, Tomaž Martinčič. Better Recommender systems with LighGCN. Available on this link: [Better Recommender systems with LighGCN](https://medium.com/@jn2279/better-recommender-systems-with-lightgcn-a0e764af14f9)
