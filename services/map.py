import openrouteservice
import polyline
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.geojson import GeoJsonMapLayer

from models.map import Map
from kivy.properties import StringProperty
from plyer import gps

gps_location = StringProperty()
gps_status = StringProperty('Start')


class MapBuilder:
    def __init__(self):
        self.api_key = "5b3ce3597851110001cf624860bbe2ce295c433185dd45a4f3e1ae18"
        self.current_zoom = 12
        self.map_popup = None

    def create_map_popup(self):
        self.map_popup = Popup(
            title='Карта',
            size_hint=(None, None),
            size=(400, 500),
            separator_color=[1, 0.478, 0, 1],
            background_color=[4, .4, .2, 1],
        )
        return self.map_popup

    def clear_way_marker(self, map_view):
        for child in map_view.children[:]:
            if isinstance(child, MapMarker):
                map_view.remove_widget(child)

    def create_map_with_route(self, start_longitude, start_latitude, end_longitude, end_latitude):
        map_view = MapView(lon=39.214167, lat=51.670833, zoom=self.current_zoom)
        self.add_markers_to_map(map_view, start_longitude, start_latitude, end_longitude, end_latitude)
        self.add_route_to_map(map_view, start_longitude, start_latitude, end_longitude, end_latitude)

        return map_view

    def add_markers_to_map(self, map_view, start_longitude, start_latitude, end_longitude, end_latitude):
        map_view.add_widget(MapMarker(lon=start_longitude, lat=start_latitude, source='img/map_marker.png'))
        map_view.add_widget(MapMarker(lon=end_longitude, lat=end_latitude, source='img/map_marker.png'))

    def add_route_to_map(self, map_view, start_longitude, start_latitude, end_longitude, end_latitude):
        client = openrouteservice.Client(key=self.api_key)
        directions = client.directions(coordinates=[[start_longitude, start_latitude], [end_longitude, end_latitude]],
                                       profile='driving-car')

        route_geometry = directions['routes'][0]['geometry']
        route_coordinates = polyline.decode(route_geometry)
        route_coordinates = [(lon, lat) for lat, lon in route_coordinates]

        for i in range(len(route_coordinates) - 2):
            geojson_data = {
                "type": "Feature",
                "properties": {
                    "stroke-width": 2.0,
                    "stroke": "#FF7900"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": route_coordinates[i:i + 2]
                }
            }
            print(route_coordinates[i:i + 2])

            geojson_layer = GeoJsonMapLayer(geojson=geojson_data)
            map_view.add_layer(geojson_layer)

    def update_route(self, map_view, route_coordinate):
        longitude, latitude = route_coordinate
        way_marker = MapMarker(lon=longitude, lat=latitude, source='img/delivery_marker.png')

        if hasattr(map_view, 'way_marker'):
            map_view.remove_widget(map_view.way_marker)

        map_view.way_marker = way_marker
        map_view.add_widget(way_marker)


    def request_android_permissions(self):
         from android.permissions import request_permissions, Permission
         request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION])

    def start_gps(self):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            self.request_android_permissions()
            gps.start()
        except NotImplementedError:
            self.gps_status = 'No equipment'

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat')
        longitude = kwargs.get('lon')
        altitude = kwargs.get('altitude')
        self.route_coordinate = [(latitude, longitude)]

    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def open_map(self, map_view, db_session, order_id):
        coord = Map.get_coord_by_id(db_session, order_id)

        self.start_gps()

        map_popup = self.create_map_popup()
        map_view = self.create_map_with_route(coord.start_longitude, coord.start_latitude,
                                              coord.end_longitude, coord.end_latitude)
        map_popup.content = map_view
        map_popup.open()

        def update_map_content(dt):
            self.update_route(map_view, self.route_coordinate)

        Clock.schedule_interval(update_map_content, 2)
