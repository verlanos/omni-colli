__author__ = 'Sefverl'

import datetime


class SubscriberRequest(object):
    def __init__(self, subscriber_instance):
        self.subscriber_id = str(subscriber_instance) + str(datetime.datetime.now())
        self.requests = {}
        self.subscriber = subscriber_instance

    def getUniqueID(self):
        return self.subscriber_id

    def getSubscriberType(self):
        return type(self.subscriber)

    def addRequest(self, data_type, device_ids):
        """
            Adds a requirement for given type of data from devices with given device_ids
        :param data_type: type of sensor data requested
        :type data_type: int/enum string
        :param device_ids: one or more device ids
        :type device_ids: int/string
        :return: none
        :rtype: none
        """
        if data_type in self.requests:
            existing_list = self.requests[data_type]
            diff = list(set(device_ids) - set(existing_list))
            existing_list.join(diff)
        else:
            self.requests[data_type] = device_ids

    def removeRequest(self, data_type, device_ids):
        """
            Removes entire requirement for given data type (if all device IDs are listed). If one or more device_ids
            are listed remove them from the request. If all requested device_ids have been removed, remove entire
            request
        :param data_type: data_type to remove
        :type data_type: int/enum string
        :param device_ids: device_ids to remove
        :type device_ids: list of int/string
        :return: none
        :rtype: none
        """
        if data_type in self.requests:
            existing_list = self.requests[data_type]
            diff = list(set(existing_list) - set(device_ids))
            if len(diff) == 0:
                del self.requests[data_type]
            else:
                self.requests[data_type] = diff

    def __eq__(self, other):
        if type(other) is type(self):
            return other.__dict__ == self.__dict__
        else:
            return False

