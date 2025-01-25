# file: final_project
# author: Reghan Lanning rkl1@bu.edu
# description: using the CDC dataframe, build functions to filter the dataframe by race
    # create visual representations of the data, give context to the data, and run
    # a chi squared test of independence to determine significance between two
    # categorical objects
    # if __name__ == __main__ section contains the dropped Other race, the built demographic table,
    # the filtered dataframe function using race, chi-squared tests on risk factors,
    # and creating visual representations of significant variables


# imports
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.mosaicplot import mosaic
import researchpy as rp
import seaborn as sns

# let's build a function that takes a column regarding race and makes a subset of the dataframe
def filter_by_category(df, boolean_series):
    '''Takes a boolean operator of the category and creates a subset of the data
    containing only values of that category'''
    # created a filtered datafrane (df_filter) based off boolean condition of column in df
    df_filter = df[boolean_series]
    
    return df_filter # return this filtered column

def make_mosaic(df, col1name, col2name, title, xlabel):
    '''Make a mosaic plot to show distributions of categorical data'''
    # using the original dataframe, insert code to create mosaic
    mosaic(df,[col1name, col2name], title = title, axes_label=True) 
    # users can input their preferred column names, titles, and x axis labels
    plt.xlabel(xlabel) # add the label to the created mosaic
    plt.show() # show the plot with added axes
    
# lets build a function that creates descriptive statistics for the categorical data
def context_categ(df, df_fil, col_name):
    '''Takes a dataframe with categorical data and brings back relevant background statistics'''
    
    # want to develop descriptive information of the filtered dataframe I built
    # going to develop so that I can get context on the data
    print(f"In the DataFrame, {len(df_fil)}, or {(len(df_fil)/len(df))*100:.2f}% of the mothers are {col_name}.")
    # Did the maternal mortality review committee (MMRC) determine death was pregnancy related? (0=no, 1=yes)
    # proportions of pregnancy related deaths for filtered data frame    
    preg_death = df_fil['Preg_Related_Death'].value_counts(normalize=True)
    # print out desired information
    print(f"{df_fil['Preg_Related_Death'].value_counts().iloc[1]} mothers, or {preg_death.iloc[1]*100:.2f}%, had deaths attributed to a pregnancy-related cause.")
    
def do_regression(df, independent, dependent):
    '''perform an OLS regression of column identified by dependent as a
    function of the column identified by independent'''
    
    # extract columns from dataframe and save into X and Y variables


   # check if columns are valid
    if independent in df and dependent in df:
        X = df[independent]
        Y = df[dependent]
        
        # run OLS and print out regression model summary
        model = sm.OLS(Y, X).fit()
        model.summary()
        print(model.summary())
    
    # # create scatterplot of values in X and Y data series with independent variable
        plt.scatter(X, Y, color = 'blue')
        P = model.predict() # predicted values of maxtemp based off mitemp
        plt.plot(X, P, color = 'red')
        plt.title(f"{independent} and {dependent}")
        plt.xlabel(independent)
        plt.show() # shows line
  
    else: # if one of these is not a valid column name
       if independent not in df: # if x not in df
           print(f"Invalid column name `{independent}`") # print the invalid column
           print(f"Valid columns are: {df.columns}") # show columns in data frame
           
       elif dependent not in df: # if y not in df
           print(f"Invalid column name `{dependent}`") # print invalid column name
           print(f"Valid columns are: {df.columns}") # print valid columns in data frame
               
           
def chi_sq(independent, dependent):
    '''Takes two column names and runs a chi-squared test of independence 
    to determine if there is a
    significant relationship between two columns, and the 
    strength of that relationship using Phi and Cramer's V'''
    # using crosstab to view distribution of observed values
    # using test results to view chi squared test
    crosstab, test_results, expected = rp.crosstab(independent,dependent,
                                                test= "chi-square",
                                                expected_freqs= True,
                                                prop= "cell")
    print(crosstab) # print out the table
    print(test_results) # print out the results
    # chi squared distribution
    # x = np.arange(0, 20, 0.001)
    # plt.plot(x, chi2.pdf(x, df=4))

