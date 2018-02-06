requirejs.config({
  'baseUrl': '/static/evenvi/js',
  'paths': {
    'jquery': 'vendor/jquery-3.0.0.min',
    'jquery-jvectormap': 'vendor/jquery-jvectormap-2.0.3.min',
    'jquery-jvectormap-world-mill': 'vendor/jquery-jvectormap-world-mill',
    'jquery-datetimepicker': 'vendor/jquery.datetimepicker.full.min',
    'jquery-mousewheel': 'vendor/jquery.mousewheel.min',
  },
  'shim': {
    'jquery-jvectormap': {
      'deps': ['jquery']
    },
    'jquery-jvectormap-world-mill': {
      'deps': ['jquery-jvectormap']
    },
    'jquery-datetimepicker': {
      'deps': ['jquery']
    }
  }
});

require(['jquery', 'lib/evenvi'], function ($, Evenvi) {
  var evenvi = new Evenvi();
  evenvi.start();

  // XXX: for testing
  //window.evenvi = evenvi;
});
