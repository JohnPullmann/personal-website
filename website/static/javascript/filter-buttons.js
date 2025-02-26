// Select all buttons that are descendants of an element with the class 'filters-javascript'
var buttons = document.querySelectorAll('.filters-javascript .button-red-outline');

// Function to update the URL query
function updateQuery(value) {
    if (history.pushState) {
        var url = new URL(window.location.href);
        var params = new URLSearchParams(url.search);
        if (value) {
            params.set('button', value);
        } else {
            params.delete('button');
        }
        url.search = params.toString();
        window.history.pushState({path:url.toString()},'',url.toString());
    }
}

// Add click event listener to each button
buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        // Check if the clicked button was previously chosen
        var wasChosen = this.classList.contains('chosen');

        // Remove 'chosen' class from all buttons and update the URL query
        buttons.forEach(function(btn) {
            if (btn.classList.contains('chosen')) {
                btn.classList.remove('chosen');
                updateQuery('');
            }
        });

        // If the clicked button was not the one previously chosen, add 'chosen' class to it and update the URL query
        if (!wasChosen) {
            this.classList.add('chosen');
            updateQuery(this.textContent);
        }
    });
});

function submitWithButton() {
    var form = document.querySelector('form');
    var button = document.querySelector('.button-red-outline.chosen');
    if (button) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'button';
        input.value = button.textContent;
        form.appendChild(input);
    }

    // Get the timespan value from the URL
    var urlParams = new URLSearchParams(window.location.search);
    var timespan = urlParams.get('timespan');

    // Add the timespan value as a hidden input field
    if (timespan) {
        var timespanInput = document.createElement('input');
        timespanInput.type = 'hidden';
        timespanInput.name = 'timespan';
        timespanInput.value = timespan;
        form.appendChild(timespanInput);
    }
    
    form.submit();
}


// Function to run when the page loads
window.onload = function() {
    // Add event listener to buttons that are descendants of an element with the class 'filters-javascript'
    var buttons = document.querySelectorAll('.filters-javascript .button-red-outline');
    buttons.forEach(function(button) {
        button.addEventListener('click', submitWithButton);
    });

    // Get the 'button' parameter from the URL query
    var url = new URL(window.location.href);
    var buttonValue = url.searchParams.get('button');

    // If the 'button' parameter exists, add the 'chosen' class to the matching button
    if (buttonValue) {
        var buttons = document.querySelectorAll('.filters-javascript .button-red-outline');
        buttons.forEach(function(button) {
            if (button.textContent === buttonValue) {
                button.classList.add('chosen');
            }
        });
    }
};