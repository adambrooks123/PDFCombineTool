# PDFCombineTool
A simple program use to for typical situation. 

## What is this tools:

This tool is a simple Python program based on `pyPDF4` and `reportLab` to improve the working effeciency when handling multiple PDF files. 

## When to use this tool?

There are cases in the daily working that requires to handle multiple PDF files. The background for this program is that: There're thousands of PDFs that requires to generate a unique COVERPAGE based on its title, print the coverpage, fill different things on the coverpage, scann the pages and then combine the coverpage to the original PDF files. Those process could spends several hours, but with this tool, the time required was limited to the time to print/ fill/ scan. 

## How to use this tool?

The necessary packages and user instructions could be found in `fileCombine.py`. Please followed all the aspects to make sure the program could run smoothly. And the help functons were moved to `relatedHelper.py`, modify the functions inside for more personalised experience. 

**Sample:**

1. Put the original files inside the folder and modify the `fileCombine.py` file. The sample files was shown below: 
    ![Origin](/Pics/step1.png)

2. Run the `fileCombine.py` file and choose 1 when prompt, the prompt is:
    ![Prompt](/Pics/prompt.png)

    When the program finished, the generated files should be inside the destinaion folder: 
    ![Changed](/Pics/step1_end.png)

    The generated cover page look like this: 
    ![Cover](/Pics/generatedfile.png)

3. Run the `fileCombine.py` file again and select 2 if the generated files needs to be combined to each files. 

-----------------------------------------------------------------------------------------------
Hope this program could help you! 

Adam @ 23/MAR/2021
