'''
FWAF - Machine Learning driven Web Application Firewall
Author: Faizan Ahmad
Performance improvements: Timo Mechsner
Website: http://fsecurify.com
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import os
import urllib.parse
import pandas as pd

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)
    with open(filepath,'r') as f:
        data = f.readlines()
    data = list(set(data))
    result = []
    for d in data:
        d = str(urllib.parse.unquote(d))   #converting url encoded data to simple string
        result.append(d)
    return result

#badQueries = loadFile('badqueries.txt')
#validQueries = loadFile('goodqueries.txt')
badQueries = loadFile('bq.txt')
validQueries = loadFile('gq.txt')

badQueries = list(set(badQueries))
validQueries = list(set(validQueries))
allQueries = badQueries + validQueries
yBad = ["Bad" for i in range(0, len(badQueries))]  #labels, 1 for malicious and 0 for clean
yGood = ["God" for i in range(0, len(validQueries))]
y = yBad + yGood
queries = allQueries

vectorizer = TfidfVectorizer(min_df = 0.0, analyzer="char", sublinear_tf=True, ngram_range=(3,3)) #converting data to vectors
X = vectorizer.fit_transform(queries)

cuantas = len(vectorizer.get_feature_names())
print (cuantas)

Datas = pd.DataFrame(X.toarray(),  columns=range(cuantas) )
labels = pd.DataFrame(y)

Datas['label'] = labels

print(Datas.shape)

Datas.to_csv('dataset.csv')

badCount = len(badQueries)
validCount = len(validQueries)

