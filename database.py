from deta import Deta

DETA_KEY = "d0ozomxnrus_hJyq2Hc1eaHnkopf9stG7FP4RaHqW6d2"

deta = Deta(DETA_KEY)

db=deta.Base("COVID_Patient")

def insert_result(docname,doc_contact,doc_quli,hospital_name,hospital_address,id,name,age,date,address,pat_contact,aadhar,remark,pred):
    db.put({
        "docname":docname,
        "doc_contact":doc_contact,
        "doc_quli":doc_quli,
        "hospital_name":hospital_name,
        "hospital_address":hospital_address,
        "id":id,
        "name":name,
        "age":age,
        "date":str(date),
        "address":address,
        "pat_contact":pat_contact,
        "aadhar":aadhar,
        "remark":remark,
        "pred":pred,
    })