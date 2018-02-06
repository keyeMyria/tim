// Info

define(['jquery', 'lib/map/marker', 'lib/ui/modal', 'jquery-jvectormap', 'jquery-jvectormap-world-mill'], function($, Marker, Modal) {
  'use strict';

  function clearObject(object) {
    for (var property in object) {
      deleteProperty(object, property);
    }
  }

  function deleteProperty(object, property) {
    if (object.hasOwnProperty(property)) {
      delete object[property];
    }
  }

  function getProperty(object, property) {
    if (object.hasOwnProperty(property)) {
      return object[property];
    }
    return null;
  }

  var EvenviMap = (function() {

    function EvenviMap() {
      this.mapElement = $('#evenvi-map');
      this.modal = new Modal('#selector');
      // TODO: seems that it is not needed
      // this.resize();
      this.markers = {};
      this.markerIds = {};
      this.mapElement.vectorMap({
        map: 'world_mill',
        backgroundColor: '#3a3a4e',
        markerStyle: {
          initial: {
            fill: 'red',
            stroke: 'red',
            r: 3
          }
        },
        series: {
          markers: [],
          regions: [{
            scale: ['#FFFFFF', '#0071A4'],
            attribute: 'fill',
            normalizeFunction: 'linear',
            values: {}
          }]
        },
        onRegionTipShow: (function(_this) {
          return function(ev, label, code) {
            return label;
          };
        })(this),
        onMarkerTipShow: (function(_this) {
          return function(e, label, code) {
            var markers = _this.markers[code],
            markersLen = markers.length,
            i, labelHtml = '';

            labelHtml += '<div>';
            for (i = 0; i < markersLen; i++) {
              var marker = markers[i];
              labelHtml += marker.tip();
            }
            labelHtml += '</div>';

            label.html(labelHtml);
            return label;
          };
        })(this),
        onMarkerClick: (function(_this) {
          return function(e, code) {
            var markers = _this.markers[code],
            markersLen = markers.length,
            i, labelHtml = '';

            for (i = 0; i < markersLen; i++) {
              var marker = markers[i];
              labelHtml += marker.label();
            }

            _this.modal.append(labelHtml);
            _this.modal.show();
            return;
          };
        })(this)
      });
      this.mapObject = this.mapElement.vectorMap('get', 'mapObject');
    }

    EvenviMap.prototype.resize = function() {
      console.log('EvenviMap.resize');
      this.mapElement.width($(document).width() - 100);
      this.mapElement.height(0.8 * $(document).height());
    }

    EvenviMap.prototype.clear = function() {
      console.log('EvenviMap.clear');
      this.mapObject.removeAllMarkers();
      clearObject(this.markers);
      clearObject(this.markerIds);
    }

    // TODO: does not work!!!
    EvenviMap.prototype.removeOldestMarker = function() {
      console.log("EvenviMap.removeOldestMarker");
      var id, parent, toRemove, markers;
      toRemove = jQuery(this.mapElement.find("svg g circle.jvectormap-marker[fill=red]")[0]);
      parent = toRemove.parent();
      id = toRemove.attr('data-index');

      console.log("id: " + id);

      // problem do not know what to delete
      markers = getProperty(this.markers, id);
      console.log(marker);

      delete this.captions[id];
      this.mapObject.removeMarkers([id]);
      return parent.remove();
    };

    EvenviMap.prototype.addEvent = function(event) {
      console.log('EvenviMap.addEvent');
      this.addMarker(new Marker(this, event));
    }

    EvenviMap.prototype.addMarker = function(marker) {
      if (!marker.hasLocation()) {
        console.log('EvenviMap.addMarker no location');
        return;
      }

      var markerId = marker.id();
      if (this.markerIds.hasOwnProperty(markerId)) {
        console.log('EvenviMap.addMarker existing markerId: ' + markerId);
        return;
      }
      console.log('EvenviMap.addMarker adding markerId: ' + markerId);
      this.markerIds[markerId] = true;

      var latLngStr = marker.latLngStr();
      if (this.markers.hasOwnProperty(latLngStr)) {
        this.markers[latLngStr].push(marker);
      } else {
        this.markers[latLngStr] = [marker];
      }
      if (this.mapObject.markers[latLngStr]) {
        return;
      }
      this.mapObject.addMarker(latLngStr, { latLng: marker.latLng(), name: latLngStr }, []);
    }

    return EvenviMap;
  })();

  return EvenviMap;
});
