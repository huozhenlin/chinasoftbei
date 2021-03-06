<?php
/**
 * Created by PhpStorm.
 * User: hzl
 * Date: 2017/6/4
 * Time: 19:30
 */
$servername = "localhost";
$username = "root";
$password = "1234";
$mysqlname = "softbei";
$json = '';
$data = array();

class User
{
    public $event;
    public $date;
    public $lng;
    public $lat;
    public $city;
}

//第二步，链接数据库，代码如下：

// 创建连接
$conn = mysqli_connect($servername, $username, $password, $mysqlname);

//第三步，定义查询语句，并执行，代码如下：time为从前端传过来的值，这里要考虑几种情况
$time = $_GET['time'];//获取从url返回的time，有两种格式，来自index.php

//切割字符，进行查找
$pattern="/,/";
$time1=preg_split($pattern,$time)[0];
$time2=preg_split($pattern,$time)[1];
//定义一个数组，根据数组动态生成json
$cars = array("演唱会", "展会", "时政", "体育", "异常天气");
//echo count($cars);
//生成json
$arr=array();
for ($i = 0; $i < count($cars); $i++) {
    $data=array();
    $sql = "SELECT city,lng,lat,start_time,event FROM data WHERE bs=$i and (start_time='$time1'or start_time='$time2')";
    $result = $conn->query($sql);
    //获取返回结果条数
    $num_rows = mysqli_num_rows($result);
    //第四步，获取查询出来的数据，并将其放在事先声明的类中，最后以json格式输出。代码如下：
    if ($num_rows > 0) {
        //echo "查询成功";
        while ($row = mysqli_fetch_array($result, MYSQL_ASSOC)) {
            $user = new User();
            $user->event = $row["event"];
            $user->date = $row["start_time"];
            $user->city = $row["city"];
            $user->lat = $row["lat"];
            $user->lng = $row["lng"];
            array_push($data,$user);
        }
        $json = json_encode($data);//把数据转换为JSON数据.
        $json   ="\"".$cars[$i]."\"". ":" .$json;
        //往数组添加元素
        array_push($arr,$json);

    } else {
        //echo "查询失败<br/>";
    }


}

mysqli_close($conn);
//生成最终的json
echo "{".join(",",$arr)."}";

