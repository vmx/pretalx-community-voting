'use strict'

$(() => {
  const csrftoken = getCookie("pretalx_csrftoken")

  // Get the user from the URL. The user needs to be the last element of the
  // URL. Trailing slashes are ignored
  let user
  for (user of window.location.pathname.split('/').reverse()) {
    // Ignore trailing slashes
    if (user !== '') {
      break
    }
  }

  $('body').on('click', 'label', (event) => {
    // Don't select the radio button by just clicking it. Wait for the GET
    // request to return before the radiobox is selected, to make sure the
    // server processed vote correctly.
    event.preventDefault()

    const label = $(event.currentTarget);
    const radio = label.children().first()

    // If it was already selected, don't do anything
    if (radio.prop('checked')) {
      return
    }

    label.addClass('loading')

    // Reset errors
    label.siblings().addBack().removeClass('error')

    // Get values for Ajax request
    const submission = radio.attr('name')
    const score = radio.val()

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
      headers: {
        'X-CSRFToken': csrftoken
      }
    }).done((json) => {
      // Select the checkbox based on the POST response
      $(`input[name=${json.submission}]`)
        .filter(`[value=${json.score}]`)
        .prop('checked', true)
      label.addClass('selected')
      label.removeClass('loading')
      // Vote was successfully registered, hence unselect the previously
      // selected one
      label.siblings().removeClass('selected')
    }).fail((xhr, status, error) => {
      label.addClass('error')
      label.removeClass('loading')
      console.log('error on vote request:', error)
    })
  })
})

// From https://docs.djangoproject.com/en/3.0/ref/csrf/
const getCookie = (name) => {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (const i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue;
}
