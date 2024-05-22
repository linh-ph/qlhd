$(document).ready(function () {
  console.log("ready! 2");
  // form upload
  // Listerner ID
  $(document).on("click", ".open-AddBookDialog", function () {
    var myBookId = $(this).data("id");
    $("#id_ajax_upload_form #id_img").val(myBookId);
  });

  // Close Modal
  $(document).on("click", ".modal-header .close", function () {
    $("#wait").css("display", "block");
    $("#result").text("");
    $("#id_url").val("");
  });


  // end
});
