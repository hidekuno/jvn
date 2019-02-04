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
          <center>
            <h1 style="color:red" class="page-header">システムエラーが発生しました。</h1>
            <h4 style="color:red" class="page-header">{{ app.exception }}</h4>
            保守担当者までお問い合わせください。(不正操作の場合は、もう一度最初からやり直してください。)
          </center>
        </div>
      </div>
    </div>
{% include 'template/jvn_footer.tpl' %}
