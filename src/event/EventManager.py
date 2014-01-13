from event.OmniEvent import OmniEvent

__author__ = 'Sefverl'


class EventManager:
    def __init__(self):
        self.subscribers = {}

    def fireEvent(self, event):
        """
            Fire an OmniEvent, sending a copy to all subscribers of an event
        :param event: Event object containing information about the source and so on
        :type event: OmniEvent
        :return: none
        :rtype: none
        """

        print("EventManager: Event triggered")
        print("EventManager: # of current subscribers: " + str(len(self.subscribers)))
        print("Type: ", type(event))
        print("State of EventManager: ", self.__dict__)
        if len(self.subscribers) > 0 and type(event) == OmniEvent:
            print("EventManager: Event validated!")
            event_dev_id = event.device_id
            event_payload = dict(event.payload)
            print("EventManager: Event content: " + event_dev_id + " : " + str(event_payload))

            for subscriber in self.subscribers:
                print(
                "Subscriber: ", subscriber.getSubscriberType, " ", subscriber.getUniqueID, " ", subscriber.requests)
                print("Data type: ", event_payload['data_type'])
                if (event_payload['data_type'] in subscriber.requests) and \
                        (event_dev_id in subscriber.requests[event_payload['data_type']]):
                    print(
                    "Executing Callback of subscriber: " + str(subscriber.getSubscriberType()) + " with ID: " + str(
                        subscriber.getUniqueID()))
                    callback_func = self.subscribers[subscriber]
                    callback_func(event)

    def subscribe(self, callback_func, request):
        subscribe_dict = self.subscribers
        subscribe_dict[request] = callback_func
        EventManager.subscribers = subscribe_dict

    @staticmethod
    def unsubscribe(self, callback_func, request):

        if request in self.subscribers:
            del self.subscribers[request]

