###################################################
#     Functions that support the fileCombie.py     #
#            Adam @ 19/ MAR/ 2021                 #
###################################################

'''
Includes 4 functions: fileIDModifier, createPDF, merge_pdfs, merge_pages
Modify: fileIDModifier for changes related to naming rules
        createPDF for changes related to cover pages [CONTENT, LAYOUT, etc]
        merge_pdfs for changes related to the order of combine pdfs
        merge_pages for the changes related to the cover page order[Front/ End]
'''


# Import the necessary packages 
import os, re
from PyPDF4 import PdfFileReader, PdfFileWriter, PdfFileMerger
from shutil import copy2
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.pagesizes import  A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Spacer
from reportlab.lib.units import inch
# Change 'simsun.ttf' to the path of the font file if can't open the file
pdfmetrics.registerFont(TTFont('song', 'simsun.ttf'))

def fileIDModifier(path, des_path, changeDirectly, showProcess):
    '''
    Function used to change the fileName with unique ID. 

    :type path: String, the folder path
    :type des_path: String, the destionation folder path
    :type changDirectly: Bool, True to change the filename directly
    :type showProcess: Bool, True to show the detailed name change process
    :rtype: None
    '''
    print("===========<FILE NAME ID ADD START>===========")
    print("PROCESSING.....")

    if not os.path.exists(des_path):
        os.makedirs(des_path)

    fileList = os.listdir(path)

    id = 1
    total = 0
    successCount = 0
    errFile = []

    for fileName in fileList:
        oldName = path + os.sep + fileName
        newName = "%05d"%id + '-' +  fileName
        total += 1

        if oldName[-4:] == '.pdf':
            if changeDirectly:
                os.rename(oldName, newName)
            else:
                copy2(oldName, os.path.join(des_path, newName))
            successCount += 1

            if showProcess:
                print(oldName, ' ------> ', newName)
                print(str(total) + 'File has Processed.')
                print('-'*25)
                
            id += 1
        else:
            errFile.append(fileName)

    # Job Summary & Error Report
    if showProcess and errFile:
            print("ERROR FILE NAMES:")
            for names in errFile:
                print(names)
    print("===========<FILE NAME ID ADD COMPLETED>===========")
    print('{} files has been processed. {} name changed; {} unchanged. '.format(total, successCount, len(errFile)))
    print("="*40)


def createPDF(names, destination, showProcess):
    '''
    Function uses to create separate cover pages based on its filename. 

    :type originName: String, the name of the file (without '.pdf')
    :type destination: String, the destination folder path
    :rtype: None
    '''
    
    print("===========< COVER PAGE GENERATION START >===========")
    print("PROCESSING.........")

    total = 0

    for name in names:
        if showProcess: print("Processing - {}".format(name))
        originName = name[:-4]

        Style = getSampleStyleSheet()
        fileElements = []
        id = ''

        if re.search(r'[0-9]{5}-', originName):
            id = originName[:5]
            originName = originName[6:]

        text1 = '<para><font face = "song"> '+ originName +' </font></para>'
        text2 = '<para align = "right"><font face = "song"> #CONTENT# </font></para>'
        text3 = '<para align = "right"><font face = "song"> #CONTENT# </font></para>'

        fileElements.append(Paragraph(text1, Style['Heading2']))
        fileElements.append(Spacer(1, 1.5*inch))
        fileElements.append(Paragraph(text2, Style['Heading2']))
        fileElements.append(Paragraph(text3, Style['Heading2']))

        if not id:
            newName = originName + '.pdf'
        else:
            newName = id + '.pdf'
        
        destName = os.path.join(destination, newName)

        pdf = SimpleDocTemplate(destName, pagesize = (A4[0], A4[1]), topMargin = 30, bottomMargin = 30)
        pdf.multiBuild(fileElements)
        total += 1

    print("===========< COVER PAGE GENERATION COMPLETED >===========")
    print("{} files has been processed.".format(total))
    print("=" * 40)



def merge_pdfs(path, names, output, showProcess):
    '''
    Function that used to merge various of pdf files
    CITED FROM https://www.jianshu.com/p/932b701055e5

    :type path: String, the path that stored the pdf files
    :type names: String, the names that requried to be processed (without '.pdf')
    :rtype output: List[String], return the list of paths that created for merge purpose
    '''
    print("===========< MERGE COVER PAGE START >===========")
    print("PROCESSING.........")
    total = 0
    pdf_writer=PdfFileWriter()
    for name in names:
        total += 1
        if showProcess: print("COPYING - {}".format(name))
        namePath = os.path.join(path, name[:5] + '.pdf')
        pdf_reader=PdfFileReader(namePath)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
        os.remove(namePath)
        if showProcess: print("DELETING - {}".format(name))
    with open(output,'wb') as out:
        pdf_writer.write(out)
    
    print("===========<MERGE COVER PAGE COMPLETED>===========")
    print("{} files has been processed.".format(total))
    print("=" * 25)


def merge_pages(path, names, singleFile, showProcess, order = 0):
    '''
    Function uses to merge the scanned file to other pdf files based on its ID

    :type path: String, the folder that contains the files
    :type names: String, the names that included in the path (with '.pdf')
    :type singleFile: String, the name of the scanned file (with '.pdf')
    :type order: int, set to other if want to add the page to the end of each file 
    :rtype: None
    '''

    print("===========< MERGE BASED ON ID START >===========")
    print("PROCESSING......")
    errList = []
    total = 0
    errCount = 0
    scannedFileReader = PdfFileReader(os.path.join(path, singleFile))
    for page in range(scannedFileReader.getNumPages()):
        for name in names:
            if re.match(r'[0-9]{5}',name[:5]):
                if int(name[:5])-1 == page:
                    namePath = os.path.join(path, name)
                    pdfWriter = PdfFileWriter()
                    fileReader = PdfFileReader(namePath)
                    if showProcess: print("COPYING - {} - ID {}".format(name, page))

                    if order == 0: pdfWriter.addPage(scannedFileReader.getPage(page))

                    for i in range(fileReader.getNumPages()):
                        pdfWriter.addPage(fileReader.getPage(i))
                    
                    if order != 0: pdfWriter.addPage(scannedFileReader.getPage(page))

                    if showProcess: print("DELETING - {} - ID {}".format(name, page))
                    os.remove(namePath)
                    
                    try:
                        with open(namePath, 'wb') as out:
                            pdfWriter.write(out)
                    except Exception as e:
                        print("ERROR WITH ID {}".format(page))
                        errCount += 1
                        errList.append(name)
                    total += 1

    print("===========<MERGE BASED ON ID COMPLETED>===========")
    print("{} files has been processed.".format(total))
    if errCount != 0: 
        print("--->{} ERROR FILE -> ".format(errCount))
        for item in errList: print(item)
    print("=" * 40)


#######################################################################################################3
PROMPT = "请输入您所需要进行的步骤【输入序号即可】：\n   \
      1 -> 将原文件夹中的文件编号，并生成COVERPAGE，储存在‘merged.pdf’中 \n   \
      2 -> 将‘merged.pdf’页面与文件按顺序合成【请确保其均在同一文件夹内】"

PROMPT_ENG = "Please Input the STEP needs to be processed: [Input 1 or 2]\n \
      1 -> Create the Identifier Number for the files and generate COVER PAGE, Stored in 'merged.pdf' \n \
      2 -> Combine the 'merged.pdf' with the other files based on its identifier number [Ensure they all in same folder]"
