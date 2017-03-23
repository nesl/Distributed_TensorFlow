<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Distributed TensorFlow</title>

<style type="text/css">

.bgimg {
  background-color:lightblue;
}
.bgimg label{
display:inline-block;
width:150px;
text-align:right;
}

</style>

</head>
<body>


<div align="center" class="bgimg">

<h1>submit Job to Tensorflow cluster </h1>
<br>
<br>
<h2>Define Job on Multiple Machines </h2>
<br>
<br>
<form method="get" action="http://192.168.2.4:5000/p1" class="form-group"> 
			
 			 <label>(Node 1:)<input type="text" style="width:20px;" id="mac1" name="mac1"/>
             </label>
			 <br>
			 <br>
			 <label>(Node 2:) <input type="text" style="width:20px;" id="mac2" name="mac2"/>
			  </label>
			  <br>
			  <br>
			   <label>
			 (Node 3:)<input type="text" style="width:20px;" id="mac3" name="mac3"/>
			   </label>
			  <br>
			  <br>
			  <label>
			 (Node 4:)<input type="text" style="width:20px;" id="mac4" name="mac4"/>
			  </label>
			  <br>
			  <br>
			  <label>
			 (Node 5:)<input type="text" style="width:20px;" id="mac5" name="mac5"/>
			   </label>
			  <br>
			  <br>
			  <br>
			 <button type="submit" name="button" value="button1" 
			   class="btn btn-primary">Run Job</button>
			 
			 <br>
</form>
</div>
		
</body>
</html>