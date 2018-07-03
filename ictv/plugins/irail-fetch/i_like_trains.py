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

from ictv.model.channel import PluginChannel
from ictv.plugin_manager.plugin_capsule import PluginCapsule
from ictv.plugin_manager.plugin_manager import get_logger
from ictv.plugin_manager.plugin_slide import PluginSlide
from ictv.plugin_manager.plugin_utils import MisconfiguredParameters

def get_content(channel_id):
    channel = PluginChannel.get(channel_id)
    logger_extra = {'channel_name': channel.name, 'channel_id': channel.id}
    logger = get_logger('i_like_trains',channel)
    departure_station = channel.get_config_param('departure_station')
    if not departure_station:
        logger.warning('Problem with the departure station', extra=logger_extra)  #TODO Verifier gare existante
        return []
    else:
        return None

class ILikeTrainsCapsule(PluginCapsule):
    def __init__(self, departure_station, duration):
        self._slides = [ILikeTrainsSlide(departure_station,duration)]

    def get_slides(self):
        return self._slides

    def get_theme(self):
        return None

    def __repr__(self):
        return str(self.__dict__)



class ILikeTrainsSlide(PluginSlide):
    def __init__(self,departure_station, duration):
        self._departure_station = departure_station
        self._duration = duration
        self._content = None #TODO HTML
    def get_duration(self):
        return self._duration
    def get_content(self):
        return self._content
    def get_template(self):
        return 'template-text-center'
    def __repr__(self):
        return str(self.__dict__)


