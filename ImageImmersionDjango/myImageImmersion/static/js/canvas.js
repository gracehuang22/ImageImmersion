
function make_base()
{
  var canvas = document.getElementById("paint");
  var maskCanvas = document.getElementById("mask");
  console.log("canvas");
  context = canvas.getContext("2d");

  var width = canvas.width, height = canvas.height;

  base_image = new Image();
  base_image.src = document.querySelector('img#uploadedPic').src;
  canvas.width = base_image.width;
  canvas.height = base_image.height;

  maskCanvas.width = base_image.width;
  maskCanvas.height = base_image.height;

  base_image.onload = function(){
    context.drawImage(base_image, 0, 0);
  }
}

// pencil tool
 var canvas_data = [];
 var mask_data = [];
function pencil (){
  var canvas = document.getElementById("paint");
  context = canvas.getContext("2d");
  var maskCanvas = document.getElementById("mask");
  maskContext = maskCanvas.getContext("2d");

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
        maskContext.beginPath();
        maskContext.moveTo(prevX, prevY);
        maskContext.lineWidth = context.lineWidth + 1;
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
        maskContext.lineTo(curX, curY);
        maskContext.stroke();
        if (origX == curX && curY == origY) {
          context.closePath();
          maskContext.closePath();
          context.fill();
          maskContext.fill();
        }
    }


}


function save(token) {

    console.log("SAVED");
  //  var canvas = document.getElementById("paint");
    var canvas = document.getElementById("mask");
    var filename = document.getElementById("fname").value;
    maskContext = canvas.getContext("2d");
    base_image = document.querySelector('img#uploadedPic').src;
    console.log("base image: " + base_image);
    // set to draw behind current content
    maskContext.globalCompositeOperation = "destination-over";
    // set background color
    maskContext.fillStyle = '#fff'; // <- background color
    // draw background / rect on entire canvas
    maskContext.fillRect(0, 0, canvas.width, canvas.height);

    canvas_data = canvas.toDataURL();

    console.log("canvas_data: " + canvas_data);
  //  alert(filename + " saved: " + canvas_data);
    var URL = "/edit/"
    var data = {
      csrfmiddlewaretoken: token,
      save_fname: filename,
      save_cdata: canvas_data,
      orig_image: base_image
    };
    console.log("save_fname: " + filename);
    return $.post(URL, data);

}


function saveFinal(token) {

    console.log("SAVED");
   // var canvas = document.getElementById("paint");
    // var canvas = document.getElementById("mask");
    var filename = document.getElementById("fname").value;
    // maskContext = canvas.getContext("2d");
    base_image = document.querySelector('img#uploadedPic').src;
    // console.log("base image: " + base_image);
    // set to draw behind current content
    // maskContext.globalCompositeOperation = "destination-over";
    // set background color
    // maskContext.fillStyle = '#fff'; // <- background color
    // draw background / rect on entire canvas
    // maskContext.fillRect(0, 0, canvas.width, canvas.height);

    canvas_data = canvas.toDataURL();

    console.log("canvas_data: " + canvas_data);
  //  alert(filename + " saved: " + canvas_data);
    var URL = "/display/"
    var data = {
      csrfmiddlewaretoken: token,
      save_fname: filename,
      orig_image: base_image
    };
    console.log("save_fname: " + filename);
    return $.post(URL, data);

}

// {
//     if(response === 'success'){ alert('Yay!'); }
//     else{ alert('Error! :(' + response); }
// });
