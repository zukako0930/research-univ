
# coding: utf-8

# # クラスを作る

# In[ ]:
import numpy as np
import pandas as pd

class brand:
    def __init__(self,filename):
        self.filename=filename
        self.lines=self.read_file(filename)
        self.Coordinates=self.make_Coordinate()
        self.brandset=self.make_brandset()
        self.brand_dict=self.make_dict()
        self.W=self.brand_to_dictnum()
    
    #dictionary型に変換する関数
    def two_list_to_dict(self,key_list, val_list):
          return dict(zip(key_list, val_list))
    
    def read_file(self,filename):
        with open('./data/'+str(filename),'r',encoding='utf8') as fbrand:
            txt=fbrand.read() 
            lines = txt.split("\n")
            return lines
        
    def make_Coordinate(self):
        Coordinate=[]
        #重複のない辞書にするためにsetを用いる
        s=set()
        #lines=self.lines
        for line in self.lines:
            brands=line.split(",")
            Coordinate.append(brands)
        return Coordinate
    
    def make_brandset(self):
        #重複のない辞書にするためにsetを用いる
            s=set()
            for line in self.lines:
                brands=line.split(",")
                for brand in brands:
                    s.add(brand)
            brand_set=list(s)
            print(len(brand_set))
            return brand_set
    
    def make_dict(self):
        #dictionaryのindex
        index=[]
        for i in range(len(self.brandset)):
            index.append(i)
        #辞書
        brand_dict=self.two_list_to_dict(self.brandset,index)
        return brand_dict
    
    def brand_to_dictnum(self):
        W = [] # words
        #ブランドと補助情報の文書ごとのリストを作る
        for Coordinate in self.Coordinates:
        #list()をつけない場合iterator objectが帰ってくる
            W.append(list(map(lambda v:self.brand_dict[v],Coordinate)))
        return W
    
    def brand_to_topic(self, nctm_Z): #nctm.Zはnctm.fitの結果が入っている
        brand_topic=[]
        for brands, Topics in zip(self.Coordinates,nctm_Z):
            for brand,Topic in zip(brands,Topics):
                pair=[brand,Topic]
                brand_topic.append(pair)
        return brand_topic
    
    def brand_topic_list_f(self,brand_topic,K):
        brand_topic_list=[]
        for i in range(K):
            aaa=[x for x in brand_topic if x[1] == i]
            #print(aaa)
            brand_topic_list.append(aaa)
        return brand_topic_list
    
    def t_setlist_brand_f(self,brand_topic_list,K):
        #brandについて
        t_setlist_brand=[] #各トピックごとのbrandのsetを代入するリスト
        for i in range(K): #各トピックで回す
            a=[] #各トピックでsetを作るためのローカル変数
            for item in brand_topic_list[i]:
                a.append(item[0])
            a=set(a) #セットにする
            a=list(a) #リストに直す
            t_setlist_brand.append(a) #現在のトピックのsetをグローバルのリストに追加
        #print(t_setlist[0]) 
        return t_setlist_brand
    
    def count_topic_f(self,brand_topic_list,t_setlist_brand,K):
        count_topic=[] #全トピックの出現回数リストのリスト
        for i in range(K): #トピックループ
            count=np.zeros((len(t_setlist_brand[i]))) #今見ているトピックのsetの長さ分のbrandカウント配列を初期化
            for item in brand_topic_list[i]: #itemはリスト
                count[t_setlist_brand[i].index(item[0])]+=1 #今見ているbrandのインデックスをカウントアップ
            count_topic.append(count) #一つのトピックについて見終えたらグローバルに追加
        return count_topic
    
    def write_result(self,t_setlist_brand,count_topic):
        topic_num=0
        for item,count in zip(t_setlist_brand,count_topic):
            tuples=[]
            for b,c in zip(item,count):
                tuples.append(tuple((b,c)))
            tuples.sort(key=lambda x:x[1],reverse=True) #x[1]に出現回数が入っているので多い順にソート
            df=pd.DataFrame(tuples)
            if topic_num < 10:
                df.to_csv( './result/topic'+'0'+str(topic_num)+str(self.filename), index=False )
            else:
                df.to_csv( './result/topic'+str(topic_num)+str(self.filename), index=False )
            topic_num+=1
        print("END")