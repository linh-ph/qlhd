function AjaxFormSubmit(id_img) {
  showLoading();
  src = $(id_img).attr("src");
  var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
  var fd = new FormData();
  fd.append("url", src);
  fd.append("id_session", 1);
//  fd.append("id_folder", "web");
  fd.append("csrfmiddlewaretoken", csrf_token);
  $.ajax({
    url: "/api/detected-web",
    type: "POST",
    data: fd,
    success: function (response) {
        var delayInMilliseconds = 0; //1 second
        setTimeout(function() {
          //your code to be executed after 1 second
            if (response.error) {
                closeLoading("Thông báo", response.message, response.error);
            } else {
                $(".review").attr("src","/"+response.data['url_result']);
                //Get data
                data = response.data['form_json']
                info = data.info
                //Json Format
                $("#p_json").text(response.format_json);

                // show info
                $("#shopcode").text(info[0].ocr_text);
                $("#date").text(info[1].ocr_text);
                $("#distributor").text(info[2].ocr_text);
                $("#total").text(info[3].ocr_text);
                 table = data.table
                // remove table if before already
                 $("#tbody_bottom > tr").remove();
                 for(i=0;i < table.length;i++)
                 {
                     html=
                     "<tr"+
                        "<td scope='row'>"+"</td>"+
                        "<td style='font-size:12px'>"+String(i+1)+"</td>"+
                        "<td style='font-size:12px' colspan='5'>"+ String(table[i].name) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].unit) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].quantity) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].price) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].total_price) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].tax) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].money_tax) +"</td>"+
                        "<td style='font-size:12px'>"+ String(table[i].total) +"</td>"+
                    "</tr>";
                    //Show Table
                    $('#tbody_bottom').append(html);

                   }


                //showImgReview(response.id_img, response.full_name)
                closeLoading("Thông báo","Message: "+ response.message + "<br/> Timer detected: "+ Number(response.data.timer_final).toFixed(2) + "s", response.error);
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
