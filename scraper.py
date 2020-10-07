import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import requests
from bs4 import BeautifulSoup
import random
import json
import time

headers = [
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',},
{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',}
]


def scrape_posts(loc_id,posts_per_page,end_cursor,posts_per_file):
    #Variables iniciales
    query_hash = '36bd0f2bf5911908de389b8ceaa3be6d'
    arr_ec=[end_cursor]
    arr =[]
    timeout = 25
    errores = 0
    total_pages = 0
    total_posts = 0
    i=0
    while (True):
        # URL que irá variando
        url_var = 'http://www.instagram.com/graphql/query/?query_hash={0}&variables=%7B"id"%3A"{1}"%2C"first"%3A{2}%2C"after"%3A"{3}"%7D'.format(query_hash,loc_id,posts_per_page,arr_ec[-1])
        print(str(url_var))
        try:
            request = requests.get(url_var, timeout=timeout , headers=random.choice(headers) , verify=False) # Hacemos el request
            if(request.status_code == 200):
                
                total_pages    +=  1 # Aumentamos el contador de paginas scrapeadas
                json_response   =  json.loads(request.text) # Formateamos a JSON el response del request
                end_cursor      =  json_response["data"]["location"]["edge_location_to_media"]["page_info"]["end_cursor"] # Extraemos la referencia a la siguiente pagina
                posts_lists     =  json_response["data"]["location"]["edge_location_to_media"]["edges"] # Extraemos los posts dentro de un objeto iterable
                has_next_page   =  json_response["data"]["location"]["edge_location_to_media"]["page_info"]["has_next_page"] # Averiguamos si existe una siguiente pagina con mas posts
                
                print(end_cursor)
                print(arr_ec[-1])

                if (end_cursor=='') or (int(end_cursor)>int(arr_ec[-1])):
                    end_cursor = arr_ec[-1]
                    end_cursor= change_end_cursor(end_cursor)
                    arr_ec.append(end_cursor)
                else:
                    arr_ec.append(end_cursor)
                    print(end_cursor)
                    print(arr_ec[-1])
                    print(type(posts_lists))
                    print(has_next_page)
                    if (has_next_page!=True):
                        end_cursor = arr_ec[-1]
                        end_cursor= change_end_cursor(end_cursor)
                    else:

                        for post in posts_lists:
                            user_id = post["node"]["owner"]["id"]
                            timestamp = post["node"]["taken_at_timestamp"]
                            shortchode = post["node"]["shortcode"]
                            post_text_container = post["node"]["edge_media_to_caption"]["edges"]
                            post_reactions = post["node"]["edge_liked_by"]["count"]
                            post_is_video = post["node"]["is_video"]
                            
                            if len(post_text_container) > 0 :
                                post_text = post_text_container[0]["node"]["text"]
                            else:
                                post_text = ""
                            
                            arr.append({'user_id': str(user_id), 
                                        'date': str(timestamp),
                                        'shortchode': str(shortchode),
                                        'post_text': str(post_text),
                                        'post_reactions': str(post_reactions),
                                        'post_is_video': str(post_is_video)}) 

                            total_posts += 1 # Aumentamos el contador de posts extraidos y guardados
                            print('Timestamp : '+ str(timestamp)) # Mostramos en la terminal la cantidad de posts scrapeados   
            else:
                time.sleep(15)    # Tiempo de delay entre cada request para no sobresaturar al servidor de peticiones
                        
        except ValueError:
            errores += 1

        print("Se han capturado un total de posts de : "+str(total_posts))
        print("Se han tenido un total de errores de : "+str(errores))
        print("End cursor actual : "+str(end_cursor))
        print("Se han recorrido un total de paginas de : "+str(total_pages))
        print("Existe otra pagina siguiente ? "+str(has_next_page))

        time.sleep(0.5) 

        # Indicamos el nombre que tendrá el JSON que guardaremos (por eso 'w') finalmente
        if (len(arr)>posts_per_file):
            i=i+1
            with open('ARCHIVO_'+str(i)+'_TP_'+str(total_posts)+'_E_C_'+str(end_cursor)+'_ERR_'+str(errores)+'.json', 'w') as outfile:
                print("Se creo el json")
                json.dump(arr,outfile) # Indicamos que contendrá el JSON, que es la lista con los shortcodes de cada post scrappeado

            print("Se han tenido un total de errores de conexión de :" + str(errores))
            print("Finalmente se han guardado : "+ str(total_posts))
            arr=[]

def change_end_cursor(end_cursor):
    new_end_cursor = int(end_cursor) - random.randint(1000000000000,10000000000000)
    return new_end_cursor

def return_first_end_cursor(loc_id):
    response = requests.get('https://www.instagram.com/explore/locations/{0}'.format(loc_id))
    soup = BeautifulSoup(response.content, 'html.parser')
    script_info = soup.find_all('script')[4].string
    script_info_1 = str(script_info).split('"end_cursor":',1)[1].split('},"edges"',1)[0].replace('"',"")
    return str(script_info_1)  


class Mainwindow(QDialog):
    def __init__(self):
        super(Mainwindow,self).__init__()
        loadUi("scraper_GUI.ui",self)
        #Cambio la primera columna (0) su valor de ancho a 200p
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,150)
        self.tableWidget.setColumnWidth(3,150)
        self.load_data()
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.botonData.clicked.connect(self.scrape_trigger) 
        self.row = 0
        self.col = 0

    def scrape_trigger(self):
        #Obtengo el valor de la celda de coordenadas (fila_actual,columna_actual+1)
        loc_id = self.tableWidget.item(self.tableWidget.currentRow(),self.tableWidget.currentColumn()+1).text()
        #Obtengo el valor en posts_per_page_entr como string
        posts_per_page = str(self.posts_per_page_entry.text())
        #Paso el loc_id para generar el end_cursor de la primera iteración
        end_cursor = return_first_end_cursor(loc_id)
        #Obtengo el valor en posts_per_file_entry
        posts_per_file = int(self.posts_per_file_entry.text())
        self.posts_per_page_entry.clear()
        print("loc_ID: "+str(loc_id)+" posts_per_page: "+str(posts_per_page)+"end_cursor:"+str(end_cursor))
        scrape_posts(loc_id,posts_per_page,end_cursor,posts_per_file)

    def cell_was_clicked(self,row,column):
        loc_name = self.tableWidget.item(row,column).text()
        posts_per_file = str(self.posts_per_file_entry.text())
        self.labelFondo.setText("Start scrape on "+str(loc_name)+" with "+ str(posts_per_file)+" posts per file")

    def load_data(self):
        with open('locations.json','r') as f:
            data_set=json.load(f)["locations"]

        print(data_set)
        print(type(data_set))
        row=0
        self.tableWidget.setRowCount(len(data_set))
        for data in data_set:
            self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(data["location"]))
            self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(str(data["id"])))
            self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(str(data["lat"])))
            self.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(str(data["lng"])))
            row += 1 

# main
app = QApplication(sys.argv)
mainwindow = Mainwindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(910)
widget.setFixedHeight(510)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")