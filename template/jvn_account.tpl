{#
 # JVN Vulnerability Infomation Managed System
 #
 # hidekuno@gmail.com
 #
 #}
{% include 'template/jvn_header.tpl' %}
    <div class="container-fluid">
      <div class="row">
        <div class="main">
          <h1 class="page-header">JVN アカウント情報一覧</h1>

          <br>
          <div class="table-responsive">

            <form id="accoutForm" role="form" method="post" action="{{app.topuri}}/jvn_account/modify">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>氏名</th>
                  <th>メールアドレス</th>
                  <th>部門</th>
                  <th>権限</th>
                  <th>　</th>
                </tr>
              </thead>
              <tbody>
                {% for item in app.result %}
                <tr>
                  <td>{{ item.user_id }}</td>
                  <td>{{ item.user_name }}</td>
                  <td>{{ item.email }}</td>
                  <td>{{ item.department}}</td>
                  <td>{{ item.privs }}</td>
                  <td>
                      <button class="btn btn-sm btn-primary jvn_list_img_button jvn_list_account_button" id="{{item.user_id}}">
                        <span class="glyphicon glyphicon-wrench"></span></button>
                      <button type="button" class="btn btn-sm btn-primary jvn_list_img_button jvn_del_account_button" data-toggle="modal" data-target="#dialog-confirm" id="{{item.user_id}}">
                        <span class="glyphicon glyphicon-trash"></span></button>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
            <input type="hidden" name="user_id" id="user_id" value="" />
            </form>

            <form role="form" method="post" action="{{app.topuri}}/jvn_account/regist">
               <input type="hidden" name="web_token" value="{{app.web_token}}" ></input>
               <button class="btn btn-lg btn-primary jvn-search" id="account_regist_btn" type="submit">
               <span class="glyphicon glyphicon-wrench"></span>新規登録</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="form-group">
    <form role="form" method="post" id="form_delete" action="{{app.topuri}}/jvn_account/delete">
       <div style="display:none;">
       <input type="hidden" name="web_token" value="{{app.web_token}}" />
       <input type="hidden" name="delete_user_id" id="delete_user_id" value="" />
       </div>
    </form>
    </div>

    {% include 'template/jvn_dialog.tpl' %}
    <script type='text/javascript'>

      $('.jvn_del_account_button').click( function() {
        $('#delete_user_id').val($(this).attr('id'));
        $('#modal-title').text('アカウント情報削除');
        $('#dialog-confirm-msg').text('以下のアカウントを削除します');
        $('#dialog-confirm-data').text('アカウントID:' + $(this).attr('id'));
        $('#dialog-keyword').prop('placeholder','delete');
      });

      $(function() {
        $('#dialog-confirm').modal({
          backdrop: 'static',
          show    : false,
          keyboard: false
        });
        $('#dialog-confirm-btn').on('click.check', function() {
          if ($('#dialog-keyword').val() == '') {
             $('#dialog-error').html('<br />キーワードは必須入力です。').removeClass('hide');
             return;
          } else if ($('#dialog-keyword').val() != $('#dialog-keyword').attr('placeholder')) {
              $('#dialog-error').html('<br />キーワードを正しく入力して下さい。').removeClass('hide');
             return;
          } else {
              $('#dialog-error').addClass('hide');
          }
          $('#form_delete').submit();
          $('#dialog-confirm').modal('hide');
        });

        $('#dialog-close').on('click', function() {
          $('#dialog-confirm-error').addClass('hide');
        });

        $('#dialog-confirm-btn-cancel').on('click', function() {
          $('#dialog-confirm-error').addClass('hide');
        });
      });
    </script>

    {% if app.error_message != '' %}
     <center><h4 style="color:red">{{ app.error_message }}</h4></center>
    {% endif %}
{% include 'template/jvn_footer.tpl' %}
