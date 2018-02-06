// Info

define(['jquery'], function($) {
  'use strict';

  var Modal = (function() {

    function Modal(selector) {
      this.selector = selector;
      this.modalElement = $(this.selector);
      this.initialized = false;

      this.init();
    }

    // TODO: check if modalElement actually exists
    Modal.prototype.init = function() {
      if (this.initialized === true) {
        return;
      }

      var _modal = this;

      if (!_modal.modalElement.hasClass('modal')) {
        _modal.modalElement.addClass('modal');
      }

      _modal.modalElement.append(' \
          <div class="modal-dialog"> \
            <div class="modal-control"> \
              <span class="close">×</span> \
            </div>                         \
            <div class="modal-content"></div> \
          </div>');

      $(this.selector + ' span.close').click(function() {
        _modal.hide();
      });

      window.onclick = function(event) {
        if (event.target == _modal.modalElement[0]) {
          _modal.modalElement.hide();
        }
      };

      _modal.initialized = true;
    }

    Modal.prototype.show = function() {
      this.modalElement.show();
    }

    Modal.prototype.hide = function() {
      this.modalElement.hide();
    }

    Modal.prototype.append = function(content) {
      var modalContent = $(this.selector + ' div.modal-content');
      modalContent.empty();
      modalContent.append(content);
    }

    return Modal;
  })();

  return Modal;
});
