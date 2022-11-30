<?php
debug_to_console("test");
$json = file_get_contents('php://input');
file_put_contents('results.txt', $json, FILE_APPEND);

function debug_to_console($data) {
   $output = $data;
   if (is_array($output))
	   $output = implode(',', $output);

   echo "<script>console.log('Debug Objects: " . $output . "' );</script>";
}

?>