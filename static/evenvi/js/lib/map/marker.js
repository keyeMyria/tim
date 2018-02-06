// Info

define(['lib/event/event'], function(EvenviEvent) {
  'use strict';

  var Marker = (function() {

    function Marker(map, event) {
      this.map = map;
      this.event = event;
      this.tipAttributes = [
        'timestamp',
        //EvenviEvent.EV_SOURCE_TIME,
        EvenviEvent.EV_IP,
        EvenviEvent.EV_FEED
      ];
      this.labelAttributes = [
        'timestamp',
        //EvenviEvent.EV_SOURCE_TIME,
        EvenviEvent.EV_IP,
        EvenviEvent.EV_FEED
      ];
    }

    Marker.prototype.tip = function() {
      var tip = '<div class="marker-tip">';

      for (var i = 0, len = this.tipAttributes.length; i < len; i++) {
        var attr =  this.tipAttributes[i];
        var attrLabel = '<span class="' + attr.replace(/ /g, '-') + '">';

        if (this.event.hasAttribute(attr)) {
          attrLabel += this.event.getAttribute(attr);
        } else {
          attrLabel += 'N/A';
        }

        attrLabel += '</span>';

        tip += attrLabel;
      }

      tip += '</div>';
      return tip;
    }

    Marker.prototype.label = function() {
      var label = '<div class="marker-label">';

      for (var i = 0, len = this.labelAttributes.length; i < len; i++) {
        var attr =  this.labelAttributes[i];
        var attrLabel = '<span class="' + attr.replace(/ /g, '-') + '">';

        if (this.event.hasAttribute(attr)) {
          attrLabel += this.event.getAttribute(attr);
        } else {
          attrLabel += 'N/A';
        }

        attrLabel += '</span>';

        label += attrLabel;
      }

      label += '<span class"marker-link"><a href="#">Details</a></span>';
      label += '</div>';
      return label;
    }

    Marker.prototype.id = function() {
      if (this.event.hasAttribute(EvenviEvent.EV_ID)) {
        return this.event.getAttribute(EvenviEvent.EV_ID);
      }
      return null;
    }

    Marker.prototype.name = function() {
      if (this.event.hasAttribute(EvenviEvent.EV_SOURCE_TIME)) {
        return this.event.getAttribute(EvenviEvent.EV_SOURCE_TIME);
      }
      return "";
    }

    Marker.prototype.latitude = function() {
      if (this.event.hasAttribute(EvenviEvent.EV_LATITUDE)) {
        return this.event.getAttribute(EvenviEvent.EV_LATITUDE);
      }
      return null;
    }

    Marker.prototype.longitude = function() {
      if (this.event.hasAttribute(EvenviEvent.EV_LONGITUDE)) {
        return this.event.getAttribute(EvenviEvent.EV_LONGITUDE);
      }
      return null;
    }

    Marker.prototype.hasLocation = function() {
      return this.event.hasAttribute(EvenviEvent.EV_LATITUDE)
          && this.event.hasAttribute(EvenviEvent.EV_LONGITUDE);
    }

    Marker.prototype.latLng = function() {
      if (this.hasLocation()) {
        return [this.latitude(), this.longitude()];
      }
      return [];
    }

    Marker.prototype.latLngStr = function() {
      if (this.hasLocation) {
        return this.latitude() + ',' + this.longitude();
      }
      return null;
    }

    return Marker;
  })();

  return Marker;
});
