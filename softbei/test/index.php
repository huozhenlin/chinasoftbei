<!doctype html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>数据可视化</title>
    <link rel="stylesheet" href="css/style.css" type="text/css"/>
    <script type="text/javascript" src="js/jquery-1.7.2.js"></script>
    <script type="text/javascript" src="js/layer.js"></script>
    <script type="text/javascript" src="js/zySearch.js"></script>


</head>
<body style="">
<div style=""><div class="zySearch "  id="zySearch"></div></div>

<script type="text/javascript">
    /**
     * Created by hzl on 2017/5/25.
     */
    hostname = "http://" + location.host;
    function isEmptyObject(e) {
        var t;
        for (t in e)
            return !1;
        return !0
    }

    //检查用户的输入
    function check(time) {
        reg=/(\d{4})(\d{2})(\d{2})/;
        var result;
        if((result=reg.exec(time))!=null){
//            alert(result)
//            alert(result[1])
        }else {
            alert('error')
        }
        a=result[1];
        b=result[2];
        c=result[3];
        if(b.startsWith("0")){
           b=b[1]
        }
        if(c.startsWith("0")){
            c=c[1]
        }
        time1=result[1]+'/'+result[2]+'/'+result[3];
        time2=a+"/"+b+"/"+c;
        to_time=time1+","+time2;
        return to_time
    }

    $("#zySearch").zySearch({
        "width": "100%",
        "height": "33",
        "parentClass": "pageTitle",
        "callback": function (keyword) {
            if (keyword == '') {
                layer.msg('输入不能为空');
            } else {
                //var patt1 = new RegExp("[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}");
                var patt1 = new RegExp(/\d{4}\d{2}\d{2}/);
                if (patt1.test(keyword)) {
                    //检查没问题后重定向到当前surl
                    time=check(keyword);
                    var surl = "./page.php?key=" + time;

                    $.ajax({
                        //url: "http://localhost/"+keyword+".json",//接口
                        url:hostname+'/softbei/sql/cq.php?time='+time,
                        type:'get',
                        dataType: "json",
                        timeout: 5000,
                        success: function (msg) {
                            if(!isEmptyObject(msg)){
                                window.location.href=surl;
                            }else {
                                layer.open({
                                    type: 1,
                                    area: ['600px', '360px'],
                                    shadeClose: true, //点击遮罩关闭
                                    content: '\<\div style="padding:20px;">在数据库中找不到指定时间内容，请更换时间\<\/div>'
                                });
                            }
                        },
                        error: function () {
                            //alert(url)
                            layer.open({
                                type: 1,
                                area: ['600px', '360px'],
                                shadeClose: true, //点击遮罩关闭
                                content: '\<\div style="padding:20px;">系统错误\<\/div>'
                            });

                        }
                        });

                } else {
                    layer.msg('输入格式不正确');
                }
            }
                }

    });



</script>
</body>
</html>