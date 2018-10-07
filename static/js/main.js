var input = $('#upload');

input.change(function (){
   var filePath = $(this).val();
   var fileNameArray = filePath.split('\\');
   var fileName = fileNameArray[fileNameArray.length - 1];
   $("#filename").text(fileName).show();
});