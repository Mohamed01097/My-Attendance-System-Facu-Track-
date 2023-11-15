from odoo import http
import json

class LocationController(http.Controller):
    @http.route('/my_module/get_location', type='json', auth='public', methods=['POST'])
    def get_location(self, **kw):
        latitude = kw.get('latitude')
        longitude = kw.get('longitude')

        # Find the faculty course record based on your desired criteria
        faculty_course = http.request.env['facu_track.course'].search([('name', '=', 'Your Course Name')])

        if faculty_course:
            # Update the latitude and longitude fields of the faculty course record
            faculty_course.write({
                'latitude': latitude,
                'longitude': longitude,
            })

            return json.dumps({
                'success': True,
            })
        else:
            return json.dumps({
                'success': False,
                'message': 'Faculty course not found.',
            })
