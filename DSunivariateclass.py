import pandas as pd
import numpy as nm

class univariate():
   
        def quan_qual(dataset):
            quan_columns=[] #to store quantitative data
            qual_columns=[] #to store qualitative data
            for columnName in dataset.columns:
                if(dataset[columnName].dtypes=='O'):
                    qual_columns.append(columnName)
                else:
                    quan_columns.append(columnName)
            return quan_columns,qual_columns

        def datasetdescribe(dataset,quan_columns):
            dataset_describe=pd.DataFrame(index=["MEAN","MEDIAN","MODE","Q1","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR",
                                          "1.5Rule","Lesser_Outlier_Range","Greater_Outlier_Range","Min","Max"],columns=quan_columns)
            for columnName in dataset_describe.columns:
                dataset_describe.loc["MEAN",columnName]=dataset[columnName].mean()
                dataset_describe.loc["MEDIAN",columnName]=dataset[columnName].median()
                dataset_describe.loc["MODE",columnName]=dataset[columnName].mode()[0]
                dataset_describe.loc["Q1",columnName]=nm.percentile(dataset[columnName],25)  #Because salary having null values, NAN coming for salary
                dataset_describe.loc["Q1:25%",columnName]=dataset.describe()[columnName]["25%"]
                dataset_describe.loc["Q2:50%",columnName]=dataset.describe()[columnName]["50%"]
                dataset_describe.loc["Q3:75%",columnName]=dataset.describe()[columnName]["75%"]
                dataset_describe.loc["Q4:100%",columnName]=dataset.describe()[columnName]["max"]
                dataset_describe.loc["IQR",columnName]= dataset_describe.loc["Q3:75%",columnName]-dataset_describe.loc["Q1:25%",columnName]
                dataset_describe.loc["1.5Rule",columnName]=1.5*dataset_describe.loc["IQR",columnName]
                dataset_describe.loc["Lesser_Outlier_Range",columnName]=dataset_describe.loc["Q1:25%",columnName]-dataset_describe.loc["1.5Rule",columnName]
                dataset_describe.loc["Greater_Outlier_Range",columnName]=dataset_describe.loc["Q3:75%",columnName]+dataset_describe.loc["1.5Rule",columnName]
                dataset_describe.loc["Min",columnName]=dataset[columnName].min()
                dataset_describe.loc["Max",columnName]=dataset[columnName].max()
                dataset_describe.loc["skew",columnName]=dataset[columnName].skew()
                dataset_describe.loc["kurtosis",columnName]=dataset[columnName].kurtosis() 
                dataset_describe.loc["Var",columnName]=dataset[columnName].var()
                dataset_describe.loc["Std_Deviation",columnName]=dataset[columnName].std()
            return(dataset_describe)

        
      
        def identifyoutlier(dataset_describe,quan_columns):
            lesser_outlier=[]
            greater_outlier=[]
            for columnName in quan_columns:
                if(dataset_describe[columnName]["Min"]<dataset_describe[columnName]["Lesser_Outlier_Range"]):
                    lesser_outlier.append(columnName)
                if(dataset_describe[columnName]["Max"]>dataset_describe[columnName]["Greater_Outlier_Range"]):
                    greater_outlier.append(columnName)
            return(lesser_outlier,greater_outlier)


        def replaceoutlier(dataset,dataset_describe,lesser_outlier,greater_outlier):
           
            for columnName in lesser_outlier:
                dataset.loc[
                    dataset[columnName] < dataset_describe.loc["Lesser_Outlier_Range", columnName],
                    columnName
                ] = dataset_describe.loc["Lesser_Outlier_Range", columnName]
            
            
            for columnName in greater_outlier:
                dataset.loc[
                    dataset[columnName] > dataset_describe.loc["Greater_Outlier_Range", columnName],
                    columnName
                ] = dataset_describe.loc["Greater_Outlier_Range", columnName]    
               


        
        
            
        def freqtable(dataset,quan_columns):
            
            for columnName in dataset[quan_columns]:
                freqTable=pd.DataFrame(columns=["Unique_values","Frequency","Relative_frequency","Cumsum"])
                print(columnName)
                freqTable["Unique_values"]=dataset[columnName].value_counts().index
                freqTable["Frequency"]=dataset[columnName].value_counts().values
                freqTable["Relative_frequency"]=dataset[columnName].value_counts().values
                freqTable["Cumsum"]=freqTable["Relative_frequency"].cumsum()
                print(freqTable)
                
