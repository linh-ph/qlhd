$(document).ready(function () {
console.log("ready! upload-img");

  console.log("ready! 2");
  // form upload
  // Listerner ID
  $(document).on("click", ".openModal", function () {
    var myBookId = $(this).data("id");
    $("#id_ajax_upload_form_list #id_edit").val(myBookId);
  });

  // Close Modal
  $(document).on("click", ".modal-header .close", function () {
    $("#wait").css("display", "block");
    $("#result").text("");
    $("#id_url").val("");
  });
  // end


  // form upload
  $("#id_ajax_upload_form").submit(function (e) {
    // denied event button refresh
    e.preventDefault();
    // Model hidden
    $("#myModal").modal("hide");
    showLoading();
    $form = $(this);
    var formData = new FormData(this);
    $.ajax({
      url: "/api/upload-image-list",
      type: "POST",
      data: formData,
      success: function (response) {
        var delayInMilliseconds = 1000; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                closeLoading("Thông báo", response.message, response.error);
                // Update List
                AjaxCallStore(1);
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


  // form upload
  $("#id_ajax_upload_form_list").submit(function (e) {
    // denied event button refresh
    e.preventDefault();
    // Model hidden
    console.log("Upload")
    $("#myModal_list").modal("hide");
    showLoading();
    $form = $(this);
    var formData = new FormData(this);
    $.ajax({
      url: "/api/get-data-store-upload-image-list",
      type: "POST",
      data: formData,
      success: function (response) {
        var delayInMilliseconds = 1000; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                closeLoading("Thông báo", response.message, response.error);
                // Update List
                AjaxCallStore(1);
            }
        }, delayInMilliseconds);

      },
        error: function (xhr, error, response) {
            closeLoading("Thông báo","Có lỗi xảy ra khi upload ảnh", True);
      },
      cache: false,
      contentType: false,
      processData: false,
    });
  });


});


