document.addEventListener('DOMContentLoaded', function () {
  var fireButton = document.getElementById('fire');
  if (!fireButton) {
    return;
  }

  fireButton.addEventListener('click', function () {
    if (window.app && window.app.ports && window.app.ports.newMissile) {
      window.app.ports.newMissile.send(true);
    }
  });
});
