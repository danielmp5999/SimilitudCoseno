from ast import If
from xml.etree.ElementTree import tostring


def remove_punctuation ( text ):
    forbidden = {"?", "¿", "¡", "!", ",", ".", ";", ":",'"',"%","(",")","-"}
    return "".join(c for c in text.lower() if c not in forbidden )

def remove_nums( text ):
    return "".join(c for c in text.lower() if not c.isdigit())

def remove_vacias( text ):
    palab = ['ante','a','aun','aunque','con','del','dejar','etc','estamos',
             'fin','ir','largo','mas','me','ni','pero','sino','solo','tu','tus','yo','voy',
             'el','la','los','un','que','en','de','y','al','se','por','las','su','para','no',
             'una','es','lo','como','más','fue','contra','sus','le',
             'este','quien','fueron','sobre','sin','ya','también','son','donde'
             ,'ser','hasta','si','cuando','desde','tanto','sólo','o'
             ,'él','ahora','ese','está','quienes','dijo','entre',"'",'así',
             'hay','vez','embargo']
    return " ".join(c for c in text.split() if c not in palab)

def preProcesa(linea):


    linea = remove_punctuation (linea)
    linea = remove_nums(linea)
    linea = remove_vacias(linea)
        
    """ print(linea.lower()) """
    return linea 

def repetidas(texto):
    informe = ''
    import collections

    counter = collections.Counter(texto.split())
    for palabra, cont in counter.most_common():
        texto = (f"'{palabra}' aparece {cont} {'veces' if cont > 1 else 'vez'}.")
        informe = informe + texto + "\n"
    escribe("InformeRepetidas.txt",informe)

def tfidf(corpus):
    from sklearn import feature_extraction  
    from sklearn.feature_extraction.text import TfidfTransformer  
    from sklearn.feature_extraction.text import CountVectorizer  
    informe = ''
    
    if __name__ == "__main__":  
        
        vectorizer=CountVectorizer()# Esta clase convertirá las palabras del texto en una matriz de frecuencia de palabras. El elemento de matriz a [i] [j] representa la frecuencia de palabras de la palabra j en el tipo i  
        transformer=TfidfTransformer()# La clase contará el peso tf-idf de cada palabra  
        tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))# El primer fit_transform es calcular tf-idf, el segundo fit_transform es convertir el texto en una matriz de frecuencia de palabras  
        word=vectorizer.get_feature_names()# Obtener todas las palabras en el modelo de bolsa de palabras  
        weight=tfidf.toarray()# Extraiga la matriz tf-idf, el elemento a [i] [j] representa el peso tf-idf de la palabra j en el texto de tipo i  
        for i in range(len(weight)):# Imprima los pesos de las palabras tf-idf para cada tipo de texto, el primero para atraviesa todo el texto, el segundo para facilita los pesos de las palabras bajo un cierto tipo de texto  
            texto = ("------- la salida aquí"+ str(i) + "Pesos de palabra tf-idf para texto ------" ) 
            informe = informe + texto + "\n"
            for j in range(len(word)):  
                texto = (word[j],weight[i][j])
                texto = str(texto)
                informe = informe + texto + "\n"
    escribe("InformeTFIDF.txt",informe)

def simCos(lista_noticias):
    i = 0
    j = 0
    informe = ''
    for _ in lista_noticias:
        for __ in lista_noticias:
            if(i < 50):
                cose = coseno(lista_noticias[i],lista_noticias[j])
                informe = informe + "noticia: "+ str(i) + " con noticia: " + str(j) + " " + cose + '\n'
            
            i = i + 1
        j = j + 1
        i = 0
    escribe("InformeCoseno.txt",informe)




def escribe(filename,texto):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(texto)
    
def coseno(X,Y):
    
    from nltk.corpus import stopwords 
    from nltk.tokenize import word_tokenize 
    
    
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
    
    sw = stopwords.words('spanish')  
    l1 =[];l2 =[] 
    
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    return("similarity: " + str(cosine)) 


cont = 0
bandera = 0
noticia = ''
noticias = ''
list_noticias = []
guarda = ''


with open("ProyectoF.txt",encoding="utf8") as archivo:
    for linea in archivo:
        aux = (linea)
        if((aux == '</cuerpo>\n' or aux == ' </cuerpo>\n') and bandera == 1):
            bandera = 0
            noticiaPre = preProcesa(noticia)
            noticias = noticias + noticiaPre
            guarda = guarda + num + noticiaPre + "\n"
            
            list_noticias.append(noticiaPre)
            noticia = ''
        if(bandera == 1):
            """ print(linea) """
            noticia = noticia + linea
        if(aux == '<cuerpo> \n' ):
            num = "noticia " + str(cont) + "\n"
            cont = cont + 1
            bandera = 1


print("noticias: " + str(len(list_noticias)))
escribe("InformePreprocesado.txt",guarda)
print("InformePreprocesado.txt .... done")

repetidas(noticias)
print("InformeRepetidas.txt .... done")

""" Descomentar para ejecutar TF/IDF """
tfidf(list_noticias) 

simCos(list_noticias)    
print("InformeCoseno.txt .... done")