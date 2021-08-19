# Is it cool out yet?

I'm too lazy to look at my watch so here's a script that hits a weather API to see if the temperature has dropped to a tolerable level after a hot day, and texts me to let me know to open the windows.

## Install & Run

  pip install requirements.txt
  python main.py

## You want this?

Cool! Grab yourself a free tier twilio account from https://www.twilio.com/, and a free tier open weather map account from https://home.openweathermap.org/.
Next, rename `config.yaml.example` to `config.yaml` and fill in the values.

Hopefully they're all obvious. Refer to ISO 3166 for state and country codes.

The heat threshold should be thought of as the outdoor temperature (fahrenheit) that starts to make your living space uncomfortably warm.
The cold threshold should be just above room temperature, or whatever you feel is most comfortable.

## Future improvements

Probably account for the fact that 80 degrees and cloudy doesn't heat up the inside of a house as much as 80 degrees and sunny.
