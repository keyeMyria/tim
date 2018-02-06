// Info

define(['jquery', 'jquery-datetimepicker'], function($) {
  'use strict';

  var Toolbar = (function() {

    function Toolbar(config) {
      this.selector = config['selector'];
      this.loadCallback = config['loadCallback'];
      this.liveCallback = config['liveCallback'];

      this.toolbarElement = $(this.selector);
      this.initialized = false;

      this.init();
    }

    // TODO: check if modalElement actually exists
    Toolbar.prototype.init = function() {
      if (this.initialized === true) {
        return;
      }

      var _toolbar = this;

      _toolbar.toolbarElement.append(' \
        <input type="text" id="toolbar-from-time"></input> \
        <input type="text" id="toolbar-to-time"></input> \
        <input type="button" id="toolbar-load" value="Load"> \
        <input type="button" id="toolbar-live" value="Live"> \
      ');

      var options = {
        step: 1,
        format: 'd.m.Y H:i'
      }

      $('#toolbar-from-time').datetimepicker(options);
      $('#toolbar-to-time').datetimepicker(options);

      $('#toolbar-load').click(function() {
	console.log('LOAD');
        var fromDatetime = $('#toolbar-from-time').datetimepicker('getValue');
        var toDatetime = $('#toolbar-to-time').datetimepicker('getValue');

        console.log('toolbar-from-time: ' + fromDatetime);
        console.log('toolbar-to-time: ' + toDatetime);

        if (fromDatetime !== null && toDatetime !== null) {
          _toolbar.loadCallback(fromDatetime.toISOString(), toDatetime.toISOString());
        }
      });

      $('#toolbar-live').click(function() {
        console.log('LIVE');
        $('#toolbar-from-time').datetimepicker('reset');
        $('#toolbar-to-time').datetimepicker('reset');
        _toolbar.liveCallback();
      });
    }    

    return Toolbar;
  })();

  return Toolbar;
});
