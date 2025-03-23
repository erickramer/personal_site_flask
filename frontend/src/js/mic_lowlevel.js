$('document').ready(function(){
  window.SpeechRecognition =
    window.webkitSpeechRecognition || window.SpeechRecognition;

  //$('#record').on('click', () => {
    var recognition = new window.SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {

      var transcripts = build_transcripts(event.results)
      console.log(transcripts);
      app2.ports.newTranscript.send(transcripts);
    }

    recognition.onend = (event) =>{
      console.log("resetting")
      recognition.start()
    }

    recognition.start()
  //});

})

function build_transcripts(results){

  var re = RegExp("fire")
  var transcripts = []
  var now = (new Date).getTime()
  for(var i = 0; i < results.length; i++){
    var f = re.test(results[i][0].transcript)
    var transcript = {text: results[i][0].transcript, time: now, y: 0, op: 1.0, fire: f}
    transcripts.push(transcript)
  }
  return(transcripts)
}
