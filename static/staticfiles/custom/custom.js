'use strict';

(function () {
    // Init custom option check
    window.Helpers.initCustomOptionCheck();

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const bsValidationForms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.prototype.slice.call(bsValidationForms).forEach(function (form) {
        form.addEventListener(
            'submit',
            function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    // Submit your form
                    alert('Submitted!!!');
                }

                form.classList.add('was-validated');
            },
            false
        );
    });
})();