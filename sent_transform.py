from sentence_transformers import SentenceTransformer
from db import *
import numpy as np
import json
import os
path_to_labels = 'labels/'

def init_model(name_model="intfloat/multilingual-e5-large", cache_folder='E:/models'):
    model = SentenceTransformer(name_model,
                                cache_folder=cache_folder)
    def embed(texts):
        embs = model.encode(texts)
        print(model.similarity(embs, embs))
        return embs
    return embed

class Searcher:
    def __init__(self,
                dataset=None,
                dim=1024,
                name_model="intfloat/multilingual-e5-large",
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
        self.index = get_ind_faiss(dim, name_db_faiss)
        self.name_json = name_json
        if os.path.isfile(name_json):
            with open(name_json, 'r') as fl:
                self.loaded_labels = json.load(fl)['loaded']
        else:
            self.loaded_labels = []
            with open(name_json, 'w') as fl:
                json.dump({'loaded': []}, fl)
        if dataset:
            self.update(dataset)

        
    def update(self, dataset: dict):
        to_push = []
        for k, v in dataset.items():
            if k not in self.loaded_labels:
                self.loaded_labels.append(k)
                with open(os.path.join(path_to_labels, k)) as fl:
                    to_push.append(fl.readline())
        print(to_push)
        if len(to_push):
            embed_initial = self.model(to_push)
            push_vectors(self.index, embed_initial, self.name_db_faiss)
            with open(self.name_json, 'w') as fl:
                json.dump({'loaded': self.loaded_labels}, fl)

    
    def finder(self, texts: list, k=1):
        embed_queries = self.model(texts)
        inds = get_top_k_sim(self.index, embed_queries, k)
        relev_docs = np.array(self.loaded_labels)[inds]
        print(relev_docs)
        print(self.loaded_labels)
        print(inds)
        return relev_docs
    



