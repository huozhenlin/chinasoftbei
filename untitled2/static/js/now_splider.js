/**
 * Created by hzl on 2017/8/18.
 */
var data = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"];
var objArr = [];
hostname="http://"+location.host;
for (var i = 0; i < data.length; i++) {
    var obj = new Object();
    obj.id = i;
    obj.value = data[i];
    objArr.push(obj);
}
$(function () {
    //加载多选框的数据
    var ul = $("#ul");
    for (var i = 0; i < objArr.length; i++) {
        ul.append("<li><div class='checkbox'></div><label><input type='checkbox' value=" + objArr[i].id + " onclick='Choose(this)'/>" + objArr[i].value + "</label></li>");
    }
    for (var i = 0; i <= 1; i++) {
        showTask(i)
    }
});
//显示多选框
function show(t) {
    //设置多选框显示的位置，在选择框的中间
    var left = t.offsetLeft + t.clientWidth / 2 - $("#panel")[0].clientWidth / 2
    var top = t.offsetTop + t.clientHeight + document.body.scrollTop;
    $("#panel").css("display", "block");
    $("#panel").css("margin-left", left);
    $("#panel").css("margin-top", top + 5);
}
//隐藏多选框
function hide() {
    $("#panel").css("display", "none");
}
//全选操作
function CheckAll(t) {
    var name = "";
    var ids = "";
    var popoverContent = $($(t).parent().parent().parent().children()[2]);
    popoverContent.find("input[type=checkbox]").each(function (i, th) {
        th.checked = t.checked;
        if (t.checked) {
            name += $(th).parent().text() + ",";
            ids += $(th).val() + ",";
        }
    });
    name = name.substr(0, name.length - 1);
    ids = ids.substr(0, ids.length - 1);
    $("#txt").val(name);
    $("#ids").val(ids);
}

//勾选某一个操作
function Choose(t) {
    var oldName = $("#txt").val();
    var name = oldName == "" ? "," + $("#txt").val() : "," + $("#txt").val() + ",";
    var ids = oldName == "" ? "," + $("#ids").val() : "," + $("#ids").val() + ",";
    var newName = $(t).parent().text();
    var newid = $(t).val();

    if (t.checked) {//选中的操作
        $("#txt").val(name += newName + ",");
        $("#ids").val(ids += newid + ",");
    } else {//去掉选中的操作
        var index = name.indexOf("," + newName + ",");
        var len = newName.length;
        name = name.substring(0, index) + name.substring(index + len + 1, name.length);

        var index = ids.indexOf("," + newid + ",");
        var len = newid.length;
        ids = ids.substring(0, index) + ids.substring(index + len + 1, ids.length);
    }
    name = name.substr(1, name.length - 2);
    ids = ids.substr(1, ids.length - 2);
    $("#txt").val(name);
    $("#ids").val(ids);
}

//异步处理，添加任务
function addTask() {
    var task_name = $('#task_name').val();
    var types = $('#ids').val();
    var type = $('#splider_type').val();
    var ajaxCallUrl=hostname+"/message";
    $.ajax({
        cache: true,
        type: "POST",
        url: ajaxCallUrl,
        timeout:3000,
        data: $('#myForm').serialize(),// 你的formid
        async: false,
        error: function (request) {
            alert('添加成功');
            showTask(0);
            showTask(1);
        },
        success: function (data) {
            alert('添加成功');
            showTask(0);
            showTask(1);
        }
    });

}

