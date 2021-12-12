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
vectors = df1.copy()

class_col_name = df.columns[-1] 
classes_list = df[class_col_name].unique().tolist()
column_list = df.columns[0:-1]

st.subheader("Dane")
st.dataframe(df)

listCountObj = []
list_point_cut = []

st.write("Lista kolumn - column_list")
st.write(column_list)

flag=True
isXor=0
count=0
vector_nr = 1
previous_record=[]

while flag:

  countObj = CountObj(0, None, None, None)
  for one_class in column_list:

    count=0
    df1 = df1.sort_values(by=[one_class, class_col_name])
    st.write("df1 - class: "+str(one_class))
    st.write(df1) 
    previous_record=[]
    for index, beginning_record in df1.iterrows():

      st.write("beginning_record[one_class]: "+str(beginning_record[one_class]))
      st.write("isXor: "+str(isXor))
    

      if (df1[class_col_name].iloc[0]==beginning_record[class_col_name]):
        count=count+1 
        previous_record.append(beginning_record)  

        st.write("Count dla beginning_record: "+str(count))

      else:
        previous_record_last_element = previous_record[-1]
        if(beginning_record[one_class]!=previous_record_last_element[one_class]):    
          if(countObj.count<count): 
            mean_points = (beginning_record[one_class]+previous_record_last_element[one_class])/2.0
            countObj = CountObj(count, one_class, "beginning", mean_points) 
            count=0 
            st.write("Średnia wartośc (beginning): "+str(mean_points))          
            st.write("Count (beginning): "+str(countObj.count))
            
        else:       
          if(count==1):
            isXor=isXor+1
          else:
            for previous_record_element in reversed(previous_record):
                if(beginning_record[one_class]!=previous_record_element[one_class]):    
                  if(countObj.count<count): 
                    mean_points = (beginning_record[one_class]+previous_record_element[one_class])/2.0
                    countObj = CountObj(count, one_class, "beginning", mean_points) 
                    count=0 
                    st.write("Średnia wartośc (beginning): "+str(mean_points))          
                    st.write("Count (beginning): "+str(countObj.count))
                  break
                count=count-1
        break

    count=0
    previous_record=[]
    for index,end_record in df1.iloc[::-1].iterrows():

      st.write("end_record[one_class]: "+str(beginning_record[one_class]))
      st.write("isXor: "+str(isXor))

      if (df1[class_col_name].iloc[-1]==end_record[class_col_name]):       
        count=count+1
        previous_record.append(end_record)

        st.write("Count dla end_record: "+str(count))

      else:
        previous_record_last_element = previous_record[-1]
        if(end_record[one_class]!=previous_record_last_element[one_class]):
          if(countObj.count<count):
            mean_points = (end_record[one_class]+previous_record_last_element[one_class])/2.0
            countObj = CountObj(count, one_class, "end", mean_points) 
            count=0

            st.write("Średnia wartośc (end_record): "+str(mean_points))
            st.write("Count (end_record): "+str(countObj.count))

        else:          
          if(count==1):
            isXor=isXor+1
            toDelete=index
          else:
            for previous_record_element in reversed(previous_record):
              if(end_record[one_class]!=previous_record_element[one_class]):
                if(countObj.count<count):
                  mean_points = (end_record[one_class]+previous_record_element[one_class])/2.0
                  countObj = CountObj(count, one_class, "end", mean_points) 
                  count=0

                  st.write("Średnia wartośc (end_record): "+str(mean_points))
                  st.write("Count (end_record): "+str(countObj.count))
                break
              count=count-1
        break

  
  st.write("XOR")
  st.write(isXor)
  st.write((len(df.columns)-1)*2)
  if(isXor==(len(df.columns)-1)*2):
    df1.drop(index=toDelete,inplace=True)
    df.drop(index=toDelete,inplace=True)
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

  if(countObj.count<=0 and isXor==0): break #wychodzi z gownego whila 

  if(countObj.side=="beginning"):
    df1=df1.sort_values(by=[countObj.name_class, class_col_name])
    st.write("Usuwam to: ")
    st.write(df1.head(countObj.count))
    df1.drop(df1.index[range(countObj.count)],inplace=True)

    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))
  
    vectors_list = []
    for index, row in vectors.iterrows():
      if row[countObj.name_class] >= countObj.mean_points:
        vectors_list.append(1)
      if row[countObj.name_class] < countObj.mean_points:
        vectors_list.append(0)
    vectors["w"+str(vector_nr)] = vectors_list
    vector_nr += 1

  else:
    df1=df1.sort_values(by=[countObj.name_class, class_col_name])  
    
    st.write("Usuwam to: ")
    st.write(countObj.name_class)
    st.write(df1)
    st.write(df1.tail(countObj.count))
    df1 = df1[:-countObj.count]
    #df1.drop(df1.index[range(countObj.count)],inplace=True)
    st.write(df1)
    list_point_cut.append(CutOffPointObj(countObj.mean_points, countObj.name_class))

    vectors_list = []
    for index, row in vectors.iterrows():
      if row[countObj.name_class] >= countObj.mean_points:
        vectors_list.append(1)
      if row[countObj.name_class] < countObj.mean_points:
        vectors_list.append(0)
    vectors["w"+str(vector_nr)] = vectors_list
    vector_nr += 1

  st.write(vectors)
  listCountObj.append(countObj)


st.write("Test!!!!!!!!!!!!!!!!!!!")

if(len(df.columns)==3):
  col_a = df.columns[0]
  col_b = df.columns[1]
  plot_class =  df.columns[2]
  fig, ax = plt.subplots()
  
  #we converting it into categorical data
  cat_col = df[plot_class].astype('category') 
  st.write(cat_col)
  #we are getting codes for it 
  cat_col = cat_col.cat.codes 
  st.write(cat_col)
  df.plot(kind='scatter',x=col_a, y=col_b, c=cat_col, cmap="viridis", ax=ax)

  st.write(list_point_cut)
  for line_point in list_point_cut:
    st.write(line_point.name_class)
  
    if(col_a==line_point.name_class):
      x1, y1 = [line_point.value, line_point.value], [df[col_b].min()-1, df[col_b].max()+1]
      ax.plot( x1, y1, color='red')

    else:
      x1, y1 =  [df[col_a].min()-1, df[col_a].max()+1], [line_point.value, line_point.value]
      ax.plot( x1, y1, color='blue')

    
st.pyplot(fig)






