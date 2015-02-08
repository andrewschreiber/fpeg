<!DOCTYPE html>
<html>
  <head>
    <title>FPEG Demo</title>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script src="/static/main.js"></script>
  </head>
  
  <body>
    <form action="/compress" method="post" enctype="multipart/form-data">
      Select a file: <input type="file" name="upload" />
      <input type="submit" value="Show Compressed FPEG!" />
    </form>
  </body>
</html>
