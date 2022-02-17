import pickle
import pandas as pd

COLS = ['Title', 'Author', 'Year', 'Venue']
COL_LIMIT = 5


class Repo:
    default_path = 'papers.repo'
    default_csv = 'papers.csv'

    def __init__(self, path=None):
        self.file_path = self.default_path if path is None else path

    def load(self):
        with open(self.file_path, 'rb') as fr:
            return pickle.load(fr)

    def store(self, obj):
        with open(self.file_path, 'wb') as fw:
            pickle.dump(obj, fw)

    def format(self):
        with open(self.file_path, 'rb') as fr:
            papers = pickle.load(fr)
            paper_num = len(papers)
            datas = {COLS[0]: [], COLS[1]: [], COLS[2]: [], COLS[3]: []}
            for index in range(paper_num):
                for col in range(1, COL_LIMIT):
                    datas[COLS[col-1]].append(papers[index][col])
            df = pd.DataFrame(datas)
            df.to_csv(self.default_csv, encoding='gbk')

    def over(self):
        self.file.close()
