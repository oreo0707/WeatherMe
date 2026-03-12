Weather Me

Weather Me is a pixel-style desktop weather application built with Python and Tkinter.
The project combines programming, UI design, and pixel art to create an interactive weather experience where each weather condition is represented with a unique visual environment.
All graphical assets and backgrounds were hand-drawn in pixel style, and the interface was first prototyped in Figma before implementation.
The application retrieves real-time weather data using the OpenWeatherMap API and dynamically changes the visual environment depending on the weather conditions.

Introduction Video
https://drive.google.com/file/d/1dbOb3Yq-28qxrGjnLZ1iRdEZs65MRQRd/view?usp=sharing

Features
1. City Search
  -Users can enter a city name in the search bar.
  -Available cities are displayed dynamically.
  -Selecting a city retrieves real-time weather data.

2. Dynamic Weather Visuals
The interface changes depending on the weather condition.
Supported weather types:
  -Sunny
  -Rainy
  -Thunderstorm
  -Snow
  -Cloudy
Each weather condition includes:
  -Weather type header
  -Temperature (°C)
  -Location
  -Precipitation
  -Humidity
  -Wind speed

3. Custom Pixel Art Interface
All graphical elements were created manually, including:
  -Weather backgrounds
  -UI elements
  -Character portrait
  -Screen designs
The project uses a pixel art visual style for a cohesive aesthetic.

4. Light & Dark Mode
Users can toggle between light mode and dark mode, with adjusted assets for each theme.

5. Dynamic Background Music
Different background music is used across screens:
  -Main menu
  -Settings
  -Info page
  -Weather screens
Weather screens feature weather-appropriate background music for better immersion.

6. Settings Panel
Users can:
  -Toggle light/dark theme
  -Increase volume
  -Decrease volume
  -Mute/unmute music

7. Error Handling
The application handles invalid city inputs safely.
If a user selects a city that does not return weather data, the program prevents crashes and remains on the main screen.

8. Tech Stack
Programming Language: Python
Libraries / Frameworks: Tkinter (GUI framework)
APIs: OpenWeatherMap API
Design Tools: Figma (UI prototyping)
Assets: Custom pixel art created by the developer

9. Structure
Weather-Me

├── __pyache__

│

├── assets

│    ├── fonts

│    ├── icons

│    ├── music

│    ├── screen

│    ├── theme_toggle

│    └── volume

│

├── build

│   ├── main

│       ├── localpycs

│       ├── Analysis-00.toc

│       ├── base_library

│       ├── COLLECT-00.toc

│       ├── EXE-00.toc

│       ├── main.exe

│       ├── main.pkg

│       ├── PKG-00.toc

│       ├── PYZ-00.pyz

│       ├── PYZ-00.toc

│       ├── warn-main.txt

│       └── xref-main.html

│
├── dist

│   ├── main

│       ├── _internal

│       ├── main.exe

│       └── weatherme.zip

│

├── screens

│   ├── __pyache__

│   ├── __init__.py

│   ├── info.py

│   ├── menu.py

│   ├── settings.py

│   └── weather.py

│

├── screenshots

│   ├── light_info

│   ├── light_settings

│   ├── light_menu

│   ├── light_weather_sunny

│   ├── light_weather_rain

│   ├── light_weather_cloudy

│   ├── light_weather_snow

│   ├── light_weather_storm

│   ├── dark_info

│   ├── dark_settings

│   ├── dark_menu

│   ├── dark_weather_sunny

│   ├── dark_weather_rain

│   ├── dark_weather_cloudy

│   ├── dark_weather_snow

│   └── dark_weather_storm

│

├── services

│   ├── __pyache__

│   ├── __init__.py

│   └── weather_api.py

│

├── .gitattributes

├── config.py

├── utils.py

├── main.py

├── main.spec

├── weatherme.zip

└── weatherme_cmd.txt

11. Installation
1. Download weatherme.zip
2. Navigate to assets and download the font(.ttf)
3. Build executable using weatherme_cmd.txt
4. Run the application in dist/main/main.exe

11. Skills Demonstrated
  - GUI development with Tkinter
  - API integration
  - JSON data processing
  - UI/UX prototyping with Figma
  - modular Python project architecture
  -  asset design and pixel art creation
  - packaging applications using PyInstaller

12. Motivation
This project was created to combine software development with creative design.
The goal was to build an application that merges:
  -programming
  -digital art
  -user experience design
I enjoy designing projects that people can visually appreciate and interact with, while also gaining practical experience in real-world programming concepts such as API integration and GUI development.

Author
Created by Anthea Lua
