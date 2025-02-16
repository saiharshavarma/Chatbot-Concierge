var checkout = {};

$(document).ready(function () {
  var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

  $(window).load(function () {
    $messages.mCustomScrollbar();
    insertResponseMessage('Hi there, I\'m your personal Concierge. How can I help?');
  });

  function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
      scrollInertia: 10,
      timeout: 0
    });
  }

  function setDate() {
    d = new Date();
    if (m != d.getMinutes()) {
      m = d.getMinutes();
      $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
  }

  function callChatbotApi(message) {
    // Create the API client and call the chatbot API
    var apigClient = apigClientFactory.newClient();
    return apigClient.chatbotPost({}, {
      messages: [{
        type: 'unstructured',
        unstructured: {
          text: message
        }
      }]
    }, {});
  }

  function insertMessage() {
    var msg = $('.message-input').val();
    if ($.trim(msg) === '') {
      return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();

    callChatbotApi(msg).then((response) => {
      console.log('User message:', msg, 'Response:', response);
      
      // Parse the body if it's stringified
      var responseBody = response.data.body ? JSON.parse(response.data.body) : response.data;

      if (responseBody.messages && responseBody.messages.length > 0) {
        console.log('Received ' + responseBody.messages.length + ' messages from chatbot.');

        var messages = responseBody.messages;
        for (var message of messages) {
          if (message.type === 'unstructured') {
            insertResponseMessage(message.unstructured.text);
          } else {
            console.log('Unsupported message type:', message.type);
          }
        }
      } else {
        insertResponseMessage('Oops, something went wrong. Please try again.');
      }
    }).catch((error) => {
      console.error('An error occurred:', error);
      insertResponseMessage('Oops, something went wrong. Please try again.');
    });
  }

  $('.message-submit').click(function () {
    insertMessage();
  });

  $(window).on('keydown', function (e) {
    if (e.which === 13) {
      insertMessage();
      return false;
    }
  });

  function insertResponseMessage(content) {
    $('<div class="message loading new"><figure class="avatar"><img src="https://media.tenor.com/images/4c347ea7198af12fd0a66790515f958f/tenor.gif" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
      $('.message.loading').remove();
      $('<div class="message new"><figure class="avatar"><img src="https://media.tenor.com/images/4c347ea7198af12fd0a66790515f958f/tenor.gif" /></figure>' + content + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
      i++;
    }, 500);
  }
});