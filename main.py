import sys
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import RequestException

#version 2 for the testing
#main class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.user_prompt = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.degrees_display = QLabel(self)
        self.symbol_display = QLabel(self)
        self.symbol_description = QLabel(self)

        self.initUI()

    def initUI(self):
        #main window config
        self.setWindowTitle("Weather App")

        #labels config


        #pushbutton config


        #line edit config
        self.city_input.setMaxLength(50)


        #general style sheet
        self.user_prompt.setObjectName("user_prompt")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.degrees_display.setObjectName("degrees_display")
        self.symbol_display.setObjectName("symbol_display")
        self.symbol_description.setObjectName("symbol_description")

        self.setStyleSheet("""
            QLabel{
                font-family: calibri;
                font-size: 40px;
            }
            QPushButton{
                font-family: calibri;
                font-size: 30px;
                font-weight: bold;
                background-color: #b3afaf;
            }
            QLineEdit{
                font-size: 40px;
            }
            QLabel#degrees_display{
                font-size: 75px;
                font-family: Segoe UI emoji;
            }
            QLabel#symbol_display{
                font-size: 100px;
            }
            QLabel#symbol_description{
                font-size: 50px;
            }
            """)

        #layout manager
        vbox = QVBoxLayout()
        vbox.addWidget(self.user_prompt)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.degrees_display)
        vbox.addWidget(self.symbol_display)
        vbox.addWidget(self.symbol_description)

        self.setLayout(vbox)

        #alignments
        self.user_prompt.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.degrees_display.setAlignment(Qt.AlignCenter)
        self.symbol_display.setAlignment(Qt.AlignCenter)
        self.symbol_description.setAlignment(Qt.AlignCenter)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "b2130e73e0b1ed295a953c9e16b18d7f"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as HTTP_error:
            match response.status_code:
                case 404:
                    self.display_error(f"City does not exist:\nplease try again")
                case 401:
                    self.display_error(f"Unauthorized access:\nInvalid API key")
                case 403:
                    self.display_error(f"forbidden:\naccess is denied")
                case 404:
                    self.display_error(f"Not found:\ncity not found")
                case 500:
                    self.display_error(f"Internal server error:\nplease try again later")
                case 502:
                    self.display_error(f"Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error(f"Service unavailable:\nServer is down")
                case 503:
                    self.display_error(f"Gateway Timeout:\nNo response from the Server")
                case _:
                    self.display_error(f"http error occurred:\n{HTTP_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Check your internet connection")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\n Check the URL")

    def display_error(self, message):
        self.degrees_display.setText(message)
        self.degrees_display.setStyleSheet("font-size: 30px;")
        self.symbol_display.clear()
        self.symbol_description.clear()

    def display_weather(self, data):
        self.degrees_display.setStyleSheet("font-size: 75px;")
        #print(data)
        temperature = data["main"]["temp"] - 273.15
        weather_description = data["weather"][0]["description"]

        self.degrees_display.setText(f"{temperature:.0f}°C")
        self.symbol_description.setText(weather_description)

        weather_symbol = data["weather"][0]["id"]
        self.symbol_display.setText(self.display_symbol_func(weather_symbol))

    @staticmethod
    def display_symbol_func(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


#main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
