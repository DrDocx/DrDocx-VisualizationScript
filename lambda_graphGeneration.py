import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import json
import boto3
import io

_decodedJson = ""
_bucketName = ""

def lambda_handler(event, context):
    ingestDataFile(event)


def ingestDataFile(event):
    print(":Status: Ingesting Data File")
    global _decodedJson
    global _bucketName
    
    s3 = boto3.client('s3')

    record = event['Records'][0]
    _bucketName = record['s3']['bucket']['name']
    key = (record['s3']['object']['key'])
    tmpkey = key.replace('/', '')

    _file = s3.get_object(Bucket = 'doctordocx-patientdata', Key = tmpkey)
    _data = _file['Body'].read()
    _decodedJson = json.loads(_data)

def generateChart():
    global DEBUG
    global SHOWCHART
    global BOGUSVALS
    global PAGECOUNT
    global _count
    global _decodedJson

    print(":Status: Generating Graphs")

    _categories = []
    for _key in _decodedJson.keys():
        _categories.append(_key)

    if DEBUG:
        print("Categories: ")
        print(_categories)

    _xList = []
    _yList = []
    _colors = []

    for _cat in _categories:
        _xList.append(r"$\bf{" + str(_cat.replace(" ", "\ ")) + "}$") #magic, don't touch
        _yList.append(0)
        _colors.append('black')

        for index in range(0, len(_decodedJson[_cat])):
            _testName = _decodedJson[_cat][index]['RelatedTest']['Name']
            _testVal = _decodedJson[_cat][index]['ZScore']
            if BOGUSVALS:
                _testVal = random.uniform(-5,5)
            _xList.append(_testName)
            _yList.append(_testVal)
            _colors.append(getColor(_testVal))

        _xList.append("")
        _yList.append(0)
        _colors.append('black')
    
    _xList.pop()
    _yList.pop()
    _colors.pop()

    while not len(_xList) % 36 == 0:
        _xList.append("")
        _yList.append(0)
        _colors.append('black')

    if DEBUG:
        print(_xList)
        print(_yList)

    PAGECOUNT = math.ceil(len(_xList) / 36.0)
    for page in range(1, PAGECOUNT + 1):
        _tmpX = _xList[0 + 36 * (page - 1): 36 * page]
        _tmpY = _yList[0 + 36 * (page - 1): 36 * page]
        _tmpcolors = _colors[0 + 36 * (page - 1): 36 * page]

        _tmpX.reverse()
        _tmpY.reverse()
        _tmpcolors.reverse()

        _count = len(_tmpX)
        _yScal = np.arange(_count)
        plt.barh(_yScal, _tmpY, color = _tmpcolors, align='center', alpha=1)
        plt.yticks(_yScal, _tmpX, rotation = 35, fontsize = 10)
        plt.xlim([-4, 4])
        plt.grid(b=True, axis = 'x')
        plt.subplots_adjust(left = 0.25)
        saveChart(page)

def getColor(_val):
    if _val < 0 and _val >= -1:
        color = 'yellow'
    elif _val < -1 and _val >= -2:
        color = 'orange'
    elif _val < -2: 
        color = 'red'
    else: 
        color = 'green'

    return color

def saveChart(pageNumber):
    global _localDir

    print("Status: Saving Graph " + str(pageNumber))

    _graphName = "graph" + str(pageNumber) + ".png"
    _placeholder = io.BytesIO()

    fig = plt.gcf()
    fig.set_size_inches(8, 10.5)
    fig.savefig(-_placeholder, tranparent=True, dpi = 300, orientation = 'portrait', pad_inches = 0)
    
    _s3 = boto3.client('s3')
    _bucket = _s3.Bucket(_bucketName)
    _bucket.put_object(Body = _placeholder, ContentType='image/png', key = _graphName)

    plt.clf()