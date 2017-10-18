
# coding: utf-8

# # クラスを作る

# In[ ]:

class brand:
    def __init__(self,filename):
        self.filename=filename
        self.lines=self.read_file(filename)
        self.Coordinates=self.make_Coordinate()
        self.brandset=self.make_brandset()
        self.brand_dict=self.make_dict()
        
    
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
    
    #dictionary型に変換する関数
    def two_list_to_dict(self,key_list, val_list):
          return dict(zip(key_list, val_list))

