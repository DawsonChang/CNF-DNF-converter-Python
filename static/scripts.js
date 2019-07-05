var link = $('#hiddenLine')[0];

$('input').on("change keyup paste", function(){
    var elem = $(this);
    if(elem.val()){

      $.getJSON('/input', {formula: elem.val()}, function(data, textStatus, jqXHR) {
        $('#showData').html("<p>DNF: "+ data.dnf + "</p><p>CNF: " + data.cnf + "</p>");
      });
        $('#showData').show()
      
    }
    else{
      $('#showData').hide();
    }
});
