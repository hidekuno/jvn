//
// JVN Vulnerability Infomation Managed System
//
// hidekuno@gmail.com
//

//====================================================================
// チェックボックス制御
//====================================================================
$('#header_check').on('click', function() {
     $('.rec').prop('checked', $('#header_check').prop('checked'));
});

var change_undefine = function(status) {

    var rows =  $('#vulnerability_prodcut')[0].rows;
    $.each(rows, function(i) {
        var cells = rows[i].cells;
        if ( $(cells[1]).text() == "未定義" ) {
            var id = '#check' + i;
            $(id).prop('checked', status);
        }
    });
}

$('#undefine_select_btn').on('click', function() {
    change_undefine(true);
});
$('#undefine_clear_btn').on('click', function() {
    change_undefine(false);
});
$('#all_select_btn').on('click', function() {
    $('input[type = "checkbox"]').prop('checked', true);
});
$('#all_clear_btn').on('click', function() {
    $('input[type = "checkbox"]').prop('checked', false);
});
//====================================================================
// 製品検索画面入力チェック制御
//====================================================================
$('#maintenance_btn').click(function() {

    if ($("#product_list_tbl tbody").children().length < 1) {
        bootbox.alert('メンテナンス対象となる製品情報が存在しません。', function(result) {});
        return false;
    }
    return true;
});
//====================================================================
// 脆弱性情報確認画面　全選択
//====================================================================
$('#cover_item_btn').click(function() { $('.product_select').val('cover_item'); });
$('#not_cover_item_btn').click(function() { $('.product_select').val('not_cover_item'); });

//====================================================================
// 不正画面使用の対策
//====================================================================
$(window).load(function() {
    var token = $('meta[name="token"]').attr('content');
    $("<input>", {
        type:  'hidden',
        name:  'web_token',
        id:    'web_token',
        value: token
    }).appendTo('form');
});
//====================================================================
// JVN 脆弱性情報依頼チェック制御
//====================================================================
$('#execute_btn').click(function() {

    if ($("#product_list_tbl tbody").children().length < 1) {
        bootbox.alert('メンテナンス対象となる製品情報が存在しません。', function(result) {});
        return false;
    }
    return true;
});
//====================================================================
// 日付入力
//====================================================================
$(function(){
    $('#dp_from').datetimepicker({lang:"ja", format: 'Y/m/d 00:00:00'});
    $('#dp_to').datetimepicker({lang:"ja", format: 'Y/m/d H:i:00'});
});
//====================================================================
// 日付チェック関数
//====================================================================
function checkDate( str ) {
    // str == null || str == '' as same
    if (!str) {
        return true;
    }
    var d = new Date(str);
    if (isNaN(d)) {
        return false;
    } else {
        return true;
    }
}
//====================================================================
// 脆弱性情報確認画面　全選択
//====================================================================
$('#vul_search_btn').click(function() {
    if (false == checkDate($('#dp_from').val())) {
        bootbox.alert('YYYY-MM-DD HH:MI:SS形式で入力してください。', function(result) {});
        return false;
    }
    if (false == checkDate($('#dp_to').val())) {
        bootbox.alert('YYYY-MM-DD HH:MI:SS形式で入力してください。', function(result) {});
        return false;
    }
    return true;
});
//====================================================================
// JVN 脆弱性情報一覧からの画面遷移をPostで行うようにする
//====================================================================
$('.jvn_list_product_button').click (
    function() {
        $('#listForm').attr('action', $('#topuri').val() + '/jvn_operation/index');
        $('#identifier').val($(this).attr('id'));
        $('#listForm').submit();
    }
);
$('.jvn_list_ticket_button').click (
    function() {
        $('#listForm').attr('action', $('#topuri').val() + '/jvn_ticket/index');
        $('#identifier').val($(this).attr('id'));
        $('#listForm').submit();
    }
);
//====================================================================
// JVN アカウント情報一覧からの画面遷移をPostで行うようにする
//====================================================================
$('.jvn_list_account_button').click (
    function() {
        $('#user_id').val($(this).attr('id'));
        $('#accoutForm').submit();
    }
);
//====================================================================
// メニューボタンクリック(jvn_menu_btn)
//====================================================================
$(".jvn_menu_btn").each( function(i) {
    var appname = $(this).attr("id");
    $('a#' + appname).click(
        function() {
            var cve = $("#cve_txt").val();
            if (appname == "jvn_cve" && !cve.match(/^CVE-[0-9][0-9][0-9][0-9]-/)) {
                bootbox.alert('CVE番号の形式で入力してください。', function(result) {});
                return false;
            }
            $('#cve_hidden').val(cve);
            $('#headerForm').attr('action', $('#topuri').val() + '/' + appname + '/index');
            $('#headerForm').submit();
        }
    );
});
