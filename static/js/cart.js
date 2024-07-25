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
            console.log('Not logged in')
        }else { // call the function to update user order if the user is logged in
            updateUserOrder(productId, action)
        }
    })
}

// function to update user order
function updateUserOrder(productId, action) {
    console.log('User is logged in. Sending data...')

    //set the url to send the data to
    let url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})// data to be sent to the view
    })
    
    .then((response) => {
        return response.json()
    }) //return promise

    .then((data) => {
        console.log('data:', data); //log the response data that was received back
    })
}