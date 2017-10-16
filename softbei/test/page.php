<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>数据可视化</title>
    <script type="text/javascript" src="js/jquery-1.7.2.js"></script>
    <script type="text/javascript" src="js/echarts.js"></script>
    <script type="text/javascript" src="data/china.js"></script>
    <script type="text/javascript" src="data/shine.js"></script>
    <!--    <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>-->
    <script type="text/javascript" src="js/zySearch.js"></script>
    <script type="text/javascript" src="js/check.js"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <style type="text/css">
        .barcon1 {
            font-size: 17px;
            float: left;
            margin-top: 20px;
        }

        .barcon2 {
            float: right;
        }

        .barcon2 ul {
            margin: 20px 0;
            padding-left: 0;
            list-style: none;
            text-align: center;
        }

        .barcon2 li {
            display: inline;
        }

        .barcon2 a {
            font-size: 16px;
            font-weight: normal;
            display: inline-block;
            padding: 5px;
            padding-top: 0;
            color: black;
            border: 1px solid #ddd;
            background-color: #fff;
        }

        .barcon2 a:hover{
            background-color: #eee;
        }

        .ban {
            opacity: .4;
        }
    </style>
</head>
<body style="text-align:center;">

<div id="all" style="width: 80%;margin: 10px auto">
    <!--    地图描点-->
    <div id="container" style="height: 700px;width:100%;margin:40px auto;padding-right:10px;"></div>
    <!--    同一行柱状图，饼状图-->
    <div style="width:100%;height:300px;margin-bottom: 25px">
        <div id="pic" style="height: 300px;width: 40%;float: left"></div>
        <div id="histogram" style="height: 300px;width: 40%;float: right"></div>
    </div>
    <!--    显示城市的事件个数-->
    <div id="num_city" style="height: 400px;width: 100%"></div>
    <!--    显示热度等情况的表格-->
    <div id="more_information" style="width: 100%;margin: 0px auto；margin-top: 20px">
        <?php
        require_once "../sql/table.php";
        //调用table.php中的be_tabel()方法，接收url中传入的key
        be_table($_GET['key'])
        ?>
    </div>

    <!--    这是分页控制跳转的按钮-->
    <div id="barcon" class="barcon" >
        <div id="barcon1" class="barcon1"></div>
        <div id="barcon2" class="barcon2">
            <ul>
                <li><a href="###" id="firstPage">首页</a></li>
                <li><a href="###" id="prePage">上一页</a></li>
                <li><a href="###" id="nextPage">下一页</a></li>
                <li><a href="###" id="lastPage">尾页</a></li>
                <li><select id="jumpWhere">
                    </select></li>
                <li><a href="###" id="jumpPage" onclick="jumpPage()">跳转</a></li>
            </ul>
        </div>
    </div>
