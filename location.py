# This is based on data from https://footprinthero.com/solar-panel-tilt-angle-calculator

# One should obviously install geocoder https://geocoder.readthedocs.io
import geocoder
from datetime import date, datetime

def stanford_rule(latitude):
    # As based on https://web.stanford.edu/group/efmh/jacobson/Articles/I/TiltAngles.pdf
    if (latitude > 0): # Northern hemisphere
        return 1.3793 + latitude * (1.2011 + latitude * (-0.014404 + latitude * 0.000080509))
    elif (latitude < 0): # Southern hemisphere
        return -0.41657 + latitude * (1.4216 + latitude * (0.024051 + latitude * 0.00021828))

def tilt_angle(latitude, today=date.today(), movingPanel=False):
    today = date.today()

    # Each month gets some extra degrees of tilting, according to the season. Month zero does not exist
    monthly_deltas = (0, 10, 5, 0, -5, -10, -15, -10, -5, 0, 5, 10, 15 )
 
    # Gives the monthly factor according to the current month and hemisphere
    monthly_factor = monthly_deltas[today.month] if latitude >0 else -1 * monthly_deltas[today.month]

    return stanford_rule(latitude)+monthly_factor if movingPanel else stanford_rule(latitude)



if __name__ == "__main__":
    myLocation = geocoder.ip('me')

    print("I have a moving solar panel, so the best angle for this month is", tilt_angle(myLocation.lat, movingPanel=True))
    print("Example for Anaheim, CA, with a fixed solar panel", tilt_angle(geocoder.arcgis('Anaheim, CA').lat))
