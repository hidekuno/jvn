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
          <h1 class="page-header">{{ app.title_name }}</h1>
          <br>
          <center>
          <div class="table-responsive">
            <table class="table table-striped" style="width:60%">
              <thead>
                <tr>
                  <th>No</th>
                  <th>名称</th>
                  <th>件数</th>
                </tr>
              </thead>
              <tbody>
                {% for item in app.result %}
                <tr>
                  <td>{{ loop.index }}</td>
                  <td>{{ item[0] }}</td>
                  <td align="right">{{ item[1] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
            <input type="hidden" name="identifier" id="identifier" value="" />
          </div>
          </center>
        </div>
      </div>
    </div>
    {% if app.error_message != '' %}
        <center><h4 style="color:red">{{ app.error_message }}</h4></center>
    {% endif %}
{% include 'template/jvn_footer.tpl' %}