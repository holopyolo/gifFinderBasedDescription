from sentence_transformers import SentenceTransformer
from db import *
import numpy as np
import json
import re
import os
path_to_faiss = 'faissdb/'
path_to_labels = 'labels/'

def init_model(name_model="intfloat/multilingual-e5-large", cache_folder='E:/models'):
    model = SentenceTransformer(name_model,
                                cache_folder=cache_folder)
    def embed(texts):
        embs = model.encode(texts)
        return embs
    return embed

class Searcher:
    def __init__(self,
                dataset=None,
                dim=1024,
                name_model="intfloat/multilingual-e5-large",
                root_db='E:/projects/gifFinderBasedDescription/faissdb',
                name_db_faiss='flat.index',
                name_json='dict.json'):
        '''
        
        dataset -> {<path_to_label>.txt: label_1, 
                    ...}
        
        '''
        self.model = init_model(name_model)
        self.db_texts = []
        self.name_model = name_model
        self.name_db_faiss = name_db_faiss
        self.name_json = name_json
        name_model_wauthor = re.sub(r'[a-zA-Z0-9]+/', '', name_model)
        self.db_path = os.path.join(root_db, name_model_wauthor, name_db_faiss)
        self.index = get_ind_faiss(dim, self.db_path)
        if not(os.path.isdir(os.path.join(root_db, name_model_wauthor))):
            os.mkdir(os.path.join(root_db, name_model_wauthor))
        if os.path.isfile(name_json):
            with open(name_json, 'r') as fl:
                self.loaded_labels = json.load(fl)['loaded']
        else:
            self.loaded_labels = []
        if dataset:
            self.update(dataset)

        
    def update(self, dataset: dict):
        to_push = []
        for k, v in dataset.items():
            if k not in self.loaded_labels:
                self.loaded_labels.append(k)
                with open(os.path.join(path_to_labels, k), encoding='utf-8') as fl:
                    to_push.append(fl.readline())
        if len(to_push):
            embed_initial = self.model(to_push)
            push_vectors(self.index, embed_initial, self.db_path)

    
    def finder(self, texts: list, k=1):
        embed_queries = self.model(texts)
        inds = get_top_k_sim(self.index, embed_queries, k)
        relev_docs = np.array(self.loaded_labels)[inds]
        return relev_docs
    



