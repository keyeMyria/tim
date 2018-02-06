// Info

define(function() {
  'use strict';

  var EvenviEvent = (function() {

    function EvenviEvent(event) {
      this.event = event;
    }

    EvenviEvent.EV_ID = '_id';
    EvenviEvent.EV_FEED = 'feed';
    EvenviEvent.EV_FEED_CODE = 'feed code';
    EvenviEvent.EV_FEEDER = 'feeder';
    EvenviEvent.EV_FEED_URL = 'feed url';
    EvenviEvent.EV_OBSERVATION_TIME = 'observation time';
    EvenviEvent.EV_SOURCE_TIME = 'source time';
    EvenviEvent.EV_AS_NAME = 'as name';
    EvenviEvent.EV_ASN = 'asn';
    EvenviEvent.EV_BG_PREFIX_ALLOCATED = 'bgp prefix allocated';
    EvenviEvent.EV_BGP_PREFIX = 'bgp prefix';
    EvenviEvent.EV_DOMAIN_NAME = 'domain name';
    EvenviEvent.EV_EMAIL_ADDRESS = 'email address';
    EvenviEvent.EV_IP = 'ip';
    EvenviEvent.EV_PORT = 'port';
    EvenviEvent.EV_REGISTRY = 'registry';
    EvenviEvent.EV_REVERSE_DNS = 'reverse dns';
    EvenviEvent.EV_URL = 'url';
    EvenviEvent.EV_SOURCE_AS_NAME = 'source as name';
    EvenviEvent.EV_SOURCE_ASN = 'source asn';
    EvenviEvent.EV_SOURCE_CC = 'source cc';
    EvenviEvent.EV_SOURCE_DOMAIN_NAME = 'source domain name';
    EvenviEvent.EV_SOURCE_IP = 'source ip';
    EvenviEvent.EV_SOURCE_PORT = 'source port';
    EvenviEvent.EV_DESTINATION_AS_NAME = 'destination as name';
    EvenviEvent.EV_DESTINATION_ASN = 'destination asn';
    EvenviEvent.EV_DESTINATION_CC = 'destination cc';
    EvenviEvent.EV_DESTINATION_DOMAIN_NAME = 'destination domain name';
    EvenviEvent.EV_DESTINATION_IP = 'destination ip';
    EvenviEvent.EV_DESTINATION_PORT = 'destination port';
    EvenviEvent.EV_OS_NAME = 'os name';
    EvenviEvent.EV_OS_VERSION = 'os version';
    EvenviEvent.EV_USER_AGENT = 'user agent';
    EvenviEvent.EV_REPORTED_AS_NAME = 'reported as name';
    EvenviEvent.EV_REPORTED_ASN = 'reported asn';
    EvenviEvent.EV_REPORTED_CC = 'reported cc';
    EvenviEvent.EV_REPORTED_IP = 'reported ip';
    EvenviEvent.EV_CC = 'cc';
    EvenviEvent.EV_CITY = 'city';
    EvenviEvent.EV_COUNTRY = 'country';
    EvenviEvent.EV_LATITUDE = 'latitude';
    EvenviEvent.EV_LONGITUDE = 'longitude';
    EvenviEvent.EV_ABUSE_CONTACT = 'abuse contact';
    EvenviEvent.EV_ADDITIONAL_INFORMATION = 'additional information';
    EvenviEvent.EV_COMMENT = 'comment';
    EvenviEvent.EV_DESCRIPTION_URL = 'description url';
    EvenviEvent.EV_DESCRIPTION = 'description';
    EvenviEvent.EV_HTTP_REQUEST = 'http request';
    EvenviEvent.EV_MALWARE_FAMILY = 'malware family';
    EvenviEvent.EV_MISSING_DATA = 'missing data';
    EvenviEvent.EV_PROTOCOL = 'protocol';
    EvenviEvent.EV_STATUS = 'status';
    EvenviEvent.EV_TARGET = 'target';
    EvenviEvent.EV_TRACKING_ID = 'tracking id';
    EvenviEvent.EV_TRANSPORT_PROTOCOL = 'transport protocol';
    EvenviEvent.EV_UUID = 'uuid';

    EvenviEvent.prototype.hasAttribute = function(attribute) {
      return this.event.hasOwnProperty(attribute);
    }

    EvenviEvent.prototype.getAttribute = function(attribute) {
      return this.event[attribute];
    }

    EvenviEvent.prototype.getAttributes = function() {
      var attributes = [];
      for (var attribute in this.event) {
        attributes.push(attribute);
      }
      return attributes;
    }

    return EvenviEvent;
  })();

  return EvenviEvent;
});
