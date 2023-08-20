import requests

class TimeZone():
    

    def __init__(self, city):
        self.city = city
        self.url = f"https://api.api-ninjas.com/v1/worldtime?city={self.city}"

    def request_data(self):
        response = requests.get(self.url, headers={'X-Api-Key': 'ka/g7nybqosAgLyFNCod1A==WBv07XT0PI2TrXTO'})
        if response.status_code == requests.codes.ok:
            data = response.json()
            return data
        else:
            print("api call unsuccessful")

    def dateTransform(self, string):
        months = {"01": "january", "02": "february", "03": "march", "04": "april", "05": "may" , "06": "june", "07": "july", "08": "august", "09": "september", "10": "october", "11": "november", "12": "december"}
        date = string.split("-")
        year = date[0]
        month = [v for k,v in months.items() if k == date[1]][0]
        day = date[2]
        if day[0] == "0":
            day = day[1]
        if len(day) == 1:
            if day == "1":
                day += "st"
            elif day == "2":
                day += "nd"
            elif day == "3":
                day += "rd"
            else:
                day += "th"
        else:
            if day[0] != "1":
                if day[1] == "1":
                    day += "st"
                elif day[1] == "2":
                    day += "nd"
            else:
                day += "th"
        return " ".join([day, month.title(), year])
        
    def to_dict(self):
        data = self.request_data()
        d = {}
        d["city"] = self.city.title().replace("_", " ")
        d["time24"] = data["datetime"][11:16]
        if int(d["time24"][0:2]) < 12:
            if d["time24"][0] == "0":
                time12 = d["time24"][1:5]+" AM"
            else:
                time12 = d["time24"][:5]+" AM"
        elif int(d["time24"][0:2]) == 12:
            time12 = d["time24"][:5]+" PM"
        else:
            hour12 = str(int(d["time24"][0:2]) - 12)
            time12 = hour12+d["time24"][2:5]+" PM"
        d["time12"] = time12
        d["date"] = data["date"]
        d["date_formatted"] = self.dateTransform(data["date"])
        d["day"] = data["day_of_week"]
        d["timezone"] = data["timezone"]
        return d


# london = TimeZone("london")
# print(london.to_dict())

# berlin = TimeZone("berlin")
# print(berlin.to_dict())

# houston = TimeZone("houston")
# print(houston.to_dict())

# miami = TimeZone("miami")
# print(miami.to_dict())

# helsinki = TimeZone("helsinki")
# print(helsinki.to_dict())
