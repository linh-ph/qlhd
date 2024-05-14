
function AjaxCallStore(page) {
  key = $('#search-input').val();
  console.log(key)
  obj = {
    "limit": 5,
    "page": page,
    "order_by":"desc",
    "user_id":user_id,
    "search": key
   };

  $.ajax({
    url: "/api/get-data-store-pagination",
    type: "POST",
    data: JSON.stringify(obj),
    success: function (response) {
        var delayInMilliseconds = 0; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                     console.log(response);
                     active = response.data['active']
                     records = response.data['records']
                     table = response.data['store']


                      // remove table if before already
                       $("#tbody_bottom > tr").remove();
                       for(i=0;i < table.length;i++)
                       {
                           html=
                           "<tr"+
                              "<td scope='row'>"+"</td>"+
                              "<td style='font-size:12px'>"+ String(table[i].id) +"</td>"
                              +
                              "<td style='font-size:12px'>"
                              +
                               "<a href='/axis/detail/"+table[i].id+"'> <img src='"+table[i].url+"' alt='picture' width='100' height='100'></a>"
                              +
                              "</td>"
                              +
                              "<td style='font-size:12px'>"+ String(table[i].name) +"</td>"+
                              "<td style='font-size:12px'>"+"</td>"+
                              //"<td style='font-size:12px'>"+ String(table[i].upload) +"</td>"+
                              "<td style='font-size:12px'>"+ "" +"</td>"+
                              "</td>" +
                              "<td style='font-size:12px'>"+ "" +"</td>"+
                              "<td style='font-size:12px' class='row'>" +
                              "<div style='margin-left:10px'/>"+
                              "<i data-id='"+table[i].id+"' data-toggle='modal' data-target='#myModal_list' class='fas fa-arrow-circle-up openModal'></i>" +
                              "<div style='margin-left:10px'/>"+
                              "<i class='fas fa-edit' onClick='showModalEdit("+table[i].id+","+"\""+table[i].name+"\""+")'></i>" +
                              "<div style='margin-left:10px'/>"+
                              "<i class='fa fa-trash' onClick='showModalDelete("+table[i].id+")'></i>" +
                              "</td>" +
                              "<td style='font-size:12px'>"+ "" +"</td>"+

                          "</tr>";
                          //Show Table
                          $('#tbody_bottom').append(html);

                         }

                      $("#pagination > li").remove();

                      for(i=0;i < records.length;i++)
                       {
                           a = active[i] ? "active" : "";
                           html=
                          "<li class='page-item "+ a +"'><button class='page-link' onClick='AjaxCallStore("+records[i]+")'>"+records[i]+"</button></li>";
                          //Show Table
                           $('#pagination').append(html);

                         }
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

function showModalEdit(id, name){
    s_name = name.split('.')[0]
    s_extension = name.split('.').pop()

    Swal.fire({
    title: "Hãy đặt tên mới",
    html:
      "<input id='swal-name' class='swal2-input' value='" +
      s_name +
      "' placeholder='Nhập nhãn dán...' required>",
    showCancelButton: true,
    cancelButtonText: "Bỏ",
    confirmButtonText: "Lưu",
    showLoaderOnConfirm: true,
    onOpen: () => $('#swal-name').focus(),
    preConfirm: () => {
      label = $("#swal-name").val();

      if (pattern.test(label) && patternVie.test(label)) {
           closeLoading("Thông báo", "Tên tập tin không được chứa ký tự đặt biệt", true);
      }else{
       if (label.length == 0 || label.length > 255){
          Swal.showValidationMessage('Không được bỏ trống.')
       }else{
          obj = {
            "name": label+"."+s_extension,
            "id":id
           }
          editTableByID(obj);
       }
      }
      return 0;
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    console.log(result);
  });

}


function showModalDelete(id){
    Swal.fire({
    title: "Xác nhận xóa",
    html:
      "<p id='swal-name' class='swal2-text' >"+"ID : "+
      id +
      "</p>",
    showCancelButton: true,
    cancelButtonText: "Bỏ",
    confirmButtonText: "Cứ làm đi",
    showLoaderOnConfirm: true,
    preConfirm: () => {
      obj = {
        "id":id
       }
      deleteRowByID(obj);
      return 0;
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    console.log(result);
  });

}



function editTableByID(data){
  showLoading();

  $.ajax({
    url: "/api/get-data-store-update",
    type: "POST",
    data: JSON.stringify(data),
    success: function (response) {
        var delayInMilliseconds = 0; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                     console.log(response);
                     AjaxCallStore(1)
                     closeLoading("Thông báo","Message: "+ response.message, response.error);
                   }
        }, delayInMilliseconds);
    },
    error: function (xhr, error, response) {
            closeLoading("Thông báo", "Không thể update",true);
    },
    cache: false,
    contentType: false,
    processData: false,

  });

}

function deleteRowByID(data){
  showLoading();


  $.ajax({
    url: "/api/get-data-store-delete",
    type: "POST",
    data: JSON.stringify(data),
    success: function (response) {
        var delayInMilliseconds = 0; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                     console.log(response);
                     AjaxCallStore(1)
                     closeLoading("Thông báo","Message: "+ response.message, response.error);
                   }
        }, delayInMilliseconds);
    },
    error: function (xhr, error, response) {
            closeLoading("Thông báo", "Không thể update",true);
    },
    cache: false,
    contentType: false,
    processData: false,

  });

}
