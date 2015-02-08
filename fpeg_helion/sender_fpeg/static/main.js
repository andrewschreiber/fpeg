// main.js


        
$(document).ready(function() {
	$('#submit_button').click(function(e) {
		if($("#optionsRadios1").prop("checked")){
			var url = "/fib";
		}
		else{
			var url = "/send";
		}
		$.ajax({
		  type: "POST",
		  url: url,
		  data: JSON.stringify({"number": $("#gen_fib").val()}),
		  contentType: "application/json",
          dataType: "json",
		  success: function(data){
		  	console.log(data);
		  	$("#result").html("<span>The number you sent was: "+$("#gen_fib").val()+ ". The returned value was: "+data.sequence_value+"</span>");
		  }
		});

		
	});
	
});



