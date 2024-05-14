function AjaxCallAxis(obj) {
  showLoading();
  $.ajax({
    url: "/api/detected-create-mask",
    type: "POST",
    data: JSON.stringify(obj),
    success: function (response) {
      var delayInMilliseconds = 0; //1 second
      setTimeout(function () {
        //your code to be executed after 1 second
        if (response.error) {
          closeLoading("Thông báo", response.message, response.error);
        } else {
          console.log(response);

          text_raw = response.data["export"][0]["text"];

          Swal.fire({
            title: "Hãy đặt tên nhãn dán",
            html:
              "<input id='swal-label' class='swal2-input' value='" +
              "" +
              "' placeholder='Nhập nhãn dán...' required>" +
              "<input id='swal-text' class='swal2-input'  value='" +
              text_raw +
              "' placeholder='Nhập văn bản...' required>",
            showCancelButton: true,
            cancelButtonText: "Bỏ",
            confirmButtonText: "Lưu",
            showLoaderOnConfirm: true,
            onOpen: () => $('#swal-label').focus(),
            preConfirm: () => {


              label = $("#swal-label").val();
              text = $("#swal-text").val();

              console.log(label.length)
              console.log(text.length)

          if (pattern.test(label) && patternVie.test(label)) {
               closeLoading("Thông báo", "Tên label không được chứa ký tự đặt biệt", true);
          }else{
           if (label.trim().length == 0 && label.trim().length > 255){
               Swal.showValidationMessage('Không được bỏ trống.')
           }else{
              if (label.trim().length == 0 || text.trim().length == 0){
                Swal.showValidationMessage('Không được bỏ trống.')
              }else{
                  console.log("request_id");
                  console.log(request_id);
                  data = {
                    id: request_id,
                    data: {
                      label: label.trim(),
                      text: text.trim(),
                    },
                  };
                  save_data_confirm(data);
                  console.log(label, text);
              }
            }
          }





              return 0;
            },
            allowOutsideClick: () => !Swal.isLoading(),
          }).then((result) => {
            console.log(result);
          });
        }
      }, delayInMilliseconds);
    },
    error: function (xhr, error, response) {
      closeLoading("Thông báo", "Không có dữ liệu", true);
    },
    cache: false,
    contentType: false,
    processData: false,
  });
}

function save_data_confirm(data) {
  fetch("/api/detected-ocr-save-mask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {



      obj = {
        id: request_id,
        order_by: "desc",
      };
      AjaxCallListTable(obj);
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function AjaxCallListTable(data) {
  fetch("/api/detected-ocr-list-mask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        closeLoading("Thông báo", data.message, data.error);
      } else {
        createTableAxis(data);
      }

      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}



function showModalEditByID(id,label,text){
    console.log(id,label,text);
    Swal.fire({
        title: "Hãy thay đổi giá trị",
        html:
          "<input id='swal-label' class='swal2-input' value='" +
          label +
          "' placeholder='Nhập nhãn dán...' required>" +
          "<input id='swal-text' class='swal2-input'  value='" +
          text +
          "' placeholder='Nhập văn bản...' required>",
        showCancelButton: true,
        cancelButtonText: "Bỏ",
        confirmButtonText: "Lưu",
        showLoaderOnConfirm: true,
        preConfirm: () => {
          label = $("#swal-label").val().trim();
          text = $("#swal-text").val().trim();
          console.log(label)
          console.log(label.trim().length)

          if (pattern.test(label) && patternVie.test(label)) {
               closeLoading("Thông báo", "Tên tập tin không được chứa ký tự đặt biệt", true);
          }else{
           if (label.trim().length == 0 || label.trim().length > 255){
              Swal.showValidationMessage('Không được bỏ trống.')
           }else{
              if(text.trim().length == 0){
                Swal.showValidationMessage('Không được bỏ trống.')
              }else{
                 data = {
                id: id,
                data: {
                  label: label.trim(),
                  text: text.trim(),
                },
              };
              edit_data_confirm(data);
              }

           }
          }


          return 0;
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        console.log(result);
      });

}


function showModalDeleteByID(id,label){
    Swal.fire({
        title: "Bạn có muốn xóa",
        html:
         "<p id='swal-name' class='swal2-text' >"+"label: "+
            label +
            "</p>",
        showCancelButton: true,
        cancelButtonText: "Bỏ",
        confirmButtonText: "Xóa",
        showLoaderOnConfirm: true,
        preConfirm: () => {
          data = {
            id: id,
          };
          delete_data_confirm(data);
          return 0;
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        console.log(result);
      });

}



function createTableAxis(response) {
  console.log(response);
  table = response.data["image"];
  //remove table if before already
  $("#tbody_bottom > tr").remove();
  for (i = 0; i < table.length; i++) {
    html =
      "<tr" +
      "<td scope='row'>" +
      "</td>" +
      "<td style='font-size:12px'>" +
      "<label id='label'>" +
      String(table[i].label) +
      "</label>" +
      "</td>" +
      "<td style='font-size:12px'>" +
      String(table[i].text) +
      "</td>" +
      "<td style='font-size:12px'>" +
      "<div class='row'>"+
      "<div>"+
      "<i class='fas fa-edit' onClick='showModalEditByID("+table[i].id+", \""+table[i].label+"\" , \""+table[i].text+"\")'></i>" +
      "</div>"+
      "<div style='margin-left:10px'> </div>"+
      "<div>"+
      "<i class='fa fa-trash' onClick='showModalDeleteByID("+table[i].id+", \""+table[i].label+"\")'></i>" +
      "</div>"+
      "</div>"+
      "</td>" +
      "<td style='font-size:12px'>" +
      "</td>" +
      "</tr>";
    //Show Table
    $("#tbody_bottom").append(html);
  }
  $("#p_json").text(response.format_json);


}



function delete_data_confirm(data) {
  fetch("/api/detected-ocr-delete-mask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      obj = {
        id: request_id,
        order_by: "desc",
      };
      AjaxCallListTable(obj);
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}


function edit_data_confirm(data) {
  fetch("/api/detected-ocr-update-mask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      obj = {
        id: request_id,
        order_by: "desc",
      };
      AjaxCallListTable(obj);
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

