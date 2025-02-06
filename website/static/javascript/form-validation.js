window.addEventListener('load', function() {
    var allInputs = document.getElementsByTagName('input');
    var allTextareas = document.getElementsByTagName('textarea');
    var allElements = [...allInputs, ...allTextareas];
    for (var i = 0; i < allElements.length; i++) {
        var element = allElements[i];
        if (element.type !== 'submit') {
            element.addEventListener('input', function() {
                if (this.validity.valid) {
                    this.classList.remove('form-invalid');
                    this.classList.add('form-valid');
                } else {
                    this.classList.remove('form-valid');
                    this.classList.add('form-invalid');
                }
            });
        }
    }
});