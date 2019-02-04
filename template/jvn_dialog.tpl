{#
 # JVN Vulnerability Infomation Managed System
 #
 # hidekuno@gmail.com
 #
 #}
<div class="col-lg-1">
<div class="modal" id="dialog-confirm" tabindex="-1" role="dialog" aria-hidden="true" data-show="true" data-keyboard="false" data-backdrop="static">
  <div class="modal-dialog" style="padding: 10px">
   <div class="modal-content">
     <div class="modal-header">
       <button type="button" class="close" data-dismiss="modal" id="dialog-close">
         <span aria-hidden="true">&#215;</span><span class="sr-only">閉じる</span>
       </button>
       <h4 id="modal-title"></h4>
     </div><!-- /modal-header -->

     <div class="modal-body">
       <p id="dialog-confirm-msg"></p>
       <br>
       <p id="dialog-confirm-data"></p>
       キーワード：
       <input name="data[exec_key]" required="required" id="dialog-keyword" size="30" placeholder="confirm" type="text">
       <span id="dialog-error" class="text-danger hide"><br />キーワードを正しく入力して下さい。</span>
     </div>
     <div class="modal-footer well" style="padding: 5px">
       <button class="btn" id="dialog-confirm-btn-cancel" data-dismiss="modal" aria-hidden="true" type="submit">閉じる</button>
       <button class="btn btn-primary" id="dialog-confirm-btn" data-loading-text="実行中..." type="submit">実行</button>
      </div>
   </div> <!-- /.modal-content -->
  </div> <!-- /.modal-dialog -->
</div> <!-- /.modal -->
</div>
