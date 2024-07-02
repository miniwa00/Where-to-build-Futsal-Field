# Where to build Futsal Field in Seoul?
## !! Map is not available now !!
## Overview
- This is a **Data Visualization** project that overlaps various data on the map of Seoul using **Folium**, a mapping library of Python.  
- I thought I could find the best place to build a futsal field and figure out the intersection between various data by overlaping data on the map.
- I used **streamlit** to create a demo app that can easily visualize and display data.

  
## What is Futsal?
**Futsal** is a fast-paced indoor sport that is similar to soccer but played on a smaller, hard court.   
It typically involves two teams, each with five players on the field at a time, including a goalkeeper.   
The game focuses on quick passes, close ball control, and skillful plays.     
<img src="https://github.com/miniwa00/Where-to-build-Futsal-Field/assets/47784464/0a95b61b-89c5-4a67-a063-18fa1b234989" width=300, height=200/>  
And here is the international standard of futsal field.  
<img src="https://github.com/miniwa00/Where-to-build-Futsal-Field/assets/47784464/097458c4-2eff-4bf5-9232-68ccb03d9b1d" width=400, height=300/>  
As you can see, futsal field is not as big as regular soccer field.   
So it can be built on the roof of buildings or in buildings if there is enough place for it.
Due to the high rent fee, there are lots of indoor or rooftop futsal field in Seoul.  
## Datasets Used
I collected 5 data from various sources. And I appropriately modified the structure of datasets not a raw data. 

- **Seoul Living Population Data**: This data is based on public big data and mobile telecommunication data collected by the Seoul Metropolitan Government and KT, representing the entire population in specific areas of Seoul at a particular moment. This data is for Wednesday, May 24, 2023, making it quite up-to-date. (Data collection is ongoing, with a four-day interval, so those interested should take note.)
The reason we chose Wednesday data is that it falls in the middle of the workweek. On holidays, people tend to have more time, and futsal fields can operate all day. However, on weekdays, most of the daytime hours are occupied with work. Therefore, we started with the idea that locating futsal fields in the best possible places could minimize this daytime idleness.

- **Seoul Population Density Data**: This dataset contains population density data for Seoul's administrative districts (dong) in the year 2022. Population density is a static dataset and does not change over time, unlike mobile population data.

- **Seoul City Public Parking Lot Data**: This dataset is the updated list of public parking lots in Seoul as of April 2023.

- **Seoul Metropolitan Subway Boarding and Embarking Passengers Data**: This dataset provides information on the number of passengers boarding and embarking from the Seoul metropolitan subway system from January 2015 to April 2023. From this dataset, we have extracted and utilized data from January 2023 to April 2023, averaging it by station to create 2023 data. It represents the number of boarding and embarking passengers for each station across all time periods.

- **Seoul Private/Public Futsal Field Data**: This dataset compiles data on most of the futsal fields within Seoul by directly searching on Naver Maps and organizing it into a CSV file. The term 'most of the futsal fields' is used because this dataset takes into account the possibility of 1. futsal fields that cannot be found through search and 2. cases where futsal field information is available but the operational status cannot be determined."

## Technique Used
<table>
<tbody>
    <tr>
        <td>
            <div align="center"><img src="https://github.com/miniwa00/Urban-Sport-Field-Keyword-Analysis/assets/47784464/f8ac5984-af72-4233-9045-08df71a7cbf4" width="100" height="50"/> 
            <br>Python</br></div>
        </td>
        <td>
            <div align="center"><img src="https://github.com/miniwa00/Where-to-build-Futsal-Field/assets/47784464/44ed302d-42a0-409e-b600-75fdf17f5f23" width="100" height="50"/> 
        <br>Folium</br></div>
        </td>
        <td>
            <div align="center"><img src="https://github.com/miniwa00/Where-to-build-Futsal-Field/assets/47784464/416bb3a3-53e2-42b6-a022-563845fca3dc" width="100" height="50"/> 
            <br>Streamlit</br></div>
        </td>
</tbody>
</table>

## How to run?
1. Go to the directory that you want to start
  - `cd path/you/want`

2. Download codes or clone the repository.
  - `git clone https://github.com/miniwa00/Where-to-build-Futsal-Field.git`

3. Download the necessary packages.
  - `pip install -r requirements.txt`

4. Enter the following command in terminal:
  - `streamlit run main.py`

4. Explore it!

## Features
<img src="https://github.com/miniwa00/Where-to-build-Futsal-Field/assets/47784464/6d675c77-d2d0-404b-a2e6-6b1820412d7d" width=500, height=450/>      

<br>
<br>

- you can see the **'서을 생활인구 데이터(누적)'** and **'서울 생활인구 데이터(평균)'**. Both of them is based on 'Seoul Living Population Data'.  
But if you modify the slide bar of each one, you can see the data at individual times and the accumulation of that data in the first one  
and you can see the average population in the selected time zone in the second one.

- **'서울 인구밀도 데이터'** and **'서울 주차장 데이터'** can be easily checked by clicking the checkbox.
  And **'서울 풋살장 데이터'** also easy to toggle it.

- If you want to check the subway boarding and embarking data, you need to choose option in the text box.
  then you can modify the slide bar.
  And you can see the circle marker that changes depending on population.

- when you toggle this slide bar you can see the change in the barplot under the map.
  This is the boarding and disembarking number of the population of selected subway line in selected time zone.

- The very last barplot Displays the population of the selected region in numbers.

- A button on the top-right of the map is 'layer button' which can control what to display on the map.