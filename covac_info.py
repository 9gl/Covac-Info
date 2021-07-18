import time
import pandas as pd
import webbrowser,requests,sys,json
import datetime as dt

class covac_info:

    def __init__(self):
        print(""" 
.d8888b.                                          8888888           .d888          
d88P  Y88b                                           888            d88P"           
888    888                                           888            888             
888         .d88b.  888  888  8888b.   .d8888b       888   88888b.  888888  .d88b.  
888        d88""88b 888  888     "88b d88P"          888   888 "88b 888    d88""88b 
888    888 888  888 Y88  88P .d888888 888            888   888  888 888    888  888 
Y88b  d88P Y88..88P  Y8bd8P  888  888 Y88b.          888   888  888 888    Y88..88P 
 "Y8888P"   "Y88P"    Y88P   "Y888888  "Y8888P     8888888 888  888 888     "Y88P"  """)
        print("\nWelcome To Covac Info")
        self.pin_code = input("\nEnter Pincode: ")
        self.df = pd.DataFrame(columns=['date','name','address','pincode','district_name','from','to','vaccine','fee_type',
                        'min_age_limit','available_capacity'])
        self.date = (dt.datetime.now() + dt.timedelta(hours=5, minutes=30)).strftime('%d-%m-%Y')
        self.i = 0

    def book_slot(self):
        res = input("Do you want to book slot(Y/N)?: ")
        if res == "Y" or res == "y":
            webbrowser.open('https://selfregistration.cowin.gov.in/')
        elif res == "N" or res == "n":
            print("Thank you for using Covac Info!")
            time.sleep(2)
            sys.exit()
        else:
            sys.exit()

    def vaccine_info(self):
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={self.pin_code}&date={self.date}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'authority': 'cdn-api.co-vin.in'
        }
        r = requests.get(url, headers=headers).json()
        for data in r.get("centers", []):
            for session_data in data['sessions']:
                self.df.loc[self.i,'name'] = data.get('name')
                self.df.loc[self.i,'address'] = data.get('address')
                self.df.loc[self.i,'pincode'] = data.get('pincode')
                self.df.loc[self.i,'district_name'] = data.get('district_name')
                self.df.loc[self.i,'from'] = data.get('from')
                self.df.loc[self.i,'to'] = data.get('to')
                self.df.loc[self.i,'fee_type'] = data.get('fee_type')
                self.df.loc[self.i,'date'] = session_data.get('date')
                self.df.loc[self.i,'vaccine'] = session_data.get('vaccine')
                self.df.loc[self.i,'min_age_limit'] = session_data.get('min_age_limit')
                self.df.loc[self.i,'available_capacity'] = session_data.get('available_capacity')
                self.i+=1

        df_= self.df[(self.df.min_age_limit==18) & (self.df.available_capacity>0) ]
        print(f'Found {len(df_)} vaccination slots(18+) near you!')
        if len(df_) > 0:
            df_['Address'] = df_.apply(lambda x: f"{x['name']}, {x['address']} - {x['pincode']}", axis=1)
            df_['Timings'] = df_.apply(lambda x: f"{x['from']} - {x['to']}", axis=1)
            df_.rename(columns={'date':'Date','district_name':'District','vaccine':'Vaccine',
                        'fee_type':'Fee','available_capacity':'Available Capacity'}, inplace=True)
            df_ = df_[['Date','Address','District','Vaccine','Fee','Available Capacity']]
            df_.reset_index(drop=True,inplace=True)
            print(df_)
        else:
            print("Restart the app with different pincode or try after sometime")
        self.book_slot()


def main():
    ci = covac_info()
    ci.vaccine_info()
if __name__ == "__main__":
    main()