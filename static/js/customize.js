/**
 * Created by munis on 4/8/17.
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function change_img(image_path) {
        if (image_path.files && image_path.files[0]) { // if have input file
                var reader = new FileReader(); // read file

                reader.onload = function (e) {
                    $('.change_src_img').attr('src', e.target.result); // Append file to obj src
                };

                reader.readAsDataURL(image_path.files[0]);
            }
            var form = new FormData();
            var file = image_path.files[0]; // Get user profile image avatar
            console.log(image_path.getAttribute("name"));
            form.append(image_path.getAttribute("name"),file); // Append image file
            $.ajax({
                  url: "/panda-sistem/change/image/",
                  type: "POST",
                  processData: false,
                  contentType: false,
                  data: form,
                  success: function(data) {
                   //$('.messages').removeClass('hide').addClass('show');
                  //  $('.msg').append(data.message);
                    $('.message').text("");
                    /*if (data != '/?reg_suc=True') {
                        $.each(JSON.parse(data),function(key,input){
                            $('.'+key).html(input[0]);
                        });
                    }
                    else  {
                        window.location.href = '/?reg_suc=True';
                    }*/
                    console.log(data);
                    /*$('#register input').val('');
                    $('#ajaxloader').hide();*/
                  },
                  error: function(xhr,errmsg,err) {
                    /*$('.messages').removeClass('hide').addClass('show');
                    $('.msg').append(xhr.responseText);
                    $('#register input').val('');
                    $('#ajaxloader').hide();*/

                    console.log(xhr.status + ": " + xhr.responseText);

                  } // end error: function
                }); // end ajax func
        } // change_img end

