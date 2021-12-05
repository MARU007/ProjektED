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
   
 
uploaded_file = st.file_uploader("Wybierz plik")

def load_data():
    df = pd.read_csv(uploaded_file, sep='\t', comment='#') 
    return df

df1 = load_data()

df = df1.copy()

class_col_name = df.columns[-1] 
classes_list = df[class_col_name].unique().tolist()
column_list = df.columns[0:-1]

st.subheader("Dane")
st.dataframe(df)

listCountObj = []
list_point_cut = []

count=0

st.write("column_list")
st.write(column_list)
flag=True
while flag:
  countObj = CountObj(0, None, None, None)
 
  for one_class in column_list:
    df1 = df1.sort_values(by=[one_class])
    st.write("df1 "+str(one_class))
    st.write(df1) 
    count=0
    for index, beginning_record in df1.iterrows():

      # st.write("df1[class_col_name].iloc[0]")
      # st.write(df1[class_col_name].iloc[0]) 
      # st.write("beginning_record")
      # st.write(beginning_record[class_col_name]) 

      if (df1[class_col_name].iloc[0]==beginning_record[class_col_name]):
        count=count+1 
        previous_record = beginning_record
      else:
        if(countObj.count<count):     
          mean_points = (beginning_record[one_class]+previous_record[one_class])/2.0
          countObj = CountObj(count, one_class, "beginning", mean_points) 
          count=0
        break
    count=0
    for index,end_record in df1.iterrows():
      if (df1[class_col_name].iloc[-1]==end_record[class_col_name]):
        count=count+1
        previous_record = end_record
      else:
        if(countObj.count<count):
          mean_points = (end_record[one_class]+previous_record[one_class])/2.0
          countObj = CountObj(count, one_class, "end", mean_points) 
          count=0
        break
  st.write("Klasa dla ktorej usuwamy")
  st.write(countObj.name_class)
  st.write("Ile usunelo:")
  st.write(countObj.count)
  st.write("Punkt przez ktory tniemy:")
  st.write(countObj.mean_points)

  if(countObj.count<=0): break
  if(countObj.side=="beginning"):
    df1.sort_values(by=[countObj.name_class])
    df1 = df1.drop(df1.index[range(countObj.count)])
    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))
  else:
    df1.sort_values(by=[countObj.name_class])  
    df1 = df1.drop(df.tail(countObj.count).index,inplace=True)
    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))
  listCountObj.append(countObj)

  if(len(df1.columns)==3):
    col_a = df1.columns[0]
    col_b = df1.columns[1]
    plot_class =  df1.columns[2]
    fig, ax = plt.subplots()

    df1.plot(kind='scatter',x=col_a, y=col_b,ax=ax)

    for line_point in list_point_cut:
      
      
      if(col_a==line_point.name_class):
        x1, y1 = [line_point.value, line_point.value], [df[line_point.name_class].min(), df[line_point.name_class].max()]
        ax.plot( x1, y1, color='red')

      else:
        x1, y1 =  [df[line_point.name_class].min(), df[line_point.name_class].max()], [line_point.value, line_point.value]
        ax.plot( x1, y1, color='blue')
  #st.pyplot(fig)



st.write("Test!!!!!!!!!!!!!!!!!!!")

if(len(df1.columns)==3):
  col_a = df1.columns[0]
  col_b = df1.columns[1]
  plot_class =  df1.columns[2]
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






