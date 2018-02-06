// Info

define(['jquery'], function($) {
  'use strict';

  var AjaxFeed = (function() {

    function AjaxFeed(config) {
      this.config = config;
      this.feedUrl = this.config['feedUrl'];
      this.pollInterval = this.config['pollInterval'];; // milliseconds
      this.polling = false;
      this.doneCallback = this.config['doneCallback'];
      this.failCallback = this.config['failCallback'];
      this.timeoutId = null;
    }

    AjaxFeed.prototype.fetchUrl = function(url, data, dCallback, fCallback) {
      var _this = this;
      var request = $.ajax({
        dataType: 'json',
        url: url,
        data: data,
      });
      request.done(function(data, textStatus, jqXHR) {
        console.log('AjaxFeed.fetch [DONE] textStatus = ' + textStatus);
        if (dCallback !== null && typeof dCallback === "function") {
          dCallback();
        }
        _this.doneCallback(data, textStatus, jqXHR);
      });
      request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('AjaxFeed.fetch [FAIL] textStatus = ' + textStatus);
        if (fCallback !== null && typeof fCallback === "function") {
          fCallback();
        }
        _this.failCallback(jqXHR, textStatus, errorThrown);
      });
    }

    AjaxFeed.prototype.fetch = function(data, dCallback, fCallback) {
      this.fetchUrl(this.feedUrl, data, dCallback, fCallback);
    }

    AjaxFeed.prototype.load = function(from, to) {
      console.log('AjaxFeed.load');
      this.stop();
      var params = {
        from: encodeURIComponent(from),
        to: encodeURIComponent(to)
      };
      this.fetch(params, null, null);
    }

    AjaxFeed.prototype.start = function() {
      console.log('AjaxFeed.start');
      if (this.polling === true) {
        return;
      }
      this.polling = true;
      this.poll(500);
    }

    AjaxFeed.prototype.stop = function() {
      console.log('AjaxFeed.stop');
      if (this.polling === false) {
        return;
      }
      if (this.timeoutId !== null) {
        clearTimeout(this.timeoutId);
      }
      this.polling = false;
    }

    AjaxFeed.prototype.isPolling = function() {
      console.log('AjaxFeed.stop');
      return (this.polling === true);
    }

    AjaxFeed.prototype.poll = function(interval) {
      console.log('AjaxFeed.poll interval: ' + interval);
      var _this = this;

      if (_this.polling === false) {
        return;
      }

      _this.timeoutId = setTimeout(function() {
        var params = {
          seconds_ago: encodeURIComponent(_this.pollInterval / 1000)
        };

        console.log("AjaxFeed.poll from: " + params['seconds_ago']);

        _this.fetch(
            params,
            function() {
              console.log('AjaxFeed.poll doneCallback');
              _this.poll(_this.pollInterval);
            },
            function() {
              console.log('AjaxFeed.poll failCallback');
              _this.polling = false;
            }
        );
      }, interval);
    }

    return AjaxFeed;
  })();

  return AjaxFeed;
});