</div>
    <script type="text/javascript">
        /**
         * Created by hzl on 2017/5/25.
         */
            //请求地址
		var hostname="http://"+location.host;
        var Arr = [];//存放城市的列表
        var new_arr = [];//存放城市去重后的列表
        var new_list = [];//城市和个数的字典
        var dic = new Array();//定义一个字典放不同类型的数据
        var legendArr; //图例
        var option;//地图参数
        var option2;//饼状图
        var option3;//演唱会等各类事件的柱状图和条形图
        var option4;//城市的柱状图和条形图
        var dom = document.getElementById("container");
        var dom2 = document.getElementById("pic");
        var myChart = echarts.init(dom, 'shine');
        var myChart2 = echarts.init(dom2);
        var myChart3 = echarts.init(document.getElementById('histogram'));
        var myChart4 = echarts.init(document.getElementById('num_city'));
        //获取get参数
        function GetQueryString(name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null)return unescape(r[2]);
            return null;
        }
        //接收url参数，名为key
        var keyword = GetQueryString("key");
        if (keyword == null) {
            window.location.href = './index.php'
        } else {
            //var url = hostname + keyword + '.json';//请求地址
            var url = hostname+'/softbei/sql/cq.php?time=' + keyword;
            //alert(url);
            //这里请求数据
            $.getJSON(url, function (res) {
                legendArr = [];
                var result = res;
                analysis(result);
                console.log(legendArr);

                option.legend.data = legendArr;//设置图例
                option2.legend.data = legendArr;//给饼状图设置图例
                for (var key in dic) {
                    var series =
                        {
                            name: key,
                            type: 'scatter',
                            coordinateSystem: 'geo',
                            data: dic[key]
                        };
                    option.series.push(series)

                }
                myChart.setOption(option, true);
                myChart2.setOption(option2, true);
                myChart3.setOption(option3, true);
                myChart4.setOption(option4, true);
                //跳转
                myChart.on('click', function (param) {
                    var name = param['name'];

//                $('#indexbaidu').attr('src',"https://index.baidu.com/?tpl=crowd&word="+encodeURI(name));
//                $('#indexbaidu').show()

                })
            });
        }


        //分析数据
        function analysis(data) {
            get_city(data);
            var servies = {
                name: '事件出现次数',
                type: 'bar',
                barWidth: '60%',
                data: new_list
            };

            var aAxis = {
                type: 'category',
                data: new_arr,
                axisTick: {
                    alignWithLabel: true
                }
            };

            option4.yAxis.push(aAxis);
            option4.series.push(servies);

            //定义一个空的对象
            for (i in data) {
                var end_obj = []
                console.log(i)

                legendArr.push(i);//把图标名字添加进去
                console.log(i);

                for (x in  data[i]) {
                    var obj = {name: '', datas: []};
                    // console.log(x)
                    obj.name = data[i][x]['city'];  //获得地点
                    console.log(obj.name);
                    obj.value = [data[i][x]['lng'], data[i][x]['lat']];   //经纬度
                    // console.log(obj.value);
                    obj.datas[0] = data[i][x]['event'];   //事件
                    // console.log(obj.datas[0]);
                    obj.datas[1] = data[i][x]['date'];   //时间
                    //obj.datas[2] = data[i][x]['weather'];
                    console.log('------**********----------');
                    console.log(obj);
                    end_obj.push(obj);
                    dic[i] = end_obj;
                }

            }
            //这里配置name,value
            var obj2 = [];
            var nums = []
            console.log('-----------+++++++++++--------->');
            for (x in dic) {
                var num = dic[x].length;
                nums.push(num);
                console.log(x);
                var dic2 = {name: ''};
                dic2.name = x;
                dic2.value = num;
                obj2.push(dic2)
            }
            console.log('-----------+++++++++++--------->');
            var servies = {
                name: '事件频率',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: obj2,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            };
            option2.series.push(servies);


            var servies = {
                name: '事件出现次数',
                type: 'bar',
                barWidth: '60%',
                data: nums
            };

            var aAxis = {
                type: 'category',
                data: legendArr,
                axisTick: {
                    alignWithLabel: true
                }
            };
            option3.xAxis.push(aAxis);
            option3.series.push(servies);


        }

        //分析数据
        function get_city(data) {
            //定义一个空的对象
            for (i in data) {
                for (x in  data[i]) {
                    city = data[i][x]['city'];  //获得地点
                    console.log("开始获取城市");
                    console.log(city);
                    Arr.push(city)//把城市名添加进列表中

                }
            }
            total()
        }

        //统计元素个数
        function total() {
            for (var i = 0; i < Arr.length; i++) {
                var items = Arr[i];
                console.log(items);
                if ($.inArray(items, new_arr) == -1) {
                    new_arr.push(items);
                }
            }


            for (i = 0; i < new_arr.length; i++) {
                n = 0;
                var obj = {name: '', datas: []};
                for (j = 0; j < Arr.length; j++) {
                    if (Arr[j] == new_arr[i]) {
                        n++;
                    }
                }
                obj.name = new_arr[i];
                obj.value = n;
                new_list.push(obj)
            }
        }


        option = {
            backgroundColor: '#99eeff',
            title: {
                text: "当天全国发生事件分布",
                left: 'center',
                textStyle: {
                    color: '#000'
                }
            },
            tooltip: {
                trigger: 'item',
                //格式化
                formatter: function (a, b) {
                    return ('地点:' + a['name']
                    + '</br>经纬度:' + a['value']
                    + '<br>事件:' + a['data'].datas[0]
                    + '<br>时间:' + a['data'].datas[1]);
                    //+ '<br>天气:' + a['data'].datas[2]);
                }
            },

            legend: { //图例
                left: 'left',
                show: true,
                data: []//图例内容数组，数组项通常为{string}，每一项代表一个系列的name
            },

            //工具条
            toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                        show: true
                    },
                    dataView: {
                        show: true
                    }
                }
            },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: true
                    }
                },
                roam: true,

            },

            series: []

        };

        //配置饼状图
        option2 = {

            title: {
                text: '各事件占比',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },

            //工具条
            toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                        show: true
                    },
                    dataView: {
                        show: true
                    }
                }
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: []
            },
            series: []
        };

        //配置柱状图
        option3 = {

            title: {
                text: '各事件出现次数',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            //工具条
            toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                        show: true
                    },
                    dataView: {
                        show: true
                    },
                    magicType: {//动态类型切换
                        type: ['bar', 'line']
                    }
                }
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                show: true,
                data: []
            },
            series: []
        };


        option4 = {
            title: {
                text: '各城市事件出现次数',
                x: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            legend: {
                data: []
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value'
            },
            yAxis: [],
            //工具条
            toolbox: {
                show: true,
                feature: {
                    saveAsImage: {
                        show: true
                    },
                    dataView: {
                        show: true
                    },
                    magicType: {//动态类型切换
                        type: ['bar', 'line']
                    }
                }
            },
            series: []
        };

        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
        // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
        var blob = new Blob([html], { type: "application/vnd.ms-excel" });
        var a = document.getElementsByTagName("a")[0];
        // 利用URL.createObjectURL()方法为a元素生成blob URL
        a.href = URL.createObjectURL(blob);
        // 设置文件名，目前只有Chrome和FireFox支持此属性
        a.download = "事件详情表.xls";

        $(function(){
            //dynamicAddUser(80);
            goPage(1,10);
            var tempOption="";
            for(var i=1;i<=totalPage;i++)
            {
                tempOption+='<option value='+i+'>'+i+'</option>'
            }
            $("#jumpWhere").html(tempOption);
        })

        /**
         * 分页函数
         * pno--页数
         * psize--每页显示记录数
         * 分页部分是从真实数据行开始，因而存在加减某个常数，以确定真正的记录数
         * 纯js分页实质是数据行全部加载，通过是否显示属性完成分页功能
         **/

        var pageSize=0;//每页显示行数
        var currentPage_=1;//当前页全局变量，用于跳转时判断是否在相同页，在就不跳，否则跳转。
        var totalPage;//总页数
        function goPage(pno,psize){
            //这是查找到tbody的id
            var itable = document.getElementById("adminTbody");
            var num = itable.rows.length;//表格所有行数(所有记录数)

            pageSize = psize;//每页显示行数
            //总共分几页
            if(num/pageSize > parseInt(num/pageSize)){
                totalPage=parseInt(num/pageSize)+1;
            }else{
                totalPage=parseInt(num/pageSize);
            }
            var currentPage = pno;//当前页数
            currentPage_=currentPage;
            var startRow = (currentPage - 1) * pageSize+1;
            var endRow = currentPage * pageSize;
            endRow = (endRow > num)? num : endRow;
            //遍历显示数据实现分页
            /*for(var i=1;i<(num+1);i++){
             var irow = itable.rows[i-1];
             if(i>=startRow && i<=endRow){
             irow.style.display = "";
             }else{
             irow.style.display = "none";
             }
             }*/

            $("#adminTbody tr").hide();
            for(var i=startRow-1;i<endRow;i++)
            {
                $("#adminTbody tr").eq(i).show();
            }
            var tempStr = "共"+num+"条记录 分"+totalPage+"页 当前第"+currentPage+"页";
            document.getElementById("barcon1").innerHTML = tempStr;

            if(currentPage>1){
                $("#firstPage").on("click",function(){
                    goPage(1,psize);
                }).removeClass("ban");
                $("#prePage").on("click",function(){
                    goPage(currentPage-1,psize);
                }).removeClass("ban");
            }else{
                $("#firstPage").off("click").addClass("ban");
                $("#prePage").off("click").addClass("ban");
            }

            if(currentPage<totalPage){
                $("#nextPage").on("click",function(){
                    goPage(currentPage+1,psize);
                }).removeClass("ban")
                $("#lastPage").on("click",function(){
                    goPage(totalPage,psize);
                }).removeClass("ban")
            }else{
                $("#nextPage").off("click").addClass("ban");
                $("#lastPage").off("click").addClass("ban");
            }

            $("#jumpWhere").val(currentPage);
        }


        function jumpPage()
        {
            var num=parseInt($("#jumpWhere").val());
            if(num!=currentPage_)
            {
                goPage(num,pageSize);
            }
        }
    </script>

</body>
</html>
