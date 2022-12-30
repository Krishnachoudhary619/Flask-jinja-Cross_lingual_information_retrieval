from flask import Flask,render_template,request
import convert
import translators as ts
import translators.server as tss

app = Flask(__name__)
list_docs=["hello how are you","welcome to mithibai college"]

con_list_docs=[]
for i in list_docs:
    con_list_docs.append(convert.con(i))

dt_query="none"


@app.route('/')
def hello_world():
    return render_template('index.html')
    # return 'Hello, World!'

@app.route('/dt',methods=["GET","POST"])
def doc_trans():
    if request.method=="POST":
        dt_query=request.form['query']
        result=[]
        result_doc=[]
        q_list=dt_query.split()
        
        for i in q_list:
            count=0
            for j in list_docs:
                list_j=j.split()
                for k in list_j:
                    if i==k:
                        result.append(j)
                        result_doc.append(count)
                        break
                count+=1
       
        return render_template("new_doc_trans.html",docs=con_list_docs,dt_query=dt_query,con_docs=list_docs,result_doc=result_doc,result=result)
    else:
        dt_query="none"
        return render_template("new_doc_trans.html",docs=con_list_docs,dt_query=dt_query)

@app.route('/qt',methods=["GET","POST"])
def query_trans():
    if request.method=="POST":
        dt_query=convert.con(request.form['query'])
        result=[]
        result_doc=[]
        q_list=dt_query.split()
        
        for i in q_list:
            count=0
            for j in con_list_docs:
                list_j=j.split()
                for k in list_j:
                    if i==k:
                        result.append(list_docs[count])
                        result_doc.append(count)
                        break
                count+=1


        return render_template("new_query_trans.html",docs=con_list_docs,dt_query=dt_query,result_doc=result_doc,result=result)
    else:
        dt_query="none"
        return render_template("new_query_trans.html",docs=con_list_docs,dt_query=dt_query)

    

@app.route('/pt',methods=["GET","POST"])
def pivot_lang():
    if request.method=="POST":
        dt_query_og=request.form['query']
        dt_query=tss.google(dt_query_og, from_language='fr', to_language='en')
        print(dt_query)

        result=[]
        result_doc=[]
        q_list=dt_query.split()
        
        for i in q_list:
            count=0
            i=i.lower()
            for j in list_docs:
                list_j=j.split()
                for k in list_j:
                    if i==k:
                        result.append(j)
                        result_doc.append(count)
                        break
                count+=1

        french_result=[]
        for i in result:
            french_result.append(tss.google(i, from_language='en', to_language='fr'))
        result=french_result.copy()
        print(french_result)
        return render_template("pivot_trans.html",docs=con_list_docs,dt_query=dt_query,result_doc=result_doc,result=result,eng_docs=list_docs)
    else:
        dt_query="none"
        return render_template("pivot_trans.html",docs=con_list_docs,dt_query=dt_query)
    

if __name__=="__main__":
    app.run(debug=True)

 