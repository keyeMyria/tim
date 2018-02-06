// Info

define(['lib/map/map', 'lib/event/event', 'lib/feed/ajax-feed', 'lib/toolbar/toolbar'], function(EvenviMap, EvenviEvent, AjaxFeed, Toolbar) {
    'use strict';

  var Evenvi = (function() {

    function Evenvi(config) {
      this.config = config;
      this.toolbar = new Toolbar({
        'selector': '#evenvi-toolbar',
        'loadCallback': (function(_this) {
          return function(from, to) {
            _this.load(from, to);
          };
        })(this),
        'liveCallback': (function(_this) {
          return function() {
            _this.stop();
            _this.clearMap();
            _this.start();
          };
        })(this)
      });
      this.map = new EvenviMap();
      this.feed = new AjaxFeed({
        'feedUrl': 'http://abuseh.oneiros.eu/map/events/',
        'pollInterval': 60000,
        'doneCallback': (function(_this) {
          return function(data, textStatus, jqXHR) {
            console.log('Evenvi.doneCallback');
            _this.addEvents(data['data']);
          };
        })(this),
        'failCallback': (function(_this) {
          return function(jqXHR, textStatus, errorThrown) {
            console.log('Evenvi.failCallback');
          };
        })(this)
      });
    }

    Evenvi.prototype.start = function() {
      console.log('Evenvi.start');
      this.feed.start();
    }

    Evenvi.prototype.stop = function() {
      console.log('Evenvi.stop');
      this.feed.stop();
    }

    Evenvi.prototype.load = function(from, to) {
      console.log('Evenvi.load');
      this.stop();
      this.clearMap();

      this.feed.load(from, to);
    }

    Evenvi.prototype.clearMap = function() {
      console.log('Evenvi.clearMap');
      this.map.clear();
    }

    // TODO: maybe should remove old events
    Evenvi.prototype.addEvent = function(event) {
      console.log('Evenvi.addEvent');
      console.log(event);
      var evenviEvent = new EvenviEvent(event);
      this.map.addEvent(evenviEvent);
    }

    Evenvi.prototype.addEvents = function(events) {
      console.log('Evenvi.addEvents');
      if ($.isArray(events)) {
        var i = 0, len = events.length;
        for (i = 0; i < len; i++) {
          this.addEvent(events[i]);
        }
      } else {
        this.addEvent(events);
      }
    }

    return Evenvi;
  })();

return Evenvi;
});
