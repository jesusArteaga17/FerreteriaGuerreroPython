import re

class Valida():
    def validaNombre(self,texto):
        res=re.match(" ^ [a-zA-Z] + [a-zA-Z] + $",texto,re.I)
        return res
    def validaCorreo(self,texto):
        res=re.match("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",texto,re.I)
        return res
    def validaNumero(self,texto):
        res=re.match("^[0-9]*$",texto,re.I)
        return res
    def validaRfc(self,texto):
        res=re.match("^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$",texto)
        return res
    def validaDecimal(self,texto):
        res=re.match("^[0-9]*$|^[0-9]*\.[0-9]*$",texto)
        return res
if __name__=="__main__":
    v=Valida()
    arreglo=[1,2,3,4,6]
    for number in arreglo:
        print (v.validaNumero(str(number)))