//异步处理,展示任务
function showTask(num) {

    var url = hostname+'/json?status=' + num;
    // $.getJSON(url, function (res) {
    //     var result = res;
    //     analysis(result);
    // })
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function (data) {

            //遍历json,生成不同的div放到盒子中
            if (num == 0) {
                //清空盒子中的内容
                $("#spliding").html('');
                $.each(data['objects'], function (index, n) {

                    // 预处理
                    var type;
                    var types;
                    if (n.type == 0) {
                        type = "即时爬虫";
                    } else if (n.type == 1) {
                        type = "定时爬虫"
                    } else {
                        type = "数据分析"
                    }
                    var datas = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"];
                    var str = n.types;
                    var new_strs=new Array();
                    var strs = str.split(","); //字符分割
                    for (s = 0; s < strs.length; s++) {
                        // alert(datas[strs[s]]);
                        new_strs.push(datas[strs[s]])
                    }
                    var types=new_strs.join(",");
                    $("#spliding").append(
                        // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                        "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                        "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                        "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                        "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                        "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                        "<button type=\"button\" class=\"btn btn-default \" onclick='start(" + n.id + ")'>" +
                        "<i class=\"fa fa-play text-green\" style=\"color: green\"></i>" +
                        "</button>" +
                        "<button type=\"button\" class=\"btn btn-default\" onclick='stop(" + n.id + ")'>" +
                        "<i class=\"fa fa-square text-red\" style=\"color: red\"></i>" +
                        "</button>" +
                        "</div>" +
                        "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
                        "</button>" +
                        "</div>" +
                        "</div>" +
                        "<div class=\"box-body\">" +
                        "<div class=\"row\">" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫id：</strong>" + n.id +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫起止时间：</strong>" + n.time + "&nbsp;&nbsp; &nbsp;&nbsp;" +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫种类：</strong>" + type +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫任务：</strong>" + types +
                        "</p>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "</div>"
                    );
                });
            } else {
                $('#history_spliding').html('');
                $.each(data['objects'], function (index, n) {
                    // 预处理
                    var type;
                    var types;
                    if (n.type == 0) {
                        type = "即时爬虫";
                    } else if (n.type == 1) {
                        type = "定时爬虫"
                    } else {
                        type = "数据分析"
                    }
                    var datas = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"];
                    var str = n.types;
                    var new_strs=new Array();
                    var strs = str.split(","); //字符分割
                    for (s = 0; s < strs.length; s++) {
                        // alert(datas[strs[s]]);
                        new_strs.push(datas[strs[s]])
                    }
                    var types=new_strs.join(",");

                    $("#history_spliding").append(
                        // "<li><a href='" + n.url + "'>" + n.title + "</a></li>"
                        "<div class=\"col-md-3 col-sm-6 col-xs-12\" style=\"background-color: #f0efee\">" +
                        "<div class=\"box-header\" style=\"cursor: move; height: 50px\">" +
                        "<h4 class=\"box-title\"><i class=\"fa fa-tasks\"></i>" + n.name + "</h4>" +
                        "<div class=\"pull-right box-tools\" style=\"margin-top: -30px\">" +
                        "<div class=\"btn-group\" data-toggle=\"btn-toggle\">" +
                        "</button>" +
                        "</div>" +
                        "<button type=\"button\" class=\"btn btn-default\" onclick='deleteTask(" + n.id + ")'><i class=\"fa fa-times\"></i>" +
                        "</button>" +
                        "</div>" +
                        "</div>" +
                        "<div class=\"box-body\">" +
                        "<div class=\"row\">" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫id：</strong>" + n.id +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫起止时间：</strong>" + n.time + "&nbsp;&nbsp; &nbsp;&nbsp;" +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫种类：</strong>" + type +
                        "</p>" +
                        "</div>" +
                        "<div class=\"col-md-12\">" +
                        "<p><strong>爬虫任务：</strong>" + types +
                        "</p>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "</div>"
                    );
                });
            }

        }
    });
}


//解析json
function analysis(result) {
    // 根据不同的状态，自动写入不同的div
    pass
}
//启动任务
function start(id) {
    var url=hostname+'/start?id='+id+"&status=1";
    $.getJSON(url,function (res) {
        var result = res;
        if (result['startmess'] =='ok'){
            alert('爬虫启动成功')
        }else {
            alert('爬虫启动失败')
        }
    })
}
//停止任务
function stop(id) {
    var url=hostname+'/stop?id='+id+"&status=0";
    $.getJSON(url,function (res) {
        var result = res;
        if (result['startmess'] =='ok'){
            alert('爬虫关闭成功')
        }else {
            alert('爬虫启动成功')
        }
    })
}

//异步处理，删除任务
function deleteTask(id) {
    var url = hostname+'/deljson?delete=' + id;
    $.getJSON(url, function (res) {
        var result = res;
        if (result['delmes'] == 'ok') {
            alert('成功')
            showTask(0)
            showTask(1)
        } else {
            alert('失败')
        }
    })
}
