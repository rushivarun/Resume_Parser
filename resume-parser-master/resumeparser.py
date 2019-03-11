from flask import Flask
from functiona import extract_name
from functiona import extract_phone_numbers
from functiona import extract_email_addresses
from functiona import extract_information
from functiona import convert 
import csv
import numpy as np
import json
from flask import flash, request, redirect, url_for
import os


app = Flask(__name__)


UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        with open('techatt.csv', 'rb') as f:
            reader = csv.reader(f)
            your_listatt = list(reader)
        with open('techskill.csv', 'rb') as f:
            reader = csv.reader(f)
            your_list = list(reader)
        with open('nontechnicalskills.csv', 'rb') as f:
            reader = csv.reader(f)
            your_list1 = list(reader)
        #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
        s = set(your_list[0])
        s1 = your_list
        s2 = your_listatt
        skillindex = []
        skills = []
        skillsatt = []
        #Converting pdf to string
        resume_string = convert(file.filename)
        resume_string1 = resume_string
        #Removing commas in the resume for an effecient check
        resume_string = resume_string.replace(',', ' ')
        #Converting all the charachters in lower case
        resume_string = resume_string.lower()
        #Information Extraction Function

        y = extract_phone_numbers(resume_string)
        y1 = []
        for i in range(len(y)):
            if(len(y[i]) > 9):
                y1.append(y[i])
        email_ad = extract_email_addresses(resume_string)
        for word in resume_string.split(" "):
            if word in s:
                skills.append(word)
        skills1 = list(set(skills))
        np_a1 = np.array(your_list)
        for i in range(len(skills1)):
            item_index = np.where(np_a1 == skills1[i])
            skillindex.append(item_index[1][0])
        nlen = len(skillindex)
        s1 = set(your_list1[0])
        nontechskills = []
        for word in resume_string.split(" "):
            if word in s1:
                nontechskills.append(word)
        nontechskills = set(nontechskills)
        list5 = list(nontechskills)

        output = {
            "string_key": "aeldjalefjaepfkjpefoj",
            "phone number": y1,
            "Email": email_ad,
            "Technical_skills": skills1,
        }

        return json.dumps(output)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

    


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
