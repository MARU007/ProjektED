from os import linesep
import streamlit as st
import pandas as pd
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.lines as lines

class CountObj:
  def __init__(MyCountObj, count, name_class, side, mean_points):
    MyCountObj.count = count
    MyCountObj.name_class = name_class
    MyCountObj.side = side
    MyCountObj.mean_points = mean_points #mean between points
    
 
class CutOffPointObj:
  def __init__(MyCutOffPointObj, value, name_class):
    MyCutOffPointObj.value = value
    MyCutOffPointObj.name_class = name_class
   
def xor(df1, name_class1, name_class2):
  df1[class_col_name].iloc[-1]
  return False 

uploaded_file = st.file_uploader("Wybierz plik")

def load_data():
    df = pd.read_csv(uploaded_file, sep='\t', comment='#') 
    return df

df1 = load_data()

df = df1.copy()
df2 = df1.copy()

class_col_name = df.columns[-1] 
classes_list = df[class_col_name].unique().tolist()
column_list = df.columns[0:-1]

st.subheader("Dane")
st.dataframe(df)

listCountObj = []
list_point_cut = []

count=0

st.write("Lista kolumn - column_list")
st.write(column_list)

flag=True
isXor=0

while flag:

  countObj = CountObj(0, None, None, None)
  for one_class in column_list:

    count=0
    df1 = df1.sort_values(by=[one_class])
    st.write("df1 - class: "+str(one_class))
    st.write(df1) 

    for index, beginning_record in df1.iterrows():

      st.write("beginning_record[one_class]:")
      st.write(beginning_record[one_class]) 
      st.write("isXor:")
      st.write(isXor) 

      if (df1[class_col_name].iloc[0]==beginning_record[class_col_name]):
        count=count+1 
        previous_record = beginning_record  

        st.write("Count dla beginning_record: ")
        st.write(count) 
      else:
        if(beginning_record[one_class]!=previous_record[one_class] or count>1):    
          if(countObj.count<count): 
            mean_points = (beginning_record[one_class]+previous_record[one_class])/2.0
            countObj = CountObj(count, one_class, "beginning", mean_points) 
            count=0 
            st.write("Średnia wartośc (beginning):")
            st.write(mean_points)
            st.write("Count (beginning):")
            st.write(countObj.count)
        else:       
          if(count==2):
            isXor=isXor+1
        break

    count=0

    for index,end_record in df1.iloc[::-1].iterrows():

      st.write("end_record[one_class]:")
      st.write(beginning_record[one_class]) 
      st.write("isXor:")
      st.write(isXor) 

      if (df1[class_col_name].iloc[-1]==end_record[class_col_name]):       
        count=count+1
        previous_record = end_record

        st.write("Count dla beginning_record: ")
        st.write(count) 

      else:
        if(end_record[one_class]!=previous_record[one_class] or count>1):
          if(countObj.count<count):
            mean_points = (end_record[one_class]+previous_record[one_class])/2.0
            countObj = CountObj(count, one_class, "end", mean_points) 
            count=0

            st.write("Średnia wartośc (end_record):")
            st.write(mean_points)
            st.write("Count (end_record):")
            st.write(countObj.count)

        else:          
          if(count==2):
            isXor=isXor+1
            toDelete=index
  
        break

  
  st.write("XOR")
  st.write(isXor)
  st.write((len(df.columns)-1)*2)
  if(isXor==(len(df.columns)-1)*2):
    df1.drop(index=toDelete,inplace=True)
    isXor=0
    st.write("!!!!!!!!XOR!!!!!!!!")
    continue
  else:
    isXor=0
  st.write("Klasa dla ktorej usuwamy")
  st.write(countObj.name_class)
  st.write("Ile usunelo:")
  st.write(countObj.count)
  st.write("Punkt przez ktory tniemy:")
  st.write(countObj.mean_points)

  if(countObj.count<=0): break
  if(countObj.side=="beginning"):
    df1=df1.sort_values(by=[countObj.name_class])
    st.write("Usuwam to: ")
    st.write(df1.head(countObj.count))
    df1.drop(df1.index[range(countObj.count)],inplace=True)

    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))
  else:
    df1=df1.sort_values(by=[countObj.name_class], ascending = False)  
    st.write("Usuwam to: ")
    st.write(df1.head(countObj.count))

    df1.drop(df1.index[range(countObj.count)],inplace=True)
    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))
  listCountObj.append(countObj)

  # if(len(df1.columns)==3):
  #   col_a = df1.columns[0]
  #   col_b = df1.columns[1]
  #   plot_class =  df1.columns[2]
  #   fig, ax = plt.subplots()

  #   df1.plot(kind='scatter',x=col_a, y=col_b,ax=ax)

  #   for line_point in list_point_cut:
      
      
  #     if(col_a==line_point.name_class):
  #       x1, y1 = [line_point.value, line_point.value], [df[line_point.name_class].min(), df[line_point.name_class].max()]
  #       ax.plot( x1, y1, color='red')

  #     else:
  #       x1, y1 =  [df[line_point.name_class].min(), df[line_point.name_class].max()], [line_point.value, line_point.value]
  #       ax.plot( x1, y1, color='blue')
  #st.pyplot(fig)



st.write("Test!!!!!!!!!!!!!!!!!!!")

if(len(df.columns)==3):
  col_a = df.columns[0]
  col_b = df.columns[1]
  plot_class =  df.columns[2]
  fig, ax = plt.subplots()

   
  df.plot(kind='scatter',x=col_a, y=col_b,ax=ax)

  st.write(list_point_cut)
  for line_point in list_point_cut:
    st.write(line_point.name_class)
  
    if(col_a==line_point.name_class):
      x1, y1 = [line_point.value, line_point.value], [df[line_point.name_class].min(), df[line_point.name_class].max()]
      ax.plot( x1, y1, color='red')

    else:
      x1, y1 =  [df[line_point.name_class].min(), df[line_point.name_class].max()], [line_point.value, line_point.value]
      ax.plot( x1, y1, color='blue')

    
st.pyplot(fig)






