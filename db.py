import faiss
import os

def get_ind_faiss(dim, name='flat.index'):
    index = None
    if os.path.exists(name):
        index = faiss.read_index(name)
    else:
        index = faiss.IndexFlatIP(dim)
    return index

def push_vectors(index, vectors, name='flat.index'):
    index.add(vectors)
    faiss.write_index(index, name)
    print(index.search(vectors, 5))
    return index


def get_top_k_sim(index, query_vec, k=2):
    D, I = index.search(query_vec, k)
    print(D)
    print(index.ntotal)
    print(index.search(query_vec, 4))
    return I

