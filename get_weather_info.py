import datetime as dt
import requests
import sys
import pandas as pd
import schedule
import time

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = '2d48f1aa43f965c330e7cfd6dc6cc2d9'
CITIES = ['Brzeg Głogowski', 'Starogard Gdański', 'Pułtusk', 'Legionowo', 'Kędzierzyn-Koźle', 'Kętrzyn', 'Jędrzejów',
          'Trzebnica', 'Szczawno-Zdrój', 'Proszowice', 'Stalowa Wola', 'Jasło', 'Nidzica', 'Sokolec', 'Opole',
          'Jarczew', 'Nieszawa',
          'Tarnów', 'Szczawnica', 'Parzniewice', 'Gryfice', 'Sanok', 'Widuchowa', 'Bogatynia',
          'Ostrowiec Świętokrzyski', 'Kostrza',
          'Brześć Kujawski', 'Przemyśl', 'Międzyrzecz', 'Katowice', 'Korsze', 'Dorohusk', 'Sochaczew',
          'Międzyrzec Podlaski', 'Koszalin', 'Prudnik', 'Polańczyk', 'Krempna', 'Zamość', 'Kołuda Wielka', 'Andrychów',
          'Środa Śląska',
          'Chełmża', 'Częstochowa', 'Ostróda', 'Kamień Pomorski', 'Będzin', 'Żywiec', 'Glitajny', 'Chodecz',
          'Giżycko', 'Brodnica',
          'Mieczysławów', 'Kobierzyce', 'Niepołomice', 'Włodawa', 'Miasteczko Śląskie', 'Chełm', 'Żukowice', 'Kęty',
          'Ozorków', 'Świdnik',
          'Kutno', 'Iława', 'Żagań', 'Nowa Sól', 'Zambrów', 'Horyniec-Zdrój', 'Wadowice', 'Jasna Góra',
          'Ustrzyki Dolne', 'Szczytno', 'Czarna',
          'Sopot', 'Miechów', 'Gajew', 'Zielonka', 'Racibórz', 'Wąbrzeźno', 'Wolbrom', 'Konstancin-Jeziorna', 'Kielce',
          'Chojnów',
          'Golub-Dobrzyń', 'Pleszew', 'Grajewo', 'Maków Mazowiecki', 'Łęczna', 'Bielsk Podlaski', 'Opatów', 'Wieliczka',
          'Łeba',
          'Dobrzyń nad Wisłą', 'Lubaczów', 'Zameczno', 'Kłodzko', 'Białystok', 'Kartuzy', 'Dębno', 'Opoczno', 'Ełk',
          'Gubin', 'Końskie',
          'Mogilno', 'Kraśnik', 'Piotrkowice', 'Pruszków', 'Działoszyn', 'Skawina', 'Ruda Śląska', 'Sokołów Podlaski',
          'Gryfino', 'Cieszyn',
          'Siedlce', 'Łowicz', 'Czerwionka-Leszczyny', 'Iwonicz-Zdrój', 'Władysławowo', 'Rybnik', 'Nowy Tomyśl',
          'Bielawa', 'Złotoryja', 'Krotoszyn', 'Borucin', 'Kołobrzeg', 'Wałcz', 'Radomsko', 'Górne Gruczno', 'Lubań',
          'Piastów',
          'Gorzów Wielkopolski', 'Przysiek', 'Świecie', 'Sokółka', 'Szczecin', 'Mława', 'Bolesławiec', 'Dzierżoniów',
          'Szklarska Poręba',
          'Borówiec', 'Połaniec', 'Gostynin', 'Słupsk', 'Dąbrowa Górnicza', 'Żyrardów', 'Nowy Targ', 'Siemiatycze',
          'Komańcza', 'Wiktorowo',
          'Kwidzyn', 'Szamotuły', 'Turek', 'Czarna Góra', 'Sierpc', 'Grodzisk Mazowiecki', 'Toruń',
          'Piotrków Trybunalski', 'Myszków', 'Luboń',
          'Dębica', 'Kruszyn', 'Ostrołęka', 'Radom', 'Kraków', 'Swarzędz', 'Tychy', 'Kolbuszowa', 'Szczecinek',
          'Szklarki', 'Czarny Las',
          'Jaworzno', 'Tuchola', 'Ząbkowice Śląskie', 'Mińsk Mazowiecki', 'Głubczyce', 'Mszana Dolna', 'Legnica',
          'Wałbrzych',
          'Piechcin', 'Belsk Duży', 'Świebodzin', 'Namysłów', 'Drezdenko', 'Białka', 'Olkusz', 'Lądek-Zdrój', 'Spalona',
          'Sobczyce',
          'Ostrów Mazowiecka', 'Grodziec Mały', 'Wyszków', 'Lubin', 'Koniczynka', 'Radomierzyce', 'Konin', 'Gostyń',
          'Bydgoszcz', 'Chęciny',
          'Słone', 'Nałęczów', 'Świnoujście', 'Gać', 'Malbork', 'Tuchów', 'Tarnobrzeg', 'Wejherowo', 'Jarocin',
          'Rabka-Zdrój', 'Kawice', 'Biała',
          'Brzeziny', 'Rawa Mazowiecka', 'Oborniki', 'Duszniki-Zdrój', 'Oława', 'Sandomierz', 'Busko-Zdrój', 'Wołomin',
          'Witków', 'Zawiercie',
          'Poznań', 'Krzyżówka', 'Przeworsk', 'Płońsk', 'Sulęcin', 'Oświęcim', 'Dąbrowa Tarnowska', 'Warszawa',
          'Łuków',
          'Polanica-Zdrój', 'Głogówko', 'Mielec', 'Lesko', 'Osieczów', 'Chełmno', 'Stargard Szczeciński',
          'Tarnowo Podgórne', 'Jeleniów', 'Lublin',
          'Wolice', 'Limanowa', 'Piła', 'Kowary', 'Marwice', 'Łasin', 'Trzcianka', 'Latoszyn', 'Muszyna',
          'Ustka', 'Jastrzębie-Zdrój',
          'Leśna', 'Izbica Kujawska', 'Odolanów', 'Kozienice', 'Hajnówka', 'Augustów', 'Rzeszów', 'Goczałkowice-Zdrój',
          'Brzeszcze', 'Gołdap', 'Grab', 'Jelenia Góra', 'Liniewko Kościerskie', 'Biłgoraj', 'Szczebrzeszyn',
          'Myślibórz',
          'Głogów', 'Nakło nad Notecią', 'Wodzisław Śląski', 'Lipnik', 'Słubice', 'Słomniki', 'Wieluń', 'Złoczew',
          'Kruszwica',
          'Stare Koźle', 'Nowiny', 'Grudziądz', 'Żory', 'Strzelin', 'Karpacz', 'Kozie Doły', 'Pabianice',
          'Skarżysko-Kamienna',
          'Kościerzyna', 'Mosina', 'Kłobuck', 'Aleksandrów Kujawski', 'Ożarów', 'Godów', 'Sosnowiec', 'Gdynia',
          'Inowrocław', 'Sępólno Krajeńskie',
          'Nowe Skalmierzyce', 'Koło', 'Bielsko-Biała', 'Ciechanów', 'Ciechocinek', 'Gorlice', 'Tarnowskie Góry',
          'Myślenice', 'Nowa Ruda', 'Puławy',
          'Rypin', 'Ostrów Wielkopolski', 'Maszewo Duże', 'Święty Krzyż', 'Elbląg', 'Jawor', 'Chrzanów', 'Lubliniec',
          'Zgierz', 'Sadłogoszcz', 'Chorzów',
          'Pionki', 'Krosno', 'Małogoszcz', 'Nisko', 'Sieradz', 'Zabrze', 'Kościan', 'Milicz', 'Krzeszowice', 'Złockie',
          'Mrągowo', 'Gliwice', 'Dobczyce', 'Wrocław', 'Biała Podlaska', 'Leszno', 'Tczew', 'Łask', 'Zakopane',
          'Zduńska Wola', 'Płock', 'Łomża',
          'Złoty Potok', 'Krynica-Zdrój', 'Szymbark', 'Kalisz', 'Olesno', 'Opatówek', 'Trzebinia', 'Olsztyn',
          'Nowy Sącz', 'Polkowice', 'Wieniec-Zdrój',
          'Otwock', 'Aleksandrów Łódzki', 'Rawicz', 'Radziejów', 'Brzeg', 'Bełchatów', 'Szarów', 'Łódź',
          'Rymanów-Zdrój', 'Ustroń',
          'Gdańsk', 'Wleń', 'Żnin', 'Białe Błota', 'Starachowice', 'Strzelce Opolskie', 'Zdzieszowice', 'Hrubieszów',
          'Skierniewice', 'Piekary Śląskie',
          'Wągrowiec', 'Bytom', 'Wilczopole', 'Uniejów', 'Kromolin', 'Zabierzów', 'Radzyń Chełmiński',
          'Nowa Wies Wielka', 'Pajęczno',
          'Wschowa', 'Nysa', 'Krasnobród', 'Bukowno', 'Gniezno', 'Tomaszów Lubelski', 'Sucha Beskidzka', 'Włocławek',
          'Wojkowice', 'Gołuchów', 'Nowy Dwór Mazowiecki', 'Kamienna Góra', 'Świdnica', 'Chojnice', 'Września',
          'Tłuszcz',
          'Maków Podhalański', 'Kaszów', 'Koziegłowy', 'Kudowa-Zdrój', 'Kalwaria Zebrzydowska', 'Radzyń Podlaski',
          'Piaseczno', 'Krasnystaw',
          'Pruszcz Gdański', 'Biskupiec', 'Knurów', 'Działdowo', 'Brzesko', 'Storkowo', 'Kluczbork', 'Chodzież',
          'Borsukowizna', 'Oleśnica',
          'Stoki', 'Gorzyce', 'Krynica', 'Adamów', 'Florianka', 'Rejowiec Fabryczny', 'Suwałki', 'Jedlina-Zdrój',
          'Guty Duże', 'Przerzeczyn-Zdrój',
          'Police', 'Solec Kujawski', 'Januszkowice', 'Bartoszyce', 'Bochnia', 'Trzepowo', 'Połczyn-Zdrój',
          'Zgorzelec', 'Lębork', 'Pszczyna', 'Tomaszów Mazowiecki', 'Żary', 'Zielona Góra', 'Lwówek Śląski', 'Goleniów']

