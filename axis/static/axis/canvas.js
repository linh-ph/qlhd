var canvasUpper = document.getElementById("myCanvasUpper");
var canvasLower = document.getElementById("myCanvasLower");
var canvasShortest = document.getElementById("myCanvasShortest");

var width_resize = 500;
var height_resize = 0;
// Get Context
var ctxU = canvasUpper.getContext("2d"); //ruler
var ctxL = canvasLower.getContext("2d"); //image and rect
var ctxS = canvasShortest.getContext("2d"); //image and rect

// Variables global
var startX = 0;
var startY = 0;
var endX = 0;
var endY = 0;
var width = 0;
var height = 0;
var url_src = "";

canvasUpper.onmousedown = function (e) {
  rect = canvasUpper.getBoundingClientRect();
  x = e.clientX - rect.left;
  y = e.clientY - rect.top;
  startX = x;
  startY = y;
  console.log("onMouseDown", x, y);
};

canvasUpper.onmouseup = function (e) {
  rect = canvasUpper.getBoundingClientRect();
  x = e.clientX - rect.left;
  y = e.clientY - rect.top;
  endX = x;
  endY = y;
  width = x - startX;
  height = y - startY;
  ctxL.beginPath();
  ctxL.lineWidth = "1";
  ctxL.strokeStyle = "red";
  ctxL.rect(startX, startY, width, height);
  ctxL.stroke();
  console.log("onMouseUp", x, y);

  if (width > 0 && height > 0) {
    data = [];
    coordinates = {};
    coordinates["x"] = Math.ceil(startX);
    coordinates["y"] = Math.ceil(startY);
    coordinates["w"] = Math.ceil(width);
    coordinates["h"] = Math.ceil(height);
    data.push(coordinates);

    obj = {
      data: data,
      img_info: {
        url: url_src,
        canvas: { width: width_resize, height: height_resize },
      },
    };
    AjaxCallAxis(obj);
  }

};

canvasUpper.onmouseout = function (e) {
  cStartX = startX - 1;
  cStartY = startY - 1;
  cWidth = width + 2;
  cHeight = height + 2;

  ctxL.clearRect(cStartX, cStartY, cWidth, 2);
  ctxL.clearRect(cStartX, cStartY, 2, cHeight);
  ctxL.clearRect(cStartX, cStartY + height, cWidth, 2);
  ctxL.clearRect(cStartX + width, cStartY, 2, cHeight);

  console.log("onMouseOut Clear");
};

canvasUpper.onmousemove = function (e) {
  ctxU.clearRect(0, 0, canvasUpper.width, canvasUpper.height);
  rect = canvasUpper.getBoundingClientRect();
  x = e.clientX - rect.left;
  y = e.clientY - rect.top;
  ctxU.beginPath();
  ctxU.lineWidth = "0.5";
  ctxU.moveTo(x, 0);
  ctxU.lineTo(x, canvasUpper.height);
  ctxU.moveTo(0, y);
  ctxU.lineTo(canvasUpper.width, y);
  ctxU.stroke();
};

function AjaxCallDetailStore(id) {
  obj = {
    id: id,
  };

  console.log(obj);

  $.ajax({
    url: "/api/get-data-store-detail",
    type: "POST",
    data: JSON.stringify(obj),
    success: function (response) {
      var delayInMilliseconds = 0; //1 second
      setTimeout(function () {
        //your code to be executed after 1 second
        if (response.error) {
          closeLoading("Thông báo", response.message, response.error);
        } else {
          img = new Image();
          img.src = response.data["url"];
          url_src = response.data["url"];
          $("#request").attr("src", url_src);

          // Set canvas width height
          canvasUpper.width = img.naturalWidth;
          canvasUpper.height = img.naturalHeight;

          canvasLower.width = img.naturalWidth;
          canvasLower.height = img.naturalHeight;

          canvasShortest.width = img.naturalWidth;
          canvasShortest.height = img.naturalHeight;

          img.onload = function () {
            console.log("Loading Image");

            ctxS.drawImage(
              img,
              0,
              0,
              canvasShortest.width,
              canvasShortest.height
            );
          };

        }
      }, delayInMilliseconds);
    },
    error: function (xhr, error, response) {
      res = JSON.parse(xhr.responseText);
      closeLoading("Thông báo", res.message, res.error);
    },
    cache: false,
    contentType: false,
    processData: false,
  });
}
