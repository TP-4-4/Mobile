import tempfile
import threading

import openrouteservice
import polyline
import yaml
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy.core.window import Window
from plyer import gps
from kivy.uix.label import Label
from kafka import KafkaProducer
import requests

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

url = "https://storage.yandexcloud.net/cloud-certs/CA.pem"
response = requests.get(url)
if response.status_code == 200:
    cert_data = response.content.decode('utf-8')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".crt") as temp_cert_file:
        temp_cert_file.write(cert_data.encode('utf-8'))
        temp_cert_path = temp_cert_file.name
else:
    print("Ошибка при загрузке файла:", response.status_code)

class MapBuilder:
    def __init__(self):
        self.api_key = f'{config["api"]["key"]}'
        self.current_zoom = 12
        self.map_popup = None
        self.route_coordinate = []
        self.gps_started = False
        self.gps_status = 'provider-disabled'
        self.gps_popup = None
        self.gps_check_started = False
        self.route_coordinate_updated = False
        self.check_stat = None

    def create_map_popup(self):
        window_width, window_height = Window.size

        popup_width = window_width * 0.9
        popup_height = window_height * 0.8
        self.map_popup = Popup(
            title='Карта',
            title_font='styles/Montserrat-ExtraBold.ttf',
            title_align='center',
            size_hint=(None, None),
            size=(popup_width, popup_height),
            separator_color=[1, 1, 1, 1],
            background_color=[255, 255, 255, 1],
            title_color=[1, 0.478, 0, 1],
            overlay_color=[1, 0.478, 0, 0.41],
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

    def update_route(self, map_view):

        print('GPS ROUTES', self.route_coordinate)
        if self.route_coordinate_updated:
            latitude, longitude = self.route_coordinate
            way_marker = MapMarker(lon=longitude, lat=latitude, source='img/delivery_marker.png')
            if hasattr(map_view, 'way_marker'):
                map_view.remove_widget(map_view.way_marker)
            map_view.way_marker = way_marker
            map_view.add_widget(way_marker)
            self.route_coordinate_updated = False

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission
        def callback(permission, results):
            if all([res for res in results]):
                print('Got All Permissions')
            else:
                print('Did Not Get All Permissions')

        request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION], callback)

    def start_gps(self):
        if not self.gps_started:
            try:
                self.request_android_permissions()
                gps.configure(on_location=self.on_gps_location, on_status=self.on_auth_status)
                gps.start(minTime=1000, minDistance=0)
                print('gps started')
                self.gps_started = True

            except NotImplementedError:
                self.gps_status = 'No equipment'

    def check_gps(self):
        gps.configure(on_location=self.on_gps_location, on_status=self.on_auth_status)
        gps.start(minTime=1000, minDistance=0)

    def start_gps_status_check(self):
        if not self.gps_check_started:
            self.check_stat = Clock.schedule_interval(self.check_gps_status, 2)
            self.gps_check_started = True

    def stop_gps(self):
        if self.gps_started:
            gps.stop()
            self.gps_started = False
            self.gps_check_started = False
            print('gps stopped')

    def on_gps_location(self, **kwargs):
        self.gps_status = 'provider-enabled'
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        print('GPS POSITION', latitude, longitude)
        self.route_coordinate = [latitude, longitude]
        self.route_coordinate_updated = True
        serialized_data = f"{latitude} {longitude}"
        kafka_thread = threading.Thread(target=self.send_serialized_data_to_kafka, args=(serialized_data,))
        kafka_thread.start()

    def on_auth_status(self, general_status, status_message):
        print('on_auth_status = ', general_status, status_message)
        if status_message == 'gps':
            self.gps_status = general_status
        if general_status == 'provider-disabled' and status_message == 'gps':
            self.start_gps_status_check()

    def open_gps_access_popup(self):
        window_width, window_height = Window.size

        popup_width = window_width * 0.75
        popup_height = window_height * 0.2

        content = Label(
            text='You need to enable GPS access for the app to function properly',
            text_size=(popup_width * 0.9, None),
            halign='center',
            valign='middle',
            padding=(10, 10),
            color=[1, 0.478, 0, 1],
            font_name='styles/Montserrat-Bold.ttf',
            font_size='12sp',
        )

        self.gps_popup = Popup(
            title='GPS Error',
            title_font='styles/Montserrat-ExtraBold.ttf',
            title_align='center',
            content=content,
            size_hint=(None, None),
            size=(popup_width, popup_height),
            separator_color=[1, 1, 1, 1],
            background_color=[255, 255, 255, 1],
            title_color=[1, 0.478, 0, 1],
            overlay_color=[1, 0.478, 0, 0.41],
        )
        self.gps_popup.bind(on_dismiss=self.reset_gps_popup)
        self.gps_popup.open()

    def reset_gps_popup(self, *args):
        self.gps_popup = None

    def check_gps_status(self, *args):
        status = self.gps_status
        print('status = ', status)
        if status == 'provider-disabled':
            self.check_gps()
            if self.gps_popup is None:
                self.open_gps_access_popup()
        else:
            Clock.unschedule(self.check_stat)
            self.gps_check_started = False
            self.check_gps()
            if self.gps_popup:
                self.gps_popup.dismiss()


    def send_serialized_data_to_kafka(self, serialized_data):
        producer = KafkaProducer(
            bootstrap_servers=['rc1a-clts7qbo7ml5kl80.mdb.yandexcloud.net:9091',
                               'rc1b-8kvb7n4m4aql8c9f.mdb.yandexcloud.net:9091',
                               'rc1d-nmfkkgq12lhnfm0p.mdb.yandexcloud.net:9091'],
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username='write',
            sasl_plain_password='k8lobova',
            ssl_cafile=temp_cert_path)
        producer.send('coordinates', serialized_data.encode('utf-8'), b'coord')
        producer.flush()
        producer.close()

