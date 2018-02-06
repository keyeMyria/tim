import socket
import idiokit
from abusehelper.core import cymruwhois
from abusehelper.bots.augmenter import geoipaugment

import idiokit
from hashlib import sha1
from abusehelper.core import events, taskfarm
#from abusehelper.core import bot
from oneiros import bot 


class _RoomBot(bot.ServiceBot):
    def __init__(self, *args, **keys):
        bot.ServiceBot.__init__(self, *args, **keys)
        self.room_handlers = taskfarm.TaskFarm(self._handle_room)

    @idiokit.stream
    def _handle_room(self, name):
        msg = "room {0!r}".format(name)
        attrs = events.Event(type="room", service=self.bot_name, room=name)

        with self.log.stateful(repr(self.xmpp.jid), "room", repr(name)) as log:
            log.open("Joining " + msg, attrs, status="joining")
            room = yield self.xmpp.muc.join(name, self.bot_name)

            log.open("Joined " + msg, attrs, status="joined")
            try:
                yield room
            finally:
                log.close("Left " + msg, attrs, status="left")

    def to_room(self, name):
        return self.room_handlers.inc(name) | idiokit.consume()

    def from_room(self, name):
        return idiokit.consume() | self.room_handlers.inc(name)



class EventAugmenter(_RoomBot):

    ip_key = bot.Param("key which has IP address as value " +
                       "(default: %default)", default="ip")
    geoip_db = bot.Param("Location of the Maxmind geoip DB file "
			 + "(default: %default)", 
			default="/srv/oneiros/geoipdb/GeoLite2-City.mmdb")

    def __init__(self, *args, **keys):
        _RoomBot.__init__(self, *args, **keys)
        self._augments = taskfarm.TaskFarm(self._handle_augment)
	self.geoip = geoipaugment.GeoIPAugmenter(self.geoip_db)
	print self.geoip
	self.ip_key = "source_ip"

    def _handle_augment(self, src_room, dst_room, args):
        return idiokit.pipe(
            self.from_room(src_room),
            events.stanzas_to_events(),
            self.augment(*args),
            events.events_to_elements(),
            self.to_room(dst_room)
        )

    @idiokit.stream
    def session(self, state, src_room, dst_room=None, **keys):
        if dst_room is None:
            dst_room = src_room

        augments = list()
        for args in self.augment_keys(src_room=src_room,
                                      dst_room=dst_room,
                                      **keys):
            augments.append(self._augments.inc(src_room, dst_room, args))
        yield idiokit.pipe(*augments)

    def augment_keys(self, *args, **keys):
        yield ()


    @idiokit.stream
    def _geoip_lookup(self, event):
	self.ip_key = "ip"
	if event.contains(self.ip_key):
           ip = event.value(self.ip_key)
           geoip_result = self.geoip.geomap(ip)
           result = geoip_result.next()
           if result:
	       for key, value in result.items():
                   event.add(key, str(value[0]))
	   else:
		self.log.info("No geomap info for ip: %s"%ip) 
		yield idiokit.send(event)
           yield idiokit.send(event)


    @idiokit.stream
    def _asn_lookup(self, event, resolver=None, cache_time=0):
	lookup = cymruwhois.OriginLookup(resolver, cache_time=cache_time)
	asn_dict = {}
        event = yield idiokit.next()
	if event.contains(self.ip_key):
	   ip = event.values(self.ip_key)
	   asns = yield lookup.lookup(ip[0])
	   for asn in asns:
	       for key, value in asn:
	           event.add(key, value)
	yield idiokit.send(event)


    @idiokit.stream
    def _asn_names_lookup(self, resolver=None, cache_time=4 * 60 * 60):
	lookup = cymruwhois.ASNameLookup(resolver, cache_time=cache_time)
        while True:
           asn_dict = {}
           event = yield idiokit.next()
	   if event.contains("asn"):
              asn_value = event.value("asn")
	      asns = yield lookup.lookup(asn_value)
              for asn in asns:
                  for key, value in asn:
                      event.add(key, value)
           yield idiokit.send(event)


    @idiokit.stream
    def augment(self):
        while True:
	    event = yield idiokit.next()	
	    yield self._geoip_lookup(event) | self._asn_lookup(event) | self._asn_names_lookup()

if __name__ == "__main__":
    EventAugmenter.from_command_line().execute()
