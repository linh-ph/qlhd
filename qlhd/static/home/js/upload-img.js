$(document).ready(function () {
  console.log("ready! upload-img");

  // form upload
  $("#id_ajax_upload_form").submit(function (e) {
    e.preventDefault();
    $("#myModal").modal("hide");
    showLoading();
    $form = $(this);
    var formData = new FormData(this);
    $.ajax({
      url: "/api/upload-image",
      type: "POST",
      data: formData,
      success: function (response) {
        var delayInMilliseconds = 2000; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                showImgReview(response.id_img, response.full_name)
                closeLoading("Thông báo", response.message, response.error);
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
  });
  // end
});


