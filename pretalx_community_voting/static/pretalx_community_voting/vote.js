'use strict'

$(() => {
  // Get the user from the URL. The user needs to be the last element of the
  // URL. Trailing slashes are ignored
  let user
  for (user of window.location.pathname.split('/').reverse()) {
    // Ignore trailing slashes
    if (user !== '') {
      break
    }
  }

  $('body').on('click', 'input[type=radio]', (event) => {
    const button = $(event.currentTarget);
    const submission = button.attr('name')
    const score = button.val()

    // Don't select the radio button by just clicking it. Wait for the GET
    // request to return before the radiobox is selected, to make sure the
    // server processed vote correctly.
    event.preventDefault()

    $.ajax({
      // TODO vmx 2020-02-23: Get the URL from Django somehow to make sure it
      // works even if the URLS are changed
      url: '../../api/',
      data: {
        submission,
        score,
        user
      },
      type: 'POST',
      dataType: 'json',
    }).done((json) => {
      // Select the checkbox based on the POST response
      $(`input[name=${json.submission}]`)
        .filter(`[value=${json.score}]`)
        .prop('checked', true)
    }).fail((xhr, status, error) => {
      console.log('error on vote request:', error)
    })
  })
})
