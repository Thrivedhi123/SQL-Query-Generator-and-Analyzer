from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
from PIL import Image

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        for row in rows:
            print(row)
        return rows
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return ["Error in executing the query"]
    finally:
        conn.close()
   
## Define Your Prompt
prompt=[
    """
 You are an expert in converting English questions to SQL queries! The SQL database includes tables such as PUBLISHER, BOOK, BOOK_AUTHOR, LIBPROGRAM, BOOK_COPIES, CARD, and BOOK_LENDING, each with specific columns.

For example,
Example 1 - Retrieve specific details from multiple tables, such as books, authors, and programs.
The SQL command might look like this: SELECT b.bookid, b.title, b.pname, a.author_name, n.No_of_Copies, l.prgid FROM book b, book_author a, libprogram l, book_copies n WHERE b.bookid = a.bookid AND b.bookid = n.bookid AND l.prgid = n.bookid;

Example 2 - Delete records from a specific table, e.g., deleting a book with ID 3 from the BOOK table.
The SQL command would be: DELETE FROM book WHERE bookid = 3;

    1. Retrieve details of all books in the library – id, title, name of publisher, authors, number of copies in each branch, etc.
    SQL Query: SELECT b.bookid, b.title, p.pname AS publisher, GROUP_CONCAT(a.author_name) AS authors, bc.No_of_Copies AS copies FROM book b INNER JOIN publisher p ON b.pname = p.pname INNER JOIN book_author a ON b.bookid = a.bookid INNER JOIN book_copies bc ON b.bookid = bc.bookid;

    2. Get the particulars of borrowers who have borrowed more than 3 books, but from Jan 2017 to Jun 2017.
    SQL Query: SELECT DISTINCT bl.card_no, COUNT(bl.bookid) AS borrowed_books FROM book_lending bl WHERE bl.date_out BETWEEN '2017-01-01' AND '2017-06-30' GROUP BY bl.card_no HAVING COUNT(bl.bookid) > 3;

    3. Delete a book in BOOK table. Update the contents of other tables to reflect this data manipulation operation.
    SQL Query: DELETE FROM book WHERE bookid = <book_id>;

    4. Partition the BOOK table based on year of publication. Demonstrate its working with a simple query.
    SQL Query: CREATE TABLE book_2019 AS SELECT * FROM book WHERE pub_year = 2019;

    5. Create a view of all books and its number of copies that are currently available in the Library.
    SQL Query: CREATE VIEW available_books AS SELECT b.bookid, b.title, bc.No_of_Copies FROM book b INNER JOIN book_copies bc ON b.bookid = bc.bookid WHERE bc.No_of_Copies > 0;

    Feel free to ask any questions or generate various SQL queries for the library database using these prompts. Ensure that the SQL code generated does not include ``` in the beginning or end, and avoid using the word "SQL" in the output.

Feel free to generate various SQL queries for the library database using these prompts. Ensure that the SQL code generated does not include ``` in the beginning or end, and avoid using the word "SQL" in the output. You can perform CRUD operations, joins, unions, and other relational database operations on the library database.

    """
]

## Streamlit App

st.set_page_config(page_title="SQL Qury Generator")
st.header("SQL Query Generator")

question = st.text_area("Input your question or SQL query:", height=5)


submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"library.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.subheader(row)
        
def image():
        img_file_buffer = st.camera_input("Take picture of Schema Diagram")
        if img_file_buffer is not None:
            img = Image.open(img_file_buffer)   
            response = model_vis.generate_content(['''Given an image of a SQL database schema, analyze and extract relevant details such as tables, columns, relationships, 
                and any notable constraints or keys present in the schema. Provide a comprehensive understanding of the structure 
                depicted in the image.
                ''',img])
            st.write("The summary of the Schema is:")
            st.write(response.text)
            return response.text  
        
def upload():
    uplaod_img = st.file_uploader("Upload a Schema Diagram of the tables if you did'nt click a pic", type=["jpg", "png", "jpeg"])
    if uplaod_img is not None:
        img_x = Image.open(uplaod_img)
        responce = model_vis.generate_content(['''Given an image of a SQL database schema, analyze and extract relevant details such as tables, columns, relationships, 
            and any notable constraints or keys present in the schema. Provide a comprehensive understanding of the structure 
            depicted in the image.
            ''',img_x])
        st.write("The summary of the Schema is:")
        st.write(responce.text)
        return responce.text


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model_text = genai.GenerativeModel('gemini-pro')
model_vis = genai.GenerativeModel('gemini-pro-vision')

def genai_img():
    
    st.write("Upload a Schema Diagram of the tables and give the prompt to generate SQL queries.")
    text_from_image  = image() 
    text_from_uploadd = upload()
    
        
    if(text_from_image is None):
        st.write("Please take a pic or upload the schema diagram to generate")
        if(text_from_uploadd is not None):
            text_from_image = text_from_uploadd
            sql_query = st.text_input('Enter the conditons for the sql query')
            img_prompt ='''Hello user'''
            if(len(text_from_image)>0):
                response = model_text.generate_content(img_prompt+text_from_image + sql_query)
        
            st.write("The SQL query is:")
            if len(sql_query) > 0:
                st.write(response.text)
            
    else:
        sql_query = st.text_input('Enter the conditons for the sql query')
        img_prompt ='''given the details of sql schema and conditions for the query 
            Generate an optimal SQL query that effectively retrieves the desired data.
            Ensure the resulting query adheres to standard SQL syntax and is well-suited to the structure identified in the 
            image along with the specified conditions.
            '''
        if(len(text_from_image)>0):
            response = model_text.generate_content(img_prompt+text_from_image + sql_query)
        
        st.write("The SQL query is:")
        if len(sql_query) > 0:
            st.write(response.text)
            
                       
genai_img()  