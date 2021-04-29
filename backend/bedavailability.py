import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import datetime
import os
from pytz import timezone

curr = datetime.datetime.now(timezone('Asia/Calcutta'))


headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"}
# response = requests.get("http://office.suratsmartcity.com/SuratCOVID19/Home/COVID19BedAvailabilitydetails?ftid=0", headers=headers)
# webpage = response.content

# soup = BeautifulSoup(webpage, "html.parser")
hospital = "HOSPITAL: "
hotel = "HOTEL"
chc = "CHC"
ccic = "CCIC"

# table = soup.find('table',class_="BedAvailDashboard")
# for tr in table.find_all('tr'):
#     values = [data for data in tr.find_all('td')]
#     if(values):
#         catUpdateInfo = [ updata for updata in values[0].find_all('span')]
#         category = catUpdateInfo[0]
#         hospitalData['hospitalCategory'] = catUpdateInfo[0].text
#         lastUpdatedAt = catUpdateInfo[1]
#         hospitalData['hospitalLastUpdatedAt'] =  catUpdateInfo[1].text
#         addressData = [a for a in values[0].find_all('a') ]
#         miscHospitalData = addressData[0].get('href')
#         cleanedHospitalData = miscHospitalData.split('showpopup')[1].strip('();').split("'")
#         hospitalName = cleanedHospitalData[1]
#         hospitalData['hospitalName'] = cleanedHospitalData[1]
#         hospitalAddress = cleanedHospitalData[3]
#         hospitalData['hospitalAddress'] = cleanedHospitalData[3]
#         hospitalContactNo = cleanedHospitalData[5]
#         hospitalData['hospitalContact'] = cleanedHospitalData[5]
#         totalBeds = values[1].text
#         hospitalData['hospitalTotalBeds'] = values[1].text
#         availableBeds = values[2].text
#         hospitalData['hospitalAvailableBeds'] = values[1].text
#         bedData.append(hospitalData) 
               # tr.find_all(class="hospital-info")
                               #tr.find_all(class="count-text")
bedData = []

# table = soup.find(id="accordionExample")
# if (table):
#     for tr in table.find_all(class_="custom-card"):
#         hospitalData = {}
#         hospitalVacantBedTypes = []
#         miscHospitalData = tr.find_all(class_="hospital-info")[0].get('href')
#         cleanedHospitalData = miscHospitalData.split('showpopup')[1].strip('();').split("'")
#         hospitalData['hospitalName'] = cleanedHospitalData[1]
#         hospitalData['hospitalAddress'] = re.sub('\n',"",cleanedHospitalData[3])
#         hospitalData['hospitalContact'] = cleanedHospitalData[5]
#         hospitalData['hospitalLastUpdatedAt'] = tr.find_all(class_="badge-lastupdated")[0].text.split("-")[1]
#         hospitalData['hospitalAvailableBeds'] =  tr.find_all(class_="pr-2")[0].text.split("-")[1]
#         hospitalData['hospitalTotalBeds'] = tr.find_all(class_="count-text")[0].text.split("-")[1]

#         bedtypesList = tr.find(class_="card-body").find_all('li')
#         for bedTypeCont in bedtypesList:
#             hospitalBedType = {}
#             hospitalBedType['type'] = bedTypeCont.find(class_="caption-text").text
#             hospitalBedType['available'] = bedTypeCont.find(class_="count-text").text
#             hospitalVacantBedTypes.append(hospitalBedType)

#         hospitalData['hospitalVacantBedTypes'] = hospitalVacantBedTypes
#         bedData.append(hospitalData)

#     bedData.append({"dataFrom":"http://office.suratsmartcity.com"})  
#     formattedYr =  "{}".format(curr.year)
#     formattedat = ("{}".format(curr.day),"0{}".format(curr.day))[len(str(curr.day)) < 2 ] 
#     formattedMo = ("{}".format(curr.month),"0{}".format(curr.month))[len(str(curr.month)) < 2]
#     # if(0 <= curr.minute < 15):
#     #     filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + "00" + ".json"
#     # elif 15 <= curr.minute < 30 :
#     #     filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + "15" + ".json" 
#     # elif 30 <= curr.minute < 45:
#     #     filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + "30" + ".json"
#     # else:
#     #     filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + "45" + ".json"
#     filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + ".json"
#     filePath  = "" + "{}".format(formattedYr) + "{}{}".format(os.sep,formattedMo) + "{}{}".format(os.sep,formattedat)
#     DIR_PATH = ".{}data{}".format(os.sep,os.sep) + filePath + "{}".format(os.sep)
#     DATA_PATH = DIR_PATH + filestring

#     if not os.path.isdir(DIR_PATH):
#         os.makedirs(DIR_PATH)
#     print(DATA_PATH)
#     with open('{}'.format(DATA_PATH),'w+') as f:
#         json.dump(bedData,f)
# else :
responseFromImaSurat = requests.get("https://imasurat.com/Covid-19-hospital-bed-availability", headers=headers)
webpage = responseFromImaSurat.content

soup = BeautifulSoup(webpage, "html.parser")
rows = soup.find(id="listings")
if (rows):
    for row in rows.find_all('div'):
        hospitalData = {}
        hospitalVacantBedTypes = []
        hospitalData['hospitalName'] = row.find('h5').text.strip()
        data = row.find_all('p')
        if (re.search('oxygen',data[0].text.split(":")[0])):
            hospitalBedType = {}
            hospitalBedType['type'] = "oxygen"
            hospitalBedType['available'] = re.sub('\n',"",data[0].text.split(":")[1]).strip()
            hospitalVacantBedTypes.append(hospitalBedType)  
        if (re.search('Ventilator',data[1].text.split(":")[0])):
            hospitalBedType = {}
            hospitalBedType['type'] = "Ventilator(BiPap)"
            hospitalBedType['available'] = re.sub('\n',"",data[1].text.split(":")[1]).strip()
            hospitalVacantBedTypes.append(hospitalBedType)
        
        hospitalData['hospitalVacantBedTypes'] = hospitalVacantBedTypes
        hospitalData['hospitalLastUpdatedAt'] = data[2].text.strip()        
        hospitalData['hospitalContact'] = re.sub('\r',"",re.sub('\n',"",data[3].text)).strip().split(" ")
        hospitalData['hospitalAddress'] = re.sub('\r',"",re.sub('\n',"",data[len(data)-1].text)).strip() 
        bedData.append(hospitalData)

    bedData.append({"dataFrom":"https://imasurat.com/"})    
    formattedYr =  "{}".format(curr.year)
    formattedat = ("{}".format(curr.day),"0{}".format(curr.day))[len(str(curr.day)) < 2 ] 
    formattedMo = ("{}".format(curr.month),"0{}".format(curr.month))[len(str(curr.month)) < 2]
    filestring = "" +  formattedat + formattedMo + formattedYr + ("{}".format(curr.hour),"0{}".format(curr.hour))[len(str(curr.hour)) < 2 ] + ".json"
    filePath  = "" + "{}".format(formattedYr) + "{}{}".format(os.sep,formattedMo) + "{}{}".format(os.sep,formattedat)
    DIR_PATH = ".{}data{}".format(os.sep,os.sep) + filePath + "{}".format(os.sep)
    DATA_PATH = DIR_PATH + filestring

    if not os.path.isdir(DIR_PATH):
        os.makedirs(DIR_PATH)
    print(DATA_PATH)
    with open('{}'.format(DATA_PATH),'w+') as f:
        json.dump(bedData,f)       
        