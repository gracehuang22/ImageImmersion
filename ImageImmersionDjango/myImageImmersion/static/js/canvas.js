
function make_base()
{
  var canvas = document.getElementById("paint");
  console.log("canvas");
  context = canvas.getContext("2d");
  var width = canvas.width, height = canvas.height;

  base_image = new Image();
  base_image.src = document.querySelector('img#uploadedPic').src;
  canvas.width = base_image.width + 10;
  canvas.height = base_image.height + 10;
  console.log(base_image.src);
  base_image.onload = function(){
    context.drawImage(base_image, 5, 5);
  }
}

// pencil tool
 var canvas_data = [];
function pencil (){
  var canvas = document.getElementById("paint");
  context = canvas.getContext("2d");
  var curX, curY, hold, prevX, prevY;
  var origX, origY;
  var firstMouseDown = false;
//  var canvas_data = {};
    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;

        prevX = curX;
        prevY = curY;
        if (!firstMouseDown) {
          origX = curX;
          origY = curY;
          firstMouseDown = true;
        }
        context.beginPath();
        context.moveTo(prevX, prevY);
        context.lineWidth = context.lineWidth + 1;
    };

    canvas.onmousemove = function (e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };

    canvas.onmouseup = function (e){
        hold = false;
    };

    canvas.onmouseout = function (e){
        hold = false;
    };

    function draw (){
        context.lineTo(curX, curY);
        context.stroke();

        if (origX == curX && curY == origY) {
          context.closePath();
        //context.fillStyle = '';
          context.fill();
        }
      //console.log("canvas_data: " + JSON.stringify(canvas_data));

        // canvas_data.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY,
        //     "thick": context.lineWidth, "color": context.strokeStyle });
      //  global.canvas_data = canvas_data;
    }


}


function save(token) {
    console.log("SAVED");
    var canvas = document.getElementById("paint");
    var filename = document.getElementById("fname").value;
    canvas_data = canvas.toDataURL();
    console.log("canvas_data: " + canvas_data);
  //  alert(filename + " saved: " + canvas_data);
    var URL = "/edit/"
    var data = {
      csrfmiddlewaretoken: token,
      save_fname: filename,
      save_cdata: canvas_data
    };
    console.log("save_fname: " + filename);
    return $.post(URL, data);

}

// {
//     if(response === 'success'){ alert('Yay!'); }
//     else{ alert('Error! :(' + response); }
// });