zachodniopomorskie = ['Świnoujście', 'Kamień Pomorski', 'Gryfice', 'Kołobrzeg', 'Koszalin', 'Połczyn-Zdrój',
                      'Storkowo', 'Szczecinek', 'Wałcz', 'Dębno', 'Myślibórz', 'Police', 'Szczecin', 'Goleniów',
                      'Stargard Szczeciński', 'Gryfino', 'Marwice', 'Widuchowa']

pomorskie = ['Ustka', 'Słupsk', 'Łeba', 'Władysławowo', 'Łębork', 'Wejherowo', 'Gdynia', 'Sopot', 'Gdańsk',
             'Pruszcz Gdański', 'Kartuzy', 'Szymbark', 'Kościerzyna', 'Liniewko Kościerskie', 'Trzepowo',
             'Chojnice', 'Starogard Gdański', 'Tczew', 'Malbork', 'Kwidzyn', 'Lębork']

warminsko_mazurskie = ['Elbląg', 'Iława', 'Ostróda', 'Bartoszyce', 'Gołdap', 'Ełk', 'Szczytno', 'Nidzica', 'Działdowo',
                       'Olsztyn', 'Biskupiec', 'Mrągowo', 'Giżycko', 'Kętrzyn', 'Korsze', 'Glitajny']

