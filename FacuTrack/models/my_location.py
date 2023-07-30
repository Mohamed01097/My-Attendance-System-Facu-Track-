from geopy.distance import distance
import geocoder

class GetUserlocation:

    def check_geo_distance(self,lat_student, long_student, lat_university, long_university):
        # Calculate the distance between the two points
        dist = distance((lat_student, long_student), (lat_university, long_university)).km
        # Check if the distance is within the specified range
        return dist

    def check_user_location(self):
        g = geocoder.ip('me')
        lat = g.latlng[0]
        lng = g.latlng[1]
        return lat,lng

    def check_if_range_available_or_not(self):
        available_range_of_uinversity = 150
        student_latitude = self.check_user_location()[0]
        student_longitude = self.check_user_location()[1]
        distance_between_student_and_university = self.check_geo_distance(student_latitude, student_longitude,
                                                                          29.0427804, 31.1090541)
        if distance_between_student_and_university <= available_range_of_uinversity:
            return True
        else:
            return False

