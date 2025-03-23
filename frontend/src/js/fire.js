$('document').ready(function(){
  $('#fire').on('click', function(){
    app.ports.newMissile.send(true);
  })
})