lubuskie = ['Gorzów Wielkopolski', 'Drezdenko', 'Słubice', 'Gubin', 'Nowiny', 'Stoki', 'Sulęcin', 'Międzyrzecz',
            'Świebodzin', 'Wschowa', 'Słone', 'Zielona Góra', 'Jeleniów', 'Nowa Sól', 'Żary', 'Żagań', 'Witków']

wielkopolskie = ['Piła', 'Trzcianka', 'Chodzież', 'Wągrowiec', 'Nowy Tomyśl', 'Oborniki', 'Szamotuły',
                 'Tarnowo Podgórne', 'Gniezno', 'Września', 'Poznań', 'Swarzędz', 'Luboń', 'Borówiec', 'Mosina',
                 'Piotrkowice', 'Kościan', 'Leszno', 'Gostyń', 'Rawicz', 'Konin', 'Koło', 'Turek', 'Grab', 'Jarocin',
                 'Krotoszyn', 'Pleszew', 'Gołuchów', 'Odolanów', 'Opatówek', 'Ostrów Wielkopolski', 'Nowe Skalmierzyce',
                 'Kalisz']

kujawsko_pomorskie = ['Sępólno Krajeńskie', 'Tuchola', 'Nakło nad Notecią', 'Górne Gruczno', 'Świecie', 'Chełmno',
                      'Grudziądz', 'Łasin', 'Wiktorowo', 'Radzyń Chełmiński', 'Wąbrzeźno', 'Brodnica', 'Rypin',
                      'Golub-Dobrzyń', 'Chełmża', 'Koniczynka', 'Toruń', 'Przysiek', 'Solec Kujawski', 'Bydgoszcz',
                      'Białe Błota', 'Nowa Wies Wielka', 'Żnin', 'Wolice', 'Sadłogoszcz', 'Piechcin', 'Inowrocław',
                      'Kołuda Wielka', 'Mogilno', 'Kruszwica', 'Radziejów', 'Aleksandrów Kujawski', 'Cichocinek',
                      'Nieszawa', 'Brześć Kujawski', 'Izbica Kujawska', 'Chodecz', 'Wieniec-Zdrój', 'Włocławek',
                      'Dobrzyń nad Wisłą', 'Ciechocinek']

mazowieckie = ['Sierpc', 'Mława', 'Maszewo Duże', 'Płock', 'Gostynin', 'Ciechanów', 'Płońsk', 'Ostrołęka', 'Guty Duże',
               'Maków Mazowiecki', 'Pułtusk', 'Ostrów Mazowiecka', 'Wyszków', 'Sokołów Podlaski', 'Siedlce',
               'Sochaczew',
               'Nowy Dwór Mazowiecki', 'Legionowo', 'Tłuszcz', 'Wołomin', 'Zielonka', 'Warszawa', 'Piastów', 'Pruszków',
               'Grodzisk Mazowiecki', 'Żyrardów', 'Krzyżówka', 'Piaseczno', 'Konstancin-Jeziorna', 'Otwock',
               'Mińsk Mazowiecki', 'Belsk Duży', 'Kozienice', 'Pionki', 'Radom', 'Mieczysławów']

podlaskie = ['Suwałki', 'Augustów', 'Czarny Las', 'Grajewo', 'Zambrów', 'Łomża', 'Kruszyn', 'Sokółka', 'Białystok',
             'Boruskowizna', 'Bielsk Podlaski', 'Siemiatycze', 'Hajnówka', 'Borsukowizna']