def make_barchart(df, x, y, race):
    '''Create a barchart of two different variables in a specified race and dataframe'''
    sns.countplot(x=x,hue=y,data=df) # describe where x, hue, and data come from (build into function)
    plt.title(f"{x} and {race} {y}")  # create title with variables inputted to function
    plt.show() # show the plot with the updated title
    

           
if __name__ == '__main__':
    filename = 'Maternal Mortality Dataset.csv' # call dataset
    df = pd.read_csv(filename) # read the csv file
    df = df.drop(df[df['Mat_Race'] == 3].index) # drop if value is listed as other
    # data is ready to use!
    
    # create histograms to show distributions of numerical data 
    df['Mat_Age'].hist(bins=25) # make a histogram showing distribution of patients ages
    plt.xlabel('Age in Years') # label x-axis
    plt.title('Distribution of Maternal Age') # give the plot a title
    plt.show() # show the updated plot with title and axis
    df['Mat_Age'].describe() # create relevant information about distribution
   
    df['Prepreg_BMI'].hist(bins=25)
    plt.xlabel('BMI') # label x-axis
    plt.title('Distribution of Maternal BMI Before Pregnancy') # give the plot a title
    plt.show() # show the updated plot with title and axis
    df['Prepreg_BMI'].describe() # create relevant information about distribution
    
    ## STEP ONE: DEMOGRAPHIC TABLE
    # i need df_update in the main section so i can reference df_update 
        # for tests for independence
    # each column has a different amount of categorical labels, each meaning a separate thing
        # for this reason, loops are going into main section so I can name the 
        # variables how they appear and group them into relevant categories
    # will be referencing data dictionary to build new names
    
    print("Table 1: Summary of Subject Characteristics") # make title for demographic table
    print(f"(N={len(df)}).") # include how many values are in DataFrame  
    df_update = pd.DataFrame() # make a new dataframe so current df is not changed
    
    race = [] # create race variable as an empty list
    for value in df['Mat_Race']: # for each entry in df['Mat Race']
        if value == 1: # if the mother was categorized as white (1)
            race.append('White') # add identifier into list
        elif value == 2: # if the mother was categorized as black (2)
            race.append('Black') # add identifier into list
    df_update['Race'] = race # set new column to contain information from accumulated list
    df_update['Race'].value_counts().plot.pie(title = 'Distribution by Race') # show pie chart distribution of race
    print(df_update['Race'].value_counts()) # print out relevant counts for demographic table
    
    maternal_m = [] # create maternal mortality variable into empty list
    for value in df['Preg_Related_Death']: # for each entry in Preg_Related_Death
        if value == 1: # if the mother was identified to have died from preg complication
            maternal_m.append('Yes') # add a yes to the list
        else: # if not
            maternal_m.append('No') # add a no to the list
    df_update['Maternal Mortality'] = maternal_m # set new column to contain info from accumulated list
    mm_count = df_update['Maternal Mortality'].value_counts() / len(df) # proportion of deaths in dataframe
    
    # mosaic(df_update, ['Race', 'Maternal Mortality'], title = 'Race and Maternal Mortality', axes_label=True)
    make_mosaic(df_update, 'Race', 'Maternal Mortality', 'Race and Maternal Mortality', 'Race') # make demographic mosaic
    
    hispanic = [] # create hispanic variable into empty list
    for value in df['Mat_Hispanic']: # for each value in Mat Hispanic
        if value == 1: # if mother was identified as hispanic
            hispanic.append('Yes') # add yes into list
        else: # if not
            hispanic.append('No') # add no to list 
    df_update['Hispanic'] = hispanic # create new column with information from list
    print(df_update['Hispanic'].value_counts()) # return relevant counts for demographic table
    
    age = [] # create age into empty list
    for value in df['Mat_Age']: # for each value in empty list
        if value < 35: # under 35 is considered a healthy age to have a pregnancy
            age.append('Average Age') # name these average age
        elif value >= 35: # if the value is greater than or equal to 35, CDC names it a 'geriatric pregnancy'
            age.append('Advanced Age/ Geriatric') # add advanced age into list
    df_update['Age'] = age # add new column with list information
    print(df_update['Age'].value_counts()) # print relevant counts for demographic table
 
    
    # 1=less than high school, 2=high school graduate, 3=some college, 4=bachelor's degree, 5=post bachelors)
    educ = [] # create education variable into empty list
    for value in df['Mat_Educ']: # less than high school, a hs grad, some college, a degree, or more
        if value == 1 or value == 2: # low is considered less than or only high school
            educ.append('Low') # add low into list
        elif value == 3 or value == 4 or value == 5: # high is considered some college, bachelors, and post
            educ.append("High") # add high education into list
    df_update['Education'] = educ # put list into column
    edu_count = df_update['Education'].value_counts() / len(df) # proportion of education for demographic table
    
 
    bmi = [] # create BMI variable as an empty list
    for value in df['Prepreg_BMI']: # for each value in prepreg bmi
        if value < 30: # if the value is less than 30
            bmi.append('Average') # classified as average weight
        elif value >= 30: # bmi greater than or equal to 30 is considered obese by CDC
            bmi.append('Obese') # add obese to list
    df_update['BMI'] = bmi # build new column with list information from bmi
    BMI_count = df_update['BMI'].value_counts() / len(df) # proportions of bmi for demographic table
    
    
    WIC = [] # create WIC usage during pregnancy, empty list
    for value in df['WIC_Dur_Preg']: # for each value in column
        if value == 1: # if the value is one
            WIC.append('Yes') # add yes
        elif value == 0: # if its not one
            WIC.append('No') # they did not use WIC
    df_update['WIC'] = WIC # add list into new column
    WIC_count = df_update['WIC'].value_counts() / len(df) # proportion of mothers using wic for demographics

    ## 2: PREPARE FOR TESTS OF INDEPENDENCE
    Mat_White = filter_by_category(df_update, df_update['Race'] == 'White') # create dataframe of only white moms
    Mat_Black = filter_by_category(df_update, df_update['Race'] == 'Black') # create dataframe of only black moms

    ## 3: CHI SQUARED TESTS -  to find statistically significant relationships btwn variables and MM
    print("Chi-Squared Test of Independence for White Moms:")
    # white moms, calling chi_sq function on education, wic, bmi, and age risk factors
    chi_sq(Mat_White['Education'], Mat_White['Maternal Mortality'])
    chi_sq(Mat_White['WIC'], Mat_White['Maternal Mortality'])
    chi_sq(Mat_White['BMI'], Mat_White['Maternal Mortality'])
    chi_sq(Mat_White['Age'], Mat_White['Maternal Mortality'])

    # repeat for black moms
    print()
    print("Chi-Squared Test of Independence for Black Moms:")
    # black moms, calling chi_sq function on education, wic, bmi, and age risk factors
    chi_sq(Mat_Black['Education'], Mat_Black['Maternal Mortality'])
    chi_sq(Mat_White['WIC'], Mat_White['Maternal Mortality'])
    chi_sq(Mat_Black['BMI'], Mat_Black['Maternal Mortality'])
    chi_sq(Mat_Black['Age'], Mat_Black['Maternal Mortality'])

    # call mosaic and bar chart functions to graph significant findings
    make_mosaic(Mat_White, 'Education', 'Maternal Mortality', 
                'Education and White Maternal Mortality', 'Education')
    make_barchart(Mat_White, 'Education', 'Maternal Mortality', 'White')
    make_mosaic(Mat_Black, 'Age', 'Maternal Mortality', 'Age and Black Maternal Mortality', 
                'Age')
    make_barchart(Mat_Black, 'Age', 'Maternal Mortality', 'Black')
    make_mosaic(Mat_Black, 'BMI', 'Maternal Mortality', 'BMI and Black Maternal Mortality', 
                'BMI')
    make_barchart(Mat_Black, 'BMI', 'Maternal Mortality', 'Black')

    ## OLS Regression for potential insights on these findings
    criteria = df['Mat_Race'] == 1
    dfw = df[criteria]
    do_regression(dfw, 'Mat_Educ', 'Preg_Related_Death')
    black = df['Mat_Race'] == 2
    dfb = df[criteria]
    do_regression(dfb, 'Prepreg_BMI', 'Preg_Related_Death')
    do_regression(dfb, 'Mat_Age', 'Preg_Related_Death')


    