<p align="center">
  <img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/banner.png" width="700" height="350">
</p>

</div>

---

The purpose of this project was to create a weather application which presenting scraped and current data about weather and air pollution on 'streamlit share' host.

---

- [1. App preview](#1-app-preview)
- [2. Installation](#2-installation)

## 1. App preview

<h2>Main page</h2>
<div>
  
Using the API, the application acquires weather information and information on air pollution levels by pollen content. All this information is collected from actual weather stations that record all this data all the time. These are stored in a non-relational database such as MongoDB. Using cartographic primers in the form of GEOJSON files, we are able to average the collected results and present them in an appropriate manner. It is also possible to select the specific area for which the acquired data is to be displayed.
The application and its functionalities are described in Polish due to the requirements set by the subject leader, as this is a project carried out as part of a university course.
  
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API.png" width="1200" height="600" />
</div>

<h2>List of weather stations</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API2.png" width="1200" height="600" />
</div>

<h2>List of contamination</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API3.png" width="1200" height="600" />
</div>

<h2>List of contamination presented by heatmap</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API4.png" width="1200" height="600" />
</div>

<h2>Results for the country</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API5.png" width="1200" height="600" />
</div>

<h2>Results for the provinces</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API6.png" width="1200" height="600" />
</div>

<h2>Results for the districts</h2>
<div>
<img src="https://github.com/Psylo1226/APP-weather-application/blob/main/pictures/API7.png" width="1200" height="600" />
</div>

## 2. Installation

Make sure to use **Python version 3.10**.
Copy the repository by forking and then downloading it using:

```bash
git clone https://github.com/<YOUR-USERNAME>/APP-weather-application
```
  
Install requirements use:
  
```bash
cd APP-weather-application
pip install -r requirements.txt
```
  
Run App:

```bash
cd APP-weather-application
streamlit run app.py
```
  