lubelskie = ['Biała Podlaska', 'Międzyrzec Podlaski', 'Łuków', 'Radzyń Podlaski', 'Adamów', 'Jarczew', 'Włodawa',
             'Puławy', 'Nałęczów', 'Kraśnik', 'Łęczna', 'Świdnik', 'Wilczopole', 'Lublin', 'Krasnystaw',
             'Rejowiec Fabryczny', 'Chełm', 'Dorohusk', 'Szczebrzeszyn', 'Zamość', 'Hrubieszów', 'Biłgoraj',
             'Florianka',
             'Krasnobród', 'Tomaszów Lubelski']

dolnoslaskie = ['Kromolin', 'Brzeg Głogowski', 'Zameczno', 'Żukowice', 'Kozie Doły', 'Głogówko', 'Sobczyce',
                'Grodziec Mały', 'Głogów', 'Szklarki', 'Polkowice', 'Lubin', 'Bogatynia', 'Jasna Góra', 'Radomierzyce',
                'Zgorzelec', 'Lubań', 'Leśna', 'Lwówek Śląski', 'Osieczów', 'Bolesławiec', 'Wleń', 'Szklarska Poręba',
                'Jelenia Góra', 'Złotoryja', 'Chojnów', 'Legnica', 'Kawice', 'Środa Śląska', 'Jawor', 'Kostrza',
                'Karpacz', 'Kowary', 'Kamienna Góra', 'Świdnica', 'Szczawno-Zdrój', 'Wałbrzych', 'Jedlina-Zdrój',
                'Milicz', 'Trzebnica', 'Oleśnica', 'Wrocław', 'Oława', 'Kobierzyce', 'Sokolec', 'Strzelin',
                'Dzierżoniów', 'Bielawa', 'Nowa Ruda', 'Przerzeczyn-Zdrój', 'Ząbkowice Śląskie', 'Kudowa-Zdrój',
                'Duszniki-Zdrój', 'Polanica-Zdrój', 'Kłodzko', 'Spalona', 'Lądek-Zdrój']

opolskie = ['Namysłów', 'Brzeg', 'Kluczbork', 'Olesno', 'Nysa', 'Biała', 'Prudnik', 'Głubczyce', 'Opole',
            'Strzelce Opolskie', 'Zdzieszowice', 'Januszkowice', 'Kędzierzyn-Koźle', 'Stare Koźle']

lodzkie = ['Kutno', 'Gajew', 'Łowicz', 'Skierniewice', 'Rawa Mazowiecka', 'Uniejów', 'Ozorków', 'Zgierz', 'Brzeziny',
           'Aleksandrów Łódzki', 'Pabianice', 'Łask', 'Zduńska Wola', 'Sieradz', 'Wieluń', 'Złoczew',
           'Tomaszów Mazowiecki',
           'Opoczno', 'Łódź', 'Piotrków Trybunalski', 'Bełchatów', 'Parzniewice', 'Działoszyn', 'Pajęczno', 'Radomsko']

slaskie = ['Lubliniec', 'Kłobuck', 'Częstochowa', 'Koziegłowy', 'Złoty Potok', 'Myszków', 'Zawiercie',
           'Miasteczko Śląskie',
           'Tarnowskie Góry', 'Piekary Śląskie', 'Wojkowice', 'Będzin', 'Dąbrowa Górnicza', 'Bytom', 'Chorzów',
           'Katowice', 'Sosnowiec', 'Jaworzno', 'Zabrze', 'Ruda Śląska', 'Tychy', 'Gliwice', 'Knurów',
           'Czerwionka-Leszczyny',
           'Żory', 'Rybnik', 'Racibórz', 'Borucin', 'Wodzisław Śląski', 'Godów', 'Jastrzębie-Zdrój', 'Pszczyna',
           'Goczałkowice-Zdrój', 'Cieszyn', 'Ustroń', 'Bielsko-Biała', 'Żywiec']

swietokrzyskie = ['Końskie', 'Skarżysko-Kamienna', 'Starachowice', 'Ostrowiec Świętokrzyski', 'Ożarów', 'Opatów',
                  'Sandomierz', 'Połaniec', 'Małogoszcz', 'Chęciny', 'Kielce', 'Święty Krzyż', 'Jędrzejów', 'Busko-Zdrój']

malopolskie = ['Wolbrom', 'Miechów', 'Bukowno', 'Olkusz', 'Słomniki', 'Proszowice', 'Trzebinia', 'Chrzanów', 'Oświęcim',
               'Brzeszcze', 'Kęty', 'Andrychów', 'Krzeszowice', 'Zabierzów', 'Kraków', 'Kaszów', 'Skawina', 'Wieliczka',
               'Wadowice', 'Kalwaria Zebrzydowska', 'Sucha Beskidzka', 'Maków Podhalański', 'Białka', 'Wieliczka', 'Dobczyce',
               'Myślenice', 'Lipnik', 'Mszana Dolna', 'Rabka-Zdrój', 'Niepołomice', 'Szarów', 'Bochnia', 'Brzesko',
               'Dąbrowa Tarnowska', 'Tarnów', 'Tuchów', 'Gorlice', 'Nowy Targ', 'Zakopane', 'Czarna Góra', 'Szczawnica',
               'Limanowa', 'Nowy Sącz', 'Krynica', 'Złockie', 'Muszyna', 'Krynica-Zdrój']

