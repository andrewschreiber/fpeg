$(document).ready(function () {

  $("#upload-button").click(function(e) {
  
    // get image data from form
    var form_data = new FormData($('form')[0]);
    
    // send async ajax request
    $.ajax({
      url: "/compress",
      type: "POST",
      data: form_data,
      cache: false,
      contentType: false,
      processData: false,
      
      complete: function(xhr, status) {
        console.log("request status: " + status);
      }
      
    });
    
  });

});
