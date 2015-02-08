<!DOCTYPE html>
<html>
  <head>
    <title>Sender App</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon"> 
    <link type="text/css" rel="stylesheet" href="/static/style.css">
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	<!-- Optional theme -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">
  </head>
  <body>
 	
	    
	    <h1>Fibonacci Calculator</h1>
	    
	    <br/>
	   
	    <div class="container">
	    <form class="form-inline" role="form">
		  <div class="form-group">
		    <div class="input-group">
		      <label class="sr-only" for="gen_fib">Sequence Number</label>
		      <input type="text" class="form-control" id="gen_fib" name="number" placeholder="Enter sequence number here">
		    </div>
		  </div>
		  <button type="button" id="submit_button" class="btn btn-default">Generate</button>
		</form>
		<div class="radio">
		  <label>
		    <input type="radio" name="typeRadio" id="optionsRadios1" value="fib" checked>
		    Calculate and display
		  </label>
		</div>
		<div class="radio">
		  <label>
		    <input type="radio" name="typeRadio" id="optionsRadios2" value="send">
		    Calculate, send, then display
		  </label>
		</div>
		<div id="result">
		</div>
		</div>

	
	
	 
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
    <!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="/static/main.js"></script>
        	
   <body>
</html>