podkarpackie = ['Gorzyce', 'Tarnobrzeg', 'Stalowa Wola', 'Nisko', 'Mielec', 'Kolbuszowa', 'Lubaczów', 'Horyniec-Zdrój',
                'Czarna', 'Latoszyn', 'Dębica', 'Rzeszów', 'Gać', 'Przeworsk', 'Przemyśl', 'Jasło', 'Krempna', 'Krosno',
                'Iwonicz-Zdrój', 'Rymanów-Zdrój', 'Sanok', 'Komańcza', 'Lesko', 'Polańczyk', 'Ustrzyki Dolne']

piaseczanski = ['Konstancin-Jeziorna', 'Piaseczno']

province = {'piaseczeński': ['Konstancin-Jeziorna', 'Piaseczno'], 'radomski': 'Pionki', 'sierpecki': 'Sierpc',
            'gostyniński': 'Gostynin', 'grodzisk': 'Grodzisk Mazowiecki', 'łukowski': ['Łuków', 'Adamów', 'Jarczew'],
            'Chełm': 'Chełm', 'brzeski': ['Brzesko', 'Brzeg'], 'Kraków': 'Kraków',
            'zgierski': ['Ozorków', 'Aleksandrów Łódzki', 'Zgierz'], 'sulęciński': 'Sulęcin', 'Radom': 'Radom',
            'żyrardowski': ['Krzyżówka', 'Żyrardów'], 'obornicki': 'Oborniki', 'Siedlce': 'Siedlce', 'Leszno': 'Leszno',
            'kolski': 'Koło', 'Łomża': 'Łomża', 'rawicki': 'Rawicz', 'kościerski': ['Kościerzyna', 'Liniewko Kościerskie'],
            'stargardzki': 'Stargard Szczeciński', 'Wrocław': 'Wrocław', 'giżycki': ['Giżycko', 'Gajew'], 'mrągowski': 'Mrągowo',
            'głogowski': ['Kromolin', 'Brzeg Głogowski', 'Zameczno', 'Żukowice', 'Kozie Doły', 'Głogówko', 'Sobczyce', 'Grodziec Mały', 'Głogów'],
            'Sosnowiec': 'Sosnowiec', 'rybnicki': 'Czerwionka-Leszczyny', 'Gliwice': 'Gliwice', 'Piekary Śląskie': 'Piekary Śląskie',
            'Jaworzno': 'Jaworzno', 'inowrocławski': ['Inowrocław', 'Kruszwica', 'Kołuda Wielka'], 'brodnicki': ['Brodnica'],
            'włocławski': ['Wieniec-Zdrój', 'Brześć Kujawski', 'Izbica Kujawska', 'Chodecz'], 'mogileński': 'Mogilno',
            'Toruń': 'Toruń', 'tucholski': 'Tuchola', 'raciborski': ['Borucin', 'Racibórz'], 'cieszyński': ['Cieszyn', 'Ustroń'],
            'nyski': 'Nysa', 'Jelenia Góra': 'Jelenia Góra', 'zgorzelecki': ['Zgorzelec', 'Radomierzyce', 'Bogatynia', 'Jasna Góra'],
            'Ostrołęka': 'Ostrołęka', 'jarociński': 'Jarocin', 'Gdynia': 'Gdynia', 'Świnoujście': 'Świnoujście',
            'kamiennogórski': 'Kamienna Góra', 'pabianicki': 'Pabianice', 'ostródzki': 'Ostróda', 'Przemyśl': 'Przemyśl',
            'włodawski': 'Włodawa', 'bocheński': 'Bochnia', 'Tarnów': 'Tarnów', 'wschowski': 'Wschowa', 'międzyrzecki': ['Międzyrzecz', 'Stoki', 'Nowiny'],
            'słubicki': 'Słubice', 'nowotomyski': 'Nowy Tomyśl', 'wągrowiecki': 'Wągrowiec', 'słupski': 'Ustka',
            'ostrowiecki': 'Ostrowiec Świętokrzyski', 'skarżyski': 'Skarżysko-Kamienna', 'kartuski': ['Szymbark', 'Kartuzy'],
            'częstochowski': 'Złoty Potok', 'Elbląg': 'Elbląg', 'gryfiński': ['Gryfino', 'Marwice', 'Widuchowa'], 'Bytom': 'Bytom',
            'złotoryjski': 'Złotoryja', 'wrocławski': 'Kobierzyce', 'milicki': 'Milicz', 'lubiński': 'Lubin', 'lipnowski': 'Dobrzyń nad Wisłą',
            'żniński': ['Żnin', 'Wolice', 'Sadłogoszcz', 'Piechcin'], 'radziejowski': 'Radziejów', 'nakielski': 'Nakło nad Notecią',
            'bartoszycki': 'Bartoszyce', 'żywiecki': 'Żywiec', 'sokolski': ['Sokółka', 'Borsukowizna'], 'jasielski': ['Jasło', 'Krempna'],
            'głubczycki': 'Głubczyce', 'nowosądecki': ['Krynica', 'Złockie', 'Muszyna', 'Krynica-Zdrój'], 'Zielona Góra': ['Zielona Góra', 'Jeleniów'],
            'Skierniewice': 'Skierniewice', 'żagański': ['Żagań', 'Witków'], 'Gdańsk': 'Gdańsk', 'lęborski': ['Łeba', 'Lębork'],
            'piotrkowski': ['Parzniewice', 'Łódź'], 'starogardzki': 'Starogard Gdański',
            'Poznań': 'Poznań', 'Konin': 'Konin', 'Tarnobrzeg': 'Tarnobrzeg', 'płoński': 'Płońsk', 'mławski': 'Mława',
            'hrubieszowski': 'Hrubieszów', 'kraśnicki': 'Kraśnik', 'łęczyński': 'Łęczna', 'Zamość': 'Zamość', 'dąbrowski': 'Dąbrowa Tarnowska',
            'krakowski': ['Skawina', 'Kaszów', 'Zabierzów', 'Krzeszowice', 'Słomniki'], 'żarski': 'Żary', 'krośnieński': ['Iwonicz-Zdrój', 'Rymanów-Zdrój', 'Gubin'],
            'dębicki': ['Czarna', 'Latoszyn', 'Dębica'], 'namysłowski': 'Namysłów', 'czarnkowsko-trzcianecki': 'Trzcianka',
            'Płock': 'Płock', 'grajewski': 'Grajewo', 'starachowicki': 'Starachowice', 'konecki': 'Końskie', 'nidzicki': 'Nidzica',
            'Ruda Śląska': 'Ruda Śląska', 'tarnogórski': ['Miasteczko Śląskie', 'Tarnowskie Góry'], 'zawierciański': 'Zawiercie',
            'Chorzów': 'Chorzów', 'Katowice': 'Katowice', 'bolesławiecki': ['Osieczów', 'Bolesławiec'], 'Wałbrzych': ['Wałbrzych', 'Szczawno-Zdrój'],
            'sępoleński': 'Sępólno Krajeńskie', 'Włocławek': 'Włocławek', 'hajnowski': 'Hajnówka', 'chrzanowski': ['Chrzanów', 'Trzebinia'],
            'wejherowski': 'Wejherowo', 'Szczecin': 'Szczecin', 'pucki': 'Władysławowo', 'rawski': 'Rawa Mazowiecka', 'łowicki': 'Łowicz',
            'iławski': 'Iława', 'niżański': 'Nisko', 'tarnobrzeski': 'Gorzyce', 'pruszkowski': ['Pruszków', 'Piastów'],
            'wyszkowski': 'Wyszków', 'biłgorajski': ['Biłgoraj', 'Florianka'], 'chełmski': ['Rejowiec Fabryczny', 'Dorohusk'],
            'świdnicki': ['Kostrza', 'Świdnica', 'Świdnik'], 'kutnowski': 'Kutno', 'kolbuszowski': 'Kolbuszowa', 'oleski': 'Olesno',
            'strzelecki': 'Strzelce Opolskie', 'Suwałki': 'Suwałki', 'kościański': ['Piotrkowice', 'Kościan'], 'szamotulski': 'Szamotuły',
            'Kielce': 'Kielce', 'staszowski': 'Połaniec', 'ełcki': 'Ełk', 'dzierżanowski': ['Dzierżoniów', 'Bielawa', 'Przerzeczyn-Zdrój'],
            'tczewski': 'Tczew', 'kołobrzeski': 'Kołobrzeg', 'Koszalin': 'Koszalin', 'kłobucki': 'Kłobuck', 'gliwicki': 'Knurów',
            'lubliniecki': 'Lubliniec', 'Bielsko-Biała': 'Bielsko-Biała', 'Legnica': 'Legnica', 'grudziądzki': ['Łasin', 'Radzyń Chełmiński', 'Wiktorowo'],
            'toruński': ['Chełmża', 'Koniczynka', 'Przysiek'], 'chełmiński': 'Chełmno', 'wodzisławski': ['Wodzisław Śląski', 'Godów'],
            'leski': ['Lesko', 'Polańczyk'], 'bieszczadzki': 'Ustrzyki Dolne', 'prudnicki': ['Prudnik', 'Biała'], 'ząbkowicki': 'Ząbkowice Śląskie',
            'makowski': ['Maków Mazowiecki', 'Guty Duże'], 'pszczyński': ['Goczałkowice-Zdrój', 'Pszczyna'], 'gołdapski': 'Gołdap',
            'Sopot': 'Sopot', 'jeleniogórski': ['Szklarska Poręba', 'Karpacz', 'Kowary'], 'opoczyński': 'Opoczno',
            'ostrowski': ['Odolanów', 'Ostrów Wielkopolski', 'Nowe Skalmierzyce', 'Ostrów Mazowiecka'], 'Kalisz': 'Kalisz', 'miński': 'Mińsk Mazowiecki',
            'zwoleński': 'Mieczysławów', 'lubelski': 'Wilczopole', 'proszowicki': 'Proszowice', 'wielicki': ['Wieliczka', 'Niepołomice', 'Szarów'],
            'sieradzki': ['Sieradz', 'Złoczew'], 'brzeziński': 'Brzeziny', 'strzelecko-drezdenecki': 'Drezdenko', 'świebodziński': 'Świebodzin',
            'lubaczowski': ['Lubaczów', 'Horyniec-Zdrój'], 'chodzieski': 'Chodzież', 'kluczborski': 'Kluczbork', 'jędrzejewski': ['Jędrzejów', 'Małogoszcz'],
            'gostyniński': 'Gostynin', 'kaliski': 'Opatówek', 'siemiatycki': 'Siemiatycze', 'gdański': ['Pruszcz Gdański', 'Trzepowo'],
            'szczycieński': 'Szczytno', 'gryficki': 'Gryfice', 'myszkowski': ['Myszków', 'Koziegłowy'], 'oleśnicki': 'Oleśnica',
            'strzeliński': 'Strzelin', 'wąbrzeski': 'Wąbrzeźno', 'kętrzyński': ['Kętrzyn', 'Korsze', 'Glitajny',], 'augustowski': ['Augustów', 'Czarny Las'],
            'wałbrzyski': 'Jedlina-Zdrój', 'kłodzki': ['Sokolec', 'Nowa Ruda', 'Kudowa-Zdrój', 'Duszniki-Zdrój', 'Polanica-Zdrój', 'Kłodzko', 'Spalona', 'Lądek-Zdrój'],
            'Tychy': 'Tychy', 'Rybnik': 'Rybnik', 'sokołowski': 'Sokołów Podlaski', 'grójecki': 'Belsk Duży',
            'puławski': ['Puławy', 'Nałęczów'], 'radzyński': 'Radzyń Podlaski', 'Biała Podlaska': 'Biała Podlaska', 'Nowy Sącz': 'Nowy Sącz',
            'Gorzów Wielkopolski': 'Gorzów Wielkopolski', 'pilski': 'Piła', 'buski': 'Busko-Zdrój', 'turecki': 'Turek',
            'opatowski': ['Opatów', 'Ożarów'], 'Słupsk': 'Słupsk', 'bielski': 'Bielsk Podlaski', 'polkowicki': ['Szklarki', 'Polkowice'],
            'Jastrzębie-Zdrój' : 'Jastrzębie-Zdrój', 'tatrzański': ['Czarna Góra', 'Zakopane'], 'nowotarski': ['Rabka-Zdrój', 'Nowy Targ', 'Szczawnica'],
            'lwówecki': ['Lwówek Śląski', 'Wleń'], 'legionowski': 'Legionowo', 'tomaszowski': ['Tomaszów Lubelski', 'Tomaszów Mazowiecki'], 'zambrowski': 'Zambrów',
            'płocki': 'Maszewo Duże', 'pułtuski': 'Pułtusk', 'sochaczewski': 'Sochaczew', 'ciechanowski': 'Ciechanów',
            'bialski': 'Międzyrzec Podlaski', 'krasnostawski': ['Krasnystaw', 'Lublin'], 'zamojski': ['Krasnobród', 'Szczebrzeszyn'],
            'tarnowski': 'Tuchów', 'bełchatowski': 'Bełchatów', 'łaski': 'Łask', 'pajęczański': ['Działoszyn', 'Pajęczno'],
            'radomszczański': 'Radomsko', 'zduńskowolski': 'Zduńska Wola', 'nowosolski': 'Nowa Sól', 'mielecki': 'Mielec',
            'Warszawa': 'Warszawa', 'krapkowicki': ['Opole', 'Zdzieszowice', 'Januszkowice'], 'moniecki': 'Kruszyn',
            'kielecki': ['Święty Krzyż', 'Chęciny'], 'wrzesiński': 'Września', 'gnieźnieński': 'Gniezno', 'malborski': 'Malbork',
            'olsztyński': 'Biskupiec', 'działdowski': 'Działdowo', 'kwidzyński': 'Kwidzyn', 'Dąbrowa Górnicza': 'Dąbrowa Górnicza',
            'myśliborski': ['Dębno', 'Myślibórz'], 'golubsko-dobrzyński': 'Golub-Dobrzyń', 'aleksandrowski': ['Nieszawa', 'Ciechocinek', 'Aleksandrów Kujawski'],
            'świecki': ['Świecie', 'Górne Gruczno'], 'pleszewski': ['Pleszew', 'Gołuchów', 'Grab'], 'Krosno': 'Krosno',
            'sanocki': ['Sanok', 'Komańcza'], 'suski': ['Sucha Beskidzka', 'Maków Podhalański', 'Białka'], 'zielonogórski': 'Słone',
            'wołomiński': ['Tłuszcz', 'Wołomin', 'Zielonka'], 'goleniowski': 'Goleniów', 'Rzeszów': 'Rzeszów', 'wałecki': 'Wałcz',
            'chojnicki': 'Chojnice', 'przeworski': ['Gać', 'Przeworsk'], 'otwocki': 'Otwock', 'kozienicki': 'Kozienice',
            'limanowski': ['Mszana Dolna', 'Limanowa'], 'miechowski': 'Miechów', 'myślenicki': ['Myślenice', 'Dobczyce', 'Lipnik'],
            'olkuski': ['Bukowno', 'Olkusz', 'Wolbrom'], 'oświęcimski': ['Oświęcim', 'Brzeszcze', 'Kęty'], 'Piotrków Trybunalski': 'Piotrków Trybunalski',
            'poddębicki': 'Uniejów', 'wieluński': 'Wieluń', 'kędzierzyńsko-kozielki': ['Stare Koźle', 'Kędzierzyn-Koźle'], 'krotoszyński': 'Krotoszyn',
            'Białystok': 'Białystok', 'sandomierski': 'Sandomierz', 'szczecinecki': ['Storkowo', 'Szczecinek'], 'świdwiński': 'Połczyn-Zdrój',
            'Zabrze': 'Zabrze', 'Olsztyn': 'Olsztyn', 'kamieński': 'Kamień Pomorski', 'Częstochowa': 'Częstochowa', 'trzebnicki': 'Trzebnica',
            'bydgoski': ['Nowa Wies Wielka', 'Solec Kujawski', 'Białe Błota'], 'oławski': 'Oława', 'średzki': 'Środa Śląska',
            'legnicki': ['Kawice', 'Chojnów'], 'Bydgoszcz': 'Bydgoszcz', 'Grudziądz': 'Grudziądz', 'rypiński': 'Rypin', 'gorlicki': 'Gorlice',
            'lubański': ['Lubań', 'Leśna'], 'wadowicki': ['Andrychów', 'Wadowice', 'Kalwaria Zebrzydowska'], 'Żory': 'Żory',
            'nowodworski': ['Nowy Dwór Mazowiecki'], 'jaworski': 'Jawor', 'poznański':['Tarnowo Podgórne', 'Mosina', 'Borówiec', 'Luboń', 'Swarzędz'],
            'stalowowolski': 'Stalowa Wola', 'będziński': ['Będzin', 'Wojkowice'], 'policki': 'Police', 'gostyński': 'Gostyń',
            }