$(document).ready(function() {
    //
    $('.del-branch').click(function (e) {
        e.preventDefault();
        $('.form-delete').attr("action","/panda-sistem/branch/"+$(this).attr('data-slug')+"/delete/");
    });
    //
    $(".chang-img").click(function (e) {
        e.preventDefault();
        $(".settings-image").click();
    });

    // security issues
    var z = true;
    $(document).on('click', '.connect-device',function () {

        var device_id = $(this).attr('data-id');
        var object = $(this);
        // if (z) {
        //     $(this).removeClass('btn-danger');
        //     $(this).addClass('btn-success');
        //     $(this).text("Qoşulub");
        //     z = false;
        // }
        // else {
        //     $(this).removeClass('btn-success');
        //     $(this).addClass('btn-danger');
        //     $(this).text("Qoşulmayıb");
        //     z = true;
        // }
        var data = new FormData();
        data.append('device_id',device_id);
        $.ajax({
          url: "/panda-sistem/device/connection/",
          type: "POST",
          processData: false,
          contentType: false,
          data: data,
          success: function(data) {
              if (data == "true") {
                object.removeClass('btn-danger');
                object.addClass('btn-success');
                object.text("Qoşulub");
              }
              else if (data == "false")  {
                  object.removeClass('btn-success');
                 object.addClass('btn-danger');
                object.text("Qoşulmayıb");
              }
              else {
                  alert("duzgun deyil");
              }
         },
         error: function(xhr,errmsg,err) {

          console.log(xhr.status + ": " + xhr.responseText);

      } // end error: function
    }); // end ajax func
    });


    function check_element(t) {

        if (t.children()[0] == undefined) {
            t.html('<i class="fa fa-plus"></i>');
            return "+"
        }
        else if (t.children().attr('class').includes('fa-plus')) {
            t.html('<i class="fa fa-minus"></i>');
            return "-"
        }
        else if (t.children().attr('class').includes('fa-minus')) {
            t.html('<i class="fa fa-info"></i>');
            return "i"
        }
        else if (t.children().attr('class').includes('fa-info')) {
            t.html('<i class="fa fa-plus"></i>');
            return "+"
        }

    }
    $(document).on('click', '.attendance', function () {
        var student_id = $(this).closest('tr').attr('data-student-id');
        var days = $(this).attr('data-id');
        var data = new FormData();
        var result = check_element($(this));
        data.append('student_id',student_id);
        data.append('day',days);
        data.append('type',result);
        $.ajax({
          url: "/panda-sistem/attendance/",
          type: "POST",
          processData: false,
          contentType: false,
          data: data,
          success: function(data) {
            if (data == "success") {
                console.log('success');
            }
            else  {
                $('.error-msg').html('<div class="confirmation-message" style="background: #ed1c24 !important;">'+obj['__all__']+'</div>');
            }
          },
          error: function(xhr,errmsg,err) {

            console.log(xhr.status + ": " + xhr.responseText);

          } // end error: function
        }); // end ajax func

    });
    var date = new Date();
    var now = date.getDate();
    $(".table-jurnal thead tr").find("."+now).addClass("active");

    //
    $('.btnApply').click(function () {
        var data = new FormData();
        $.ajax({
              url: "/panda-sistem/hesabla/",
              type: "POST",
              processData: false,
              contentType: false,
              data: data,
              success: function(data) {
                $('.modal-body').html('<h4 class="text-center text-success">' +data + ' azn sizin bu aylıq maaşınız' + '</h4>');
              },
              error: function(xhr,errmsg,err) {

                console.log(xhr.status + ": " + xhr.responseText);

              } // end error: function
            }); // end ajax func
    });
    $('.btnforadmin').click(function () {
        var data = new FormData();
        data.append('teach',$(this).attr('data-teach'));
        $.ajax({
              url: "/panda-sistem/hesabla_for_admin/",
              type: "POST",
              processData: false,
              contentType: false,
              data: data,
              success: function(data) {
                $('.modal-body').html('<h4 class="text-center text-success">' +data + ' azn sizin bu aylıq maaşınız' + '</h4>');
              },
              error: function(xhr,errmsg,err) {

                console.log(xhr.status + ": " + xhr.responseText);

              } // end error: function
            }); // end ajax func
    });
    $('.archive').click(function () {
        var data = new FormData();
        data.append('teach',$(this).attr('data-teach'));
        $.ajax({
              url: "/panda-sistem/hesabla_for_archive/",
              type: "POST",
              processData: false,
              contentType: false,
              data: data,
              success: function(data) {
                $('.modal-body').html('<h4 class="text-center text-success">' +data + ' azn sizin bu aylıq maaşınız' + '</h4>');
              },
              error: function(xhr,errmsg,err) {

                console.log(xhr.status + ": " + xhr.responseText);

              } // end error: function
            }); // end ajax func
    });
    $('.paynow').click(function () {

        var payment_obj = $(this).attr('data-id');
        var name = $(this).attr('data-name');
        var prize = $(this).attr('data-prize');
        $('.payment_obj').attr('value',payment_obj);
        $('.student-name').text(name);
        $('.add_prize').val(prize);
    });

    // Delete student function modal
    $('.deluser').click(function () {

        var payment_obj = $(this).attr('data-id');
        var name = $(this).attr('data-name');
        var prize = $(this).attr('data-prize');
        $('.deleted_obj').attr('value',payment_obj);
        $('.del-student-name').text(name);
        $('.add_prize').val(prize);
    });
    // testiqlemek ucun js
    $('.btnConfirm').click(function () {
        var data = new FormData();
        var data_id = $(this).attr("data-id");
        var my_obj = $(this);
        data.append('student_id',data_id);
        $.ajax({
                  url: "/panda-sistem/confirmed-student/",
                  type: "POST",
                  processData: false,
                  contentType: false,
                  data: data,
                  success: function(data) {
                    if (data == "success") {
                        $('.student-'+data_id).prepend('<img src="/static/img/panda.png" class="img-responsive"> ');
                        $('.student-'+data_id+' a').addClass('green');
                        my_obj.removeClass('btnConfirm');
                        my_obj.attr('disabled','disabled');
                        my_obj.text('Təstiqləndi');
                    }
                    else  {
                        $('.error-msg').html('<div class="confirmation-message" style="background: #ed1c24 !important;">'+obj['__all__']+'</div>');
                    }
                  },
                  error: function(xhr,errmsg,err) {

                    console.log(xhr.status + ": " + xhr.responseText);

                  } // end error: function
                }); // end ajax func
        });

    // Other sistem ucun js
    $('.btnConfirms').click(function () {
        var data = new FormData();
        var data_id = $(this).attr("data-id");
        var my_obj = $(this);
        data.append('student_id',data_id);
        $.ajax({
                  url: "/panda-sistem/confirmed-student/",
                  type: "POST",
                  processData: false,
                  contentType: false,
                  data: data,
                  success: function(data) {
                    if (data == "success") {
                        $('.student-'+data_id+' a').addClass('green');
                        my_obj.removeClass('btnConfirms');
                        my_obj.attr('disabled','disabled');
                        my_obj.text('Təstiqləndi');
                    }
                    else  {
                        $('.error-msg').html('<div class="confirmation-message" style="background: #ed1c24 !important;">'+obj['__all__']+'</div>');
                    }
                  },
                  error: function(xhr,errmsg,err) {

                    console.log(xhr.status + ": " + xhr.responseText);

                  } // end error: function
                }); // end ajax func
        });

});