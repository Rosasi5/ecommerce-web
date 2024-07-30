// update buttons

let updateBtns = document.getElementsByClassName('update-cart');

//loop through the buttons
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let productId = this.dataset.product // this. refers to the current button that is clicked
        let action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        console.log('USER:', user)

        if (user === 'AnonymousUser') {
            console.log('Not logged in...')
            
        }else { // call the function to update user order if the user is logged in
            updateUserOrder(productId, action)
        }
    })
}

// function to update user order
function updateUserOrder(productId, action) {
    console.log('User is logged in. Sending data...')

    //set the url to send POST the data to
    let url = '/update_item/';
    var csrftoken = getToken('csrftoken');
    console.log('CSRF Token:', csrftoken);

    fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })// data to be sent to the view in the backend as a string
    })

    .then((response) => {
        if (!response.ok) {  // Check if the response is not okay
            throw new Error('Network response was not ok...');
        }
        return response.json()
    }) //return promise

    .then((data) => {
        console.log('data:', data); //log the response data that was received back
        location.reload() //makes sure we see the new data immedeately after its added when the page reloads automatically
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


// Function to get the CSRF token from the cookie
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // does this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