def weather():
    sys.stdout = open('weather.txt', 'w', encoding='utf-8')
    print(
        'City,Longitude,Latitude,Temperature_cel,Temperature_fah,Feels_like_cel,Feels_like_fah,Wind_speed,Humidity,'
        'Pressure,Degree,Description,Sunrise_time,Sunset_time,Voivodeship,Province')

    def kelvin_to_celsius_fahrenheit(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
        return celsius, fahrenheit

    for i in CITIES:
        url = BASE_URL + 'appid=' + API_KEY + '&q=' + i
        response = requests.get(url).json()

        longitude = response['coord']['lon']
        latitude = response['coord']['lat']
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']
        degree = response['wind']['deg']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']).strftime(
            '%H:%M:%S')
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']).strftime(
            '%H:%M:%S')
        voivodeship = 'zachodniopomorskie' if i in zachodniopomorskie else 'pomorskie' if i in pomorskie \
        else 'warmińsko-mazurskie' if i in warminsko_mazurskie else 'kujawsko-pomorskie' if i in kujawsko_pomorskie \
        else 'lubuskie' if i in lubuskie else 'wielkopolskie' if i in wielkopolskie else 'zachodniopomorskie' \
        if i in zachodniopomorskie else 'lubelskie' if i in lubelskie else 'podlaskie' if i in podlaskie else \
        'mazowieckie' if i in mazowieckie else 'łódzkie' if i in lodzkie else 'śląskie' if i in slaskie else \
        'świętokrzyskie' if i in swietokrzyskie else 'małopolskie' if i in malopolskie else 'podkarpackie' \
        if i in podkarpackie else 'opolskie' if i in opolskie else 'dolnośląskie' if i in dolnoslaskie else \
        'śląskie' if i in slaskie else 'świętokrzyskie' if i in swietokrzyskie else 'małopolskie' if i in \
        malopolskie else 'podkarpackie' if i in podkarpackie else 'opolskie' if i in opolskie else \
        'dolnośląskie' if i in dolnoslaskie else 'error'

        provinces = [k for k, v in province.items() if (isinstance(v, list) and i in v) or v == i][0] if \
            [k for k, v in province.items() if (isinstance(v, list) and i in v) or v == i] else ''




        print(
            f" {i}, {longitude}, {latitude}, {temp_celsius:.2f}, {temp_fahrenheit:.2f}, {feels_like_celsius:.2f}, "
            f"{feels_like_fahrenheit:.2f}, {wind_speed}, {humidity}, {pressure}, {degree}, {description},"
            f"{sunrise_time}, {sunset_time},{voivodeship},{'powiat ' + str(provinces)}")

    sys.stdout.close()

    dataframe1 = pd.read_csv('weather.txt')

    dataframe1.to_csv('weather.csv', index=False, encoding='utf-8')
    return dataframe1

    schedule.every(1).hour.do(air_pollution)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    weather()

