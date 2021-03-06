# -*- coding: utf-8 -*-
#
#    This file belongs to the ICTV project, written by Nicolas Detienne,
#    Francois Michel, Maxime Piraux, Pierre Reinbold and Ludovic Taffin
#    at Université catholique de Louvain.
#
#    Copyright (C) 2016-2018  Université catholique de Louvain (UCL, Belgium)
#
#    ICTV is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ICTV is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with ICTV.  If not, see <http://www.gnu.org/licenses/>.

from ictv.models.channel import PluginChannel
from ictv.plugin_manager.plugin_capsule import PluginCapsule
from ictv.plugin_manager.plugin_manager import get_logger
from ictv.plugin_manager.plugin_slide import PluginSlide
import requests
import json
import time
import datetime
import web
import math


def get_content(channel_id):
    channel = PluginChannel.get(channel_id)
    logger_extra = {'channel_name': channel.name, 'channel_id': channel.id}
    logger = get_logger('sncb', channel)
    departure_station = channel.get_config_param('departure_station')
    duration = channel.get_config_param('duration')*1000
    language = channel.get_config_param('language')
    nb_train = channel.get_config_param('nb_train')
    logo_1 = channel.get_config_param('logo_1')
    if not departure_station:
        logger.warning('Problem with the departure station', extra=logger_extra)
        return []
    else:
        base_url = "http://api.irail.be/"
        head = {'user-agent': 'ictv-plugin-sncb (https://github.com/OpenWeek/ictv-plugin-survey)'}
        payload = {'station': departure_station, 'arrdep': 'departures', 'lang': language, 'format': 'json',
                   'alert': 'true'}

        r = requests.get(base_url + 'liveboard/', params=payload, headers=head)
        parsed = json.loads(r.text)
        return [SNCBCapsule(departure_station, duration, language, nb_train, parsed, logo_1)]


class SNCBCapsule(PluginCapsule):
    def __init__(self, departure_station, duration, language, nb_train, parsed, logo_1):
        self._slides = []
        nb_page = math.ceil(nb_train/8)
        for page in range(nb_page):
            self._slides.append(SNCBSlide(departure_station, duration, language, parsed['departures']['departure'][page * 8 : min((page + 1) * 8, nb_train)], logo_1))
        self._theme = 'sncb'

    def get_slides(self):
        return self._slides

    def get_theme(self):
        return self._theme

    def __repr__(self):
        return str(self.__dict__)


class SNCBSlide(PluginSlide):

    def __init__(self, departure_station, duration,language, parsed, logo_1):
        self._departure_station = departure_station
        self._duration = duration

        big_template = """$def with (parsed, actual, departure_station, language)
        <table style='width: 100%'>
            <tr>
                <th>$departure_station</td>
                <th> </td>
                <th> </td>
                <th>Generated at $actual</td>
            <tr>
                $if language=='fr':
                    <th>Destination</th>
                    <th>Voie</th>
                    <th>Départ</th>
                    <th>Retard</th>
                $elif language=='nl':
                    <th>Bestemming</th>
                    <th>Spoor</th>
                    <th>Vertrek</th>
                    <th>Vertraging</th>
                $elif language=='de':
                    <th>Ziel</th>
                    <th>Weg</th>
                    <th>Abghen</th>
                    <th>Verzögerung</th>
                $else:
                    <th>Destination</th>
                    <th>Platform</th>
                    <th>Departure</th>
                    <th>Delay</th>


            </tr>
            $for train in parsed:
                <tr>
                    <td>$train['station']</td>
                    <td>$train['platform']</td>
                    <td>$time.strftime('%H:%M', time.localtime(int(train['time'])))</td>
                    $if int(train['delay']) != 0:
                        <td>+$(int(train['delay'])//60)'</td>
                    $elif int(train['canceled']):
                        $if language=='fr':
                            <td>Supprimé</td>
                        $elif language=='nl':
                            <td>Afschaft</td>
                        $elif language=='de':
                            <td>Abschaft</td>
                        $else:
                            <td>Canceled</td>
                    $else:
                        <td> </td>
                </tr>

        </table>"""
        # <td>$time.strftime('%H:%M', time.localtime(int(train['time'])))</td>
        template_builder = web.template.Template(big_template, globals={'int': int, 'time': time})

        self._content = {'text-1': {'text': str(template_builder(parsed,
                                                                 datetime.datetime.now().strftime('%H:%M'),
                                                                 departure_station,
                                                                 language))},
                         'title-1': {'text': 'SNCB Departures'},
                         'subtitle-1': {'text': departure_station},  # TODO: Localisation
                         'logo-1': {'src': logo_1},
                         'logo-2': {'src':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/LogoBR.svg/1298px-LogoBR.svg.png'}}

    def get_duration(self):
        return self._duration

    def get_content(self):
        return self._content

    def get_template(self):
        return 'template-sncb'

    def __repr__(self):
        return str(self.__dict__)


