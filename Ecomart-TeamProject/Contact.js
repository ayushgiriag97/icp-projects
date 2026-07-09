
 // Form submission handler
document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Thank you for contacting us! We will get back to you soon.');
            this.reset();
        });