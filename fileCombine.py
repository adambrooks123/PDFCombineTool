########################################
#        PDF File Combine Tool         #
#         Adam @ 16/ MAR/ 2021         # 
########################################
# This Program is used to generate multiple title page with given file name 
# V1.0 Add the basic function, use multiple file names and generate pdf file with pre-filled format
# V1.1 Add the function that could merge the generated to a single file
# V1.2 Add the function that add the id to the file and merge based on its id 
# V2.0 Add the function that could merge the page of merged file to separate files[Based on its id]
# V2.1 Rewrite the help functions and redo the program logic  
# V2.2 Add the ENG description and language choice option
# V2.3 Add the option that could choose the location of cover page[Start/ End]
# V2.4 Add error count for page merge

'''
# PREREQUISITION:
- Please ENSURE the following files in the same folder
    -----> simsum.ttf
    -----> generatePDF.py
- And ENSURE 'reportlab' and 'pypdf4' has been installed before use 
    -----> Use 'pip3 install reportlab' in cmd to generate 'reportlab'
    -----> Use 'pip3 install pypdf4' in cmd to generate 'pypdf4'
- And ENSURE the merged file at the same folder of the other files 
'''

# Import Necessary Pacgage 
import os
import re
import relatedHelper

# Fill the folder contains the original file
# 此处填写文件所在的文件夹位置
path = '...'

# Fill the destination folder
# 此处填写需要复制到的文件夹位置
desPath = '...'

# Change this to TRUE if use ENG prompt
# 如果需要使用英文提示，请将此处设为True
useENG = True

# Change this to 1 if want to add the cover page to the end of each file
# 如需将页面置于文件末尾，将此处设为1
coverPageLoc = 1


#####################################################################################
#####################################################################################
#####################################################################################

if useENG: print(relatedHelper.PROMPT_ENG)
else: print(relatedHelper.PROMPT)
STEP = input()
if useENG: print("Preparing Executing Step: {} \n Original Path：{} \n Destination Path：{}".format(STEP, path, desPath))
else: print("准备执行 {} \n 源文件夹位置为：{} \n 目标文件夹位置为：{}".format(STEP, path, desPath))



# Create the Destination dir if its not exist
if not os.path.exists(desPath):
    if useENG: print("=======< Destination Path NOT exist，Creating... >=======")
    else: print("=======< 目标文件夹不存在，正在创建... >=======")
    os.makedirs(desPath)

mergeFileLoc = desPath + os.sep + 'merged.pdf'

if STEP == '1':
    relatedHelper.fileIDModifier(path, desPath, False, True)
    fileList = os.listdir(desPath)
    fileList = sorted(fileList, key = lambda x: x[:5])
    relatedHelper.createPDF(fileList, desPath, True)
    relatedHelper.merge_pdfs(desPath, fileList, mergeFileLoc, True)
    if useENG: print("<---STEP 1 HAS BEEN COMPLETED--->")
    else: print("<---STEP 1 已完成--->")
elif STEP == '2':
    fileList = os.listdir(desPath)
    fileList = sorted(fileList, key = lambda x: x[:5])  
    relatedHelper.merge_pages(desPath, fileList, 'merged.pdf', True, coverPageLoc)
    if useENG: print("<---STEP 2 HAS BEEN COMPLETED--->")
    else: print("<---STEP 2 已完成--->")
else:
    if useENG: print("Input ERROR, Please Re-run the program.")
    else: print("输入错误，请重新运行程序。")
