{#
 # JVN Vulnerability Infomation Managed System
 #
 # hidekuno@gmail.com
 #
 #}
{% include 'template/jvn_header.tpl' %}
    <div class="container-fluid">
      <h1 class="page-header">{{ app.title_name }}</h1>
      <center>
        <img src = {{ app.image_url }} />
      </center>
    </div>
    {% if app.error_message != '' %}
        <center><h4 style="color:red">{{ app.error_message }}</h4></center>
    {% endif %}
{% include 'template/jvn_footer.tpl' %}