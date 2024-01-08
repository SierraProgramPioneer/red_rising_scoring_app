document.addEventListener('DOMContentLoaded', function(){

    // Add Card Function
    function add_card(event){
        event.preventDefault()
        let card = {
            user_name: event.target.dataset.user_name,
            game_number: event.target.dataset.game_number,
            character: event.target.value
        }
        let jsonString = JSON.stringify(card);
        fetch('/add_cards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonString
        });
    }

    //Apply Event Listener to Each Character Button
    let character = document.querySelectorAll('.character');
    for (let i = 0; i < character.length; i++) {
        character[i].addEventListener('click', add_card);
    }
    });
