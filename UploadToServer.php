<?php
   $file_path = "files/";
   $file_path = $file_path . basename( $_FILES['uploaded_file']['name']);
   move_uploaded_file($_FILES['uploaded_file']['tmp_name'], $file_path);
?>