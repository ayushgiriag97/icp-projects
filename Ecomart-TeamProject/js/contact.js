// EcoMart — contact form submit handling (contact.html)
(function () {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    // No backend is wired up yet — replace this with a real fetch()
    // call to your form endpoint when one is available.
    form.reset();
    alert('Thanks for reaching out! We will get back to you soon.');
  });
})();