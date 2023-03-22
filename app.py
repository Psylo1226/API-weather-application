import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import branca.colormap as cm
from folium.plugins import HeatMap
import branca


class Map:
    def __init__(self):
        self.m = folium.Map(location=[52.510797328825724, 19.51308785730282],
                            zoom_start=6,
                            scroolWheelZoom=False,
                            tiles='OpenStreetMap')
        self.df = pd.read_csv('weather.csv')

    def distribution(self, data):
        folium.Choropleth(
            geo_data=data,
            data=self.df
        ).add_to(self.m)

        folium.TileLayer('cartodbpositron').add_to(self.m)
        folium.TileLayer('stamentoner').add_to(self.m)
        folium.TileLayer('stamenterrain').add_to(self.m)
        folium.LayerControl().add_to(self.m)


class Pollution(Map):
    COLORS = ['green', 'yellow', 'orange', 'red', 'purple', 'maroon']
    VMIN = 0
    VMAX = 300
    INDEX = [0, 51, 101, 151, 201, 300, 500]
    CAPTION = 'Total standard of air pollution'

    def __init__(self, csv_path='air_pollution.csv'):
        super().__init__()
        self.colormap = cm.LinearColormap(colors=self.COLORS, vmin=self.VMIN, vmax=self.VMAX, index=self.INDEX,
                                          caption=self.CAPTION)

        self.df = pd.read_csv(csv_path)

    def choices(self, choice):
        if choice == 'Pm10':
            return 5
        if choice == 'Pm25':
            return 6
        if choice == 'O3':
            return 7
        if choice == 'No2':
            return 8
        if choice == 'So2':
            return 9
        if choice == 'Co':
            return 10
        if choice == ' ':
            return Map()

    def my_choice(self, choice_made, choice):
        self.m.add_child(self.colormap)

        if choice_made == self.choices(choice):
            for row in self.df.itertuples():
                color = self.colormap(row[choice_made])
                lat = row[2]
                lon = row[3]
                contamination = row[choice_made]
                folium.Circle(
                    [lat, lon],
                    radius=500 * contamination,
                    color=color,
                    weight=1,
                    fill=True,
                    popup=('City: ' + row[1] + '<br>'
                                               'URL Address: ' + row[4] + '<br>'
                                                                          'Contamination: ' + str(contamination))
                ).add_to(self.m)


class PollutionHeatMap(Map):
    def __init__(self, csv_path='air_pollution.csv'):
        super().__init__()

        self.df = pd.read_csv(csv_path)

    def choices(self, choice):
        if choice == 'Pm10':
            return 5
        if choice == 'Pm25':
            return 6
        if choice == 'O3':
            return 7
        if choice == 'No2':
            return 8
        if choice == 'So2':
            return 9
        if choice == 'Co':
            return 10
        if choice == ' ':
            return Map()

    def heatmap(self, heat_choice, choice):
        if heat_choice == self.choices(choice):
            data = [[row[2], row[3], row[heat_choice]] for row in self.df.itertuples()]
            HeatMap(data,
                    use_local_extrema=False,
                    ).add_to(self.m)


