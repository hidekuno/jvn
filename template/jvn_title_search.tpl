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
          <h1 class="page-header">JVN タイトル製品情報検索</h1>
          <div class="form-search">
            <form role="form" method="post" action="{{app.topuri}}/jvn_title_search/search">
            <input type="text" id="keyword_txt" name="keyword"  value="{{app.ui.keyword}}"  class="form-control"  placeholder="キーワード..." required autofocus>
  
              <button class="btn btn-lg btn-primary jvn-search" id="product_search_btn" type="submit">
              <span class="glyphicon glyphicon-search"></span>検索</button>
            </form>
          </div>

          <div class="table-responsive">
            <table id="product_list_tbl" class="table table-striped">
              <thead>
                <tr>
                  <th>No</th>
                  <th>ベンダー名</th>
                  <th>製品名</th>
                  <th>cpe(/{種別}:{ベンダ名}:{製品名}:{バージョン}:{アップデート}:{エディション}:{言語})</th>
                </tr>
              </thead>
              <tbody>
                {% for item in app.result %}
                <tr>
                  <td>{{ item[0] }}</td>
                  <td>{{ item[1] }}</td>
                  <td>{{ item[2] }}</td>
                  <td>{{ item[3] }}</td>
                </tr>
                {% endfor %}

              </tbody>
            </table>
{% include 'template/jvn_pager.tpl' %}

            <form role="form" method="post" action="{{app.topuri}}/jvn_title_search/maintenance">
               <button class="btn btn-lg btn-primary jvn-search" id="maintenance_btn" type="submit">
               <span class="glyphicon glyphicon-wrench"></span>メンテナンス</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    {% if app.error_message != '' %}
        <center><h4 style="color:red">{{ app.error_message }}</h4></center>
    {% endif %}
{% include 'template/jvn_footer.tpl' %}
