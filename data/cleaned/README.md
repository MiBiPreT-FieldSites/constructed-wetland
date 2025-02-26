# step 1: standardize the data template based on Alraune's data template for site meassurements
I manually changed and standardized constructed wetland \(CW\) raw data excel with respect to defined MIBIREM data template for field meassurement and then, I creat the standardize and clean excel file for cw field meassurement data according to the standard example data template in mibipret repository defined by Alraune.
first, the raw data were transposed, so we have all the headings in different coulmns and the list of sampling wells in different rows.
Then, I check if all the headings are in first row, and the corresponding units are in the second rows. I deleted the other irrelevant information such as analysis \(specific number provided for each analysis\), project code, project name, report status, validate status, report date and and start date.
after, the template is fixed, then I translated all the namings from Dutch to English and make them similar to the defined naming existing in the mibirem template. 
I also deleted the headings which just were in the data for clarification, like metals

## important issue

the CW raw data excel files, has two sheets, the first sheet is related to chemical analysis and the second sheet is related to in-situ meassurements. The point is that, in the chemical andlysis sheet we have the list of "*sample description*" and in the second sheets we have the list of "*meassuring points*" and the order of these lists are different although they follow the same naming structure. So, in the standardize excel file, I consider the list and order of the wells having chemical analysis values for and then I add the in-situe meassurement values corresponding to them from the second sheet manually.

### standardization of the heading and naming from lab to mibirem template:
1- headings which just were in the data for clarification, like metals,inorganic compounds, volatile aromatics

2- DOC changed to Dissolved Organic Carbon (DOC)
3- TOC changed to Total Organic Carbon (TOC)
4- iron\(2\+\) changed to Iron II
5- Manganese (II) changed to manganese

### standardization of the units from lab to mibirem template:
1- Iron II and Mangenese units changed from mg/l to ug/l

# step 2: cleaning the data from lab to mibirem template

the numerical values of Iron II and mangense multiplied to 1000, because we changed their units from mg/l to ug/l

### standardization of the heading and naming:
1- the heading of "*coding*"was added as the first column of data set \(based on MIBIREM standard template), and then it is changed to "*sample_nr*" as defined in Alraune's standard template. In this template the naming of each sample number is based on the naming structure defined in MIBIREM standar template \("*NL\_CW\_W\_1*"\), which is different from what Alraune defined in her standard template as for example for the fisrt sampling: \(2000\-001\). 
2- "*well name*" is changed to obs_well.
3- In the defined template there are no heading for date and temperature, so I also deleted them manually from the raw data set.
4- changing the name of some contaminants and environment parameters:
 \(m\+p\)xylene changed to pm\_xylene (the naming in the standard mibirem template was not defined as one of the acceptable naming)
 o-xylene changed to o_xylene
 iron\(2\+\) changed to iron2
 manganese \(II\) changec to manganese

# step 2: cleaning the data
In this step, I should check the values of the data to see if they are in agreement with the way that data should be provided, for example check if the values for the contaminat or elctron acceptors concentration are integers (as the developed python code for analyzing these data doesn't sccept the float values for these varaiables), moreover, I should check if all the data separetd by comma and in case we have some variables that their value is lower that a defined limit \(which interpreted as non detectible\) I convert their values to zero, otherwise the code gives an error as could not convert their value to numerical value. 