class Stations(Map):
    def __init__(self, csv_path='weather.csv'):
        super().__init__()
        self.add = folium.TileLayer('cartodbpositron').add_to(self.m)
        self.add = folium.TileLayer('stamentoner').add_to(self.m)
        self.add = folium.TileLayer('stamenterrain').add_to(self.m)
        self.edit = folium.LayerControl().add_to(self.m)
        self.df = pd.read_csv(csv_path)

    def popup_html(self, row):
        i = row

        City_name = self.df['City'].iloc[i]
        Temperature_cel = self.df['Temperature_cel'].iloc[i]
        Temperature_fah = self.df['Temperature_fah'].iloc[i]
        Feels_like_cel = self.df['Feels_like_cel'].iloc[i]
        Feels_like_fah = self.df['Feels_like_fah'].iloc[i]
        Wind_speed = self.df['Wind_speed'].iloc[i]
        Humidity = self.df['Humidity'].iloc[i]
        Pressure = self.df['Pressure'].iloc[i]
        Degree = self.df['Degree'].iloc[i]
        Description = self.df['Description'].iloc[i]
        Sunrise_time = self.df['Sunrise_time'].iloc[i]
        Sunset_time = self.df['Sunset_time'].iloc[i]

        left_col_color = "#19a7bd"
        right_col_color = "#f2f0d3"

        html = """<!DOCTYPE html>
    <html>
    <head>
    <h4 style = "margin-bottom:10"; width = "200px" > {} </h4> """.format(City_name) + """

    </head>
        <table style = "height: 126px; width: 350px;">
    <tbody>
    <tr>
    <td style = "background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Temperatura w °C</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Temperature_cel) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Temperatura w °F</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Temperature_fah) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Temperatura odczuwalna w °C</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Feels_like_cel) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Temperatura odczuwalna w °F</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Feels_like_fah) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Prędkość wiatru</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Wind_speed) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Wilgotność</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Humidity) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Ciśnienie</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Pressure) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Kąt wiatru</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Degree) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Opis pogody</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Description) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Godzina wschodu Słońca</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Sunrise_time) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Godzina zachodu Słońca</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(Sunset_time) + """
    </tr>
    </tbody>
    </table>
    </html>
    """

        return html

    def add_markers(self, popup_html):
        global i
        global html
        for i in range(len(self.df)):
            html = popup_html(i)

            iFrame = branca.element.IFrame(html=html, width=400, height=270)
            popup = folium.Popup(iFrame, parse_html=True)

            folium.Marker([self.df['Latitude'].iloc[i], self.df['Longitude'].iloc[i]],
                          popup=popup, icon=folium.Icon(color='green', icon='info-sign')).add_to(self.m)


class Editors:
    def __init__(self):
        self.df = pd.read_csv('weather.csv')
        self.df_country = 'A00_Granice_panstwa.geojson'
        self.df_province = 'A01_Granice_wojewodztw.geojson'
        self.df_counties = 'A02_Granice_powiatow.geojson'
        self.province_list = self.df['Voivodeship'].unique()
        self.province_list.sort()
        self.counties_list = self.df['Province'].unique()
        self.counties_list.sort()
        self.type_of_division = ['', 'Państwo', 'Województwa', 'Powiaty']
        self.lista = ['temp_cel', 'temp_fah', 'feels_cel', 'feels_fah', 'wind_speed', 'humidity', 'pressure', 'degree']
        self.Country = 'Poland'

    def display(self, df, level):
        if level == self.Voivodeship:
            geo_data = self.df_province
            value = self.choice
            hmm = 'Voivodeship'
        elif level == self.Province:
            geo_data = self.df_counties
            value = self.choice
            hmm = 'Province'

        m = folium.Map(location=[52.0, 22.5], zoom_start=6, tiles='cartodbpositron')
        choropleth = folium.Choropleth(
            geo_data=geo_data,
            data=df,
            columns=(hmm, 'Temperature_cel', 'Temperature_fah', 'Feels_like_cel', 'Feels_like_fah', 'Wind_speed',
                     'Humidity', 'Pressure', 'Degree'),
            key_on='feature.properties.nazwa',
            line_opacity=0.8,
            highlight=True,
            default_value='No data',
        ).add_to(m)

        choropleth.geojson.add_to(m)
        df = df.set_index(hmm)

        for feature in choropleth.geojson.data['features']:
            level = feature['properties']['nazwa']
            if level in df.index:
                feature['properties']['temp_cel'] = 'Temperatura w °C: ' + str(
                    df.loc[level, 'Temperature_cel'].mean().round(2)) + str('')
                feature['properties']['temp_fah'] = 'Temperatura w °F: ' + str(
                    df.loc[level, 'Temperature_fah'].mean().round(2)) + str('')
                feature['properties']['feels_cel'] = 'Temperatura odczuwalna w °C: ' + str(
                    df.loc[level, 'Feels_like_cel'].mean().round(2)) + str('')
                feature['properties']['feels_fah'] = 'Temperatura odczuwalna w °F: ' + str(
                    df.loc[level, 'Feels_like_fah'].mean().round(2)) + str('')
                feature['properties']['wind_speed'] = 'Prędkość wiatru: ' + str(
                    df.loc[level, 'Wind_speed'].mean().round(2)) + str('m/s')
                feature['properties']['humidity'] = 'Wilgotność: ' + str(
                    df.loc[level, 'Humidity'].mean().round(2)) + str('%')
                feature['properties']['pressure'] = 'Ciśnienie: ' + str(
                    df.loc[level, 'Pressure'].mean().round(2)) + str('hPa')
                feature['properties']['degree'] = 'Kąt wiatru: ' + str(
                    df.loc[level, 'Degree'].mean().round(2)) + str('')
            else:
                feature['properties']['temp_cel'] = 'No data'
                feature['properties']['temp_fah'] = 'No data'
                feature['properties']['feels_cel'] = 'No data'
                feature['properties']['feels_fah'] = 'No data'
                feature['properties']['wind_speed'] = 'No data'
                feature['properties']['humidity'] = 'No data'
                feature['properties']['pressure'] = 'No data'
                feature['properties']['degree'] = 'No data'

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                ['nazwa', value], labels=False)
        )

        folium_static(m, width=1000, height=500)

    def country(self, df, df_country):
        m = folium.Map(location=[52.0, 22.5], zoom_start=6, tiles='cartodbpositron')
        choropleth = folium.Choropleth(
            geo_data=df_country,
            data=df,
            columns=('Voivodeship', 'Temperature_cel', 'Temperature_fah', 'Feels_like_cel', 'Feels_like_fah', 'Wind_speed',
                     'Humidity', 'Pressure', 'Degree'),
            key_on='feature.properties.nazwa',
            line_opacity=0.8,
            highlight=True
        ).add_to(m)

        choropleth.geojson.add_to(m)
        total_cel = df['Temperature_cel'].sum() / len(df['Temperature_cel'])
        total_fah = df['Temperature_fah'].sum() / len(df['Temperature_fah'])
        total_feels_cel = df['Feels_like_cel'].sum() / len(df['Feels_like_cel'])
        total_feels_fah = df['Feels_like_fah'].sum() / len(df['Feels_like_fah'])
        total_wind_speed = df['Wind_speed'].sum() / len(df['Wind_speed'])
        total_humidity = df['Humidity'].sum() / len(df['Humidity'])
        total_pressure = df['Pressure'].sum() / len(df['Pressure'])
        total_degree = df['Degree'].sum() / len(df['Degree'])

        for feature in choropleth.geojson.data['features']:
            feature['properties']['temp_cel'] = 'Temperatura w °C: ' + str('{:.2f}'.format(total_cel))
            feature['properties']['temp_fah'] = 'Temperatura w °F: ' + str('{:.2f}'.format(total_fah))
            feature['properties']['feels_cel'] = 'Temperatura odczuwalna w °C: ' + str('{:.2f}'.format(total_feels_cel))
            feature['properties']['feels_fah'] = 'Temperatura w °F: ' + str('{:.2f}'.format(total_feels_fah))
            feature['properties']['wind_speed'] = 'Prędkość wiatru: ' + str('{:.2f}'.format(total_wind_speed))
            feature['properties']['humidity'] = 'Wilgotność: ' + str('{:.2f}'.format(total_humidity))
            feature['properties']['pressure'] = 'Ciśnienie: ' + str('{:.2f}'.format(total_pressure))
            feature['properties']['degree'] = 'Kąt wiatru: ' + str('{:.2f}'.format(total_degree))

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                ['nazwa', 'temp_cel', 'temp_fah', 'feels_cel', 'feels_fah', 'wind_speed', 'humidity', 'pressure', 'degree'], labels=False)
        )

        folium_static(m, width=1000, height=500)

    def combined_stats(self, df, division):
        metric_temp_cel = f'Temperatura w °C:'
        metric_temp_fah = f'Temperatura w °F:'
        metric_feels_cel = f'Temperatura odczuwalna w °C:'
        metric_feels_fah = f'Temperatura w °F:'
        metric_wind_speed = f'Prędkość wiatru:'
        metric_humidity = f'Wilgotność:'
        metric_pressure = f'Ciśnienie:'
        metric_degree = f'Kąt wiatru:'

        # Filter df by Voivodeship or Province
        if division == self.Voivodeship:
            df_filtered = df[df['Voivodeship'] == self.Voivodeship]
            metric_name = self.Voivodeship
        elif division == self.Province:
            df_filtered = df[df['Province'] == self.Province]
            metric_name = self.Province
        elif division == self.Country:
            df_filtered = df
            metric_name = 'Poland'

        # Calculate metrics
        total_cel = df_filtered['Temperature_cel'].sum() / len(df_filtered['Temperature_cel'])
        total_fah = df_filtered['Temperature_fah'].sum() / len(df_filtered['Temperature_fah'])
        total_feels_cel = df_filtered['Feels_like_cel'].sum() / len(df_filtered['Feels_like_cel'])
        total_feels_fah = df_filtered['Feels_like_fah'].sum() / len(df_filtered['Feels_like_fah'])
        total_wind_speed = df_filtered['Wind_speed'].sum() / len(df_filtered['Wind_speed'])
        total_humidity = df_filtered['Humidity'].sum() / len(df_filtered['Humidity'])
        total_pressure = df_filtered['Pressure'].sum() / len(df_filtered['Pressure'])
        total_degree = df_filtered['Degree'].sum() / len(df_filtered['Degree'])

        # DISPLAY METRICS
        st.subheader(f'Zbiór danych dla obszaru {metric_name}')
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(metric_temp_cel, '{:.2f}'.format(total_cel))
            with col2:
                st.metric(metric_temp_fah, '{:.2f}'.format(total_fah))
            with col3:
                st.metric(metric_feels_cel, '{:.2f}'.format(total_feels_cel))
            with col4:
                st.metric(metric_pressure, '{:.2f}'.format(total_pressure))

        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(metric_feels_fah, '{:.2f}'.format(total_feels_fah))
            with col2:
                st.metric(metric_wind_speed, '{:.2f}'.format(total_wind_speed))
            with col3:
                st.metric(metric_humidity, '{:.2f}'.format(total_humidity))
            with col4:
                st.metric(metric_degree, '{:.2f}'.format(total_degree))


class App:
    APP_NAME = 'Wykorzystanie baz GIS do prezentacji danych'
    GITHUB_LINK = 'https://github.com/Psylo1226'
    DESCRIPTION = '# This app was created using API weather, air pollution and GIS data from Poland \
                  to real-time weather conditions monitoring.'
    AUTHOR = 'Aplikacja stworzona przez Kamil Sarzyniak w 2023'
    MAIN_TITLE = ':blue[_Aplikacja monitorująca warunki pogodowe na terenie Polski_]'
    WIDGET_TITLE = 'Wybierz co chcesz wyświetlić'
    MAP_WINDOW_WIDTH = 1100
    MAP_WINDOW_HEIGHT = 700

    def __init__(self):
        self.pollution = Pollution()
        self.heatmap = PollutionHeatMap()
        self.map_window = Map()
        self.stations = Stations()
        self.editors = Editors()
        self.csv = pd.read_csv('air_pollution.csv')
        self.df = self.df = pd.read_csv('weather.csv')

    def download(self):
        if st.sidebar.checkbox("Zaznacz jeżeli chcesz pobrać dostępne informacje!"):
            air_pollution = pd.read_csv('air_pollution.csv')
            weather = pd.read_csv('weather.csv')

            st.sidebar.download_button(label="Pobierz plik z aktualnymi zanieczyszczeniami powietrza",
                                       data=air_pollution.to_csv(),
                                       file_name="Air_pollution.csv")
            st.sidebar.download_button(label="Pobierz plik z aktualnymi warunkami pogodowymi",
                                       data=weather.to_csv(),
                                       file_name="Weather.csv")

    def show(self):
        st.set_page_config(self.APP_NAME, layout="wide",
                           menu_items={'Get Help': self.GITHUB_LINK,
                                       'Report a bug': self.GITHUB_LINK,
                                       'About': self.DESCRIPTION
                                       })
        st.title(self.MAIN_TITLE)
        st.sidebar.write(self.AUTHOR)
        st.sidebar.title(self.WIDGET_TITLE)
        clicked = st.sidebar.button('Pokaż dostępne stacje pogodowe')
        if clicked:
            self.stations.add_markers(self.stations.popup_html)
        choice = st.sidebar.selectbox("Wybierz typ zanieczyszczenia", (' ', 'Pm10', 'Pm25', 'O3', 'No2', 'So2', 'Co'))
        self.pollution.my_choice(choice_made=self.pollution.choices(choice), choice=choice)
        heat_choice = st.sidebar.selectbox("Wybierz typ HeatMapy", (' ', 'Pm10', 'Pm25', 'O3', 'No2', 'So2', 'Co'))
        self.heatmap.heatmap(heat_choice=self.heatmap.choices(heat_choice), choice=heat_choice)
        self.editors.lang = st.sidebar.selectbox('Wybierz podział administracyjny', self.editors.type_of_division)
        self.editors.choice = st.sidebar.selectbox('Wybierz informację które chcesz wyświetlić', self.editors.lista)
        self.editors.Voivodeship = st.sidebar.selectbox('Wybierz województwo', self.editors.province_list, len(self.editors.province_list) - 1)
        self.editors.Province = st.sidebar.selectbox('Wybierz powiat', self.editors.counties_list, len(self.editors.counties_list) - 1)
        App.download(self)

        lang = (choice, heat_choice, clicked)

        match (self.editors.lang, lang):
            case ('', (' ', ' ', True)):
                st.subheader('Wszystkie dostępne stacje pogodowe z których pobierane są wyniki')
                folium_static(self.stations.m, width=self.MAP_WINDOW_WIDTH, height=self.MAP_WINDOW_HEIGHT)
            case ('', (' ', ' ', False)):
                folium_static(self.map_window.m, width=self.MAP_WINDOW_WIDTH, height=self.MAP_WINDOW_HEIGHT)
            case ('', (' ', _, False)):
                st.subheader(f'HeatMapa zanieczyszczenia powietrza z zawartością pyłku {heat_choice} w atmosferze')
                folium_static(self.heatmap.m, width=self.MAP_WINDOW_WIDTH, height=self.MAP_WINDOW_HEIGHT)
            case ('', (_, ' ', False)):
                st.subheader(f'Mapa skalarna zanieczyszczenia powietrza z zawartością pyłku {choice} w atmosferze')
                folium_static(self.pollution.m, width=self.MAP_WINDOW_WIDTH, height=self.MAP_WINDOW_HEIGHT)
            case ('', (_, _, False)):
                st.subheader('Możesz wybrać tylko jeden typ mapy!!!')
            case ('Państwo', (' ', ' ', False)):
                self.editors.country(self.df, self.editors.df_country), self.editors.combined_stats(self.df,
                                                                                                    division=self.editors.Country)
            case ('Województwa', (' ', ' ', False)):
                self.editors.display(self.df, level=self.editors.Voivodeship), self.editors.combined_stats(self.df,
                                                                                                           division=self.editors.Voivodeship)
            case ('Powiaty', (' ', ' ', False)):
                self.editors.display(self.df, level=self.editors.Province), self.editors.combined_stats(self.df,
                                                                                                        division=self.editors.Province)


def main():
    app = App()
    app.show()


if __name__ == '__main__':
    main()
