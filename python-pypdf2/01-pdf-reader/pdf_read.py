import PyPDF2

pdfFileObj = open('./wantprintPDF.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Print page number
#print(pdfReader.numPages) 
pageObj = pdfReader.getPage(0)

# pageObj.extractText() 
printPDF = pageObj.extractText()
print(printPDF)