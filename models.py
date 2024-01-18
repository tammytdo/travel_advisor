class WeatherDay:
  def __init__(self, weather_object):
    self.date = weather_object.get('datetime', None)
    self.min_temp = weather_object.get('min_temp' , None)
    self.max_temp = weather_object.get('max_temp', None)
    self.description = weather_object.get('weather', None).get('description', None)
    self.weather_icon = weather_object.get('weather', None).get('icon', None)

  def to_json(self):
      return {
          "date": self.date,
          "min_temp": self.min_temp,
          "max_temp": self.max_temp,
          "description": self.description
      }