function make_base()
{
  var canvas = document.getElementById("paint"),
  console.log("canvas" + JSON.stringify(canvas));
  context = canvas.getContext("2d");
  var width = canvas.width, height = canvas.height;

  base_image = new Image();
  base_image.src = '{{ documents.last.image.url }}';
  base_image.onload = function(){
    context.drawImage(base_image, 100, 100);
  }
}
