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
from ictv.plugin_manager.plugin_utils import MisconfiguredParameters


def get_content(channel_id):
    channel = PluginChannel.get(channel_id)
    logger_extra = {'channel_name': channel.name, 'channel_id': channel.id}
    logger = get_logger('i_like_trains', channel)
    departure_station = channel.get_config_param('departure_station')
    duration = channel.get_config_param('duration')
    if not departure_station:
        logger.warning('Problem with the departure station', extra=logger_extra)  #TODO Verifier gare existante
        return []
    else:
        return [ILikeTrainsCapsule(departure_station, duration)]


class ILikeTrainsCapsule(PluginCapsule):
    def __init__(self, departure_station, duration):
        self._slides = [ILikeTrainsSlide(departure_station,duration)]
        self._theme = 'train'

    def get_slides(self):
        return self._slides

    def get_theme(self):
        return self._theme

    def __repr__(self):
        return str(self.__dict__)


class ILikeTrainsSlide(PluginSlide):

    def __init__(self, departure_station, duration):
        self._departure_station = departure_station
        self._duration = duration #TODO Ajouter les heures
        self._content = {'text-1': {'text': """

        <table style="width:100%">
            <tr>
                <th>{}</td>
                <th> </td>
                <th> </td>
                <th>{}</td>
            <tr>
                <th>Destination</th>
                <th>Voie</th>
                <th>Départ</th>
                <th>Retard</th>
            </tr>

            <tr>
                <td>Rome</td>
                <td>42</td>
                <td>13:55</td>
                <td>+55</td>
            </tr>
            <tr>
                <td>Poudlard</td>
                <td>9.75</td>
                <td>9:30</td>
                <td> </td>
            </tr>
        </table>
        """.format(departure_station, '12:00')}, 'title-1': {'text': ''}, 'subtitle-1': {'text': ''}}

    def get_duration(self):
        return self._duration

    def get_content(self):
        return self._content

    def get_template(self):
        return 'template-train'

    def __repr__(self):
        return str(self.__dict__)


