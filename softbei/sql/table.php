<?php
/**
 * Created by PhpStorm.
 * User: hzl
 * Date: 2017/6/26
 * Time: 21:14
 */
require_once "city.php";
function be_table($time)
{
    //调用city.php中的get_json（）方法，参数为事件
    $json = json_decode(get_json($time), true);//将Json转化成数组
    $key = array_keys($json);//取出键名

    echo '<table class="table table-bordered" style="width: 100%;margin:auto;>';
    echo '<caption align="left"><h3>事件详情表</h3><a>导出表格</a></caption> ';
    echo '<tr id="bindAddress" class="first-child">';
    echo '<td class="first-child">事件</td>';
    echo '<td class="first-child">类型</td>';
    echo '<td class="nth2">开始时间</td>';
    echo '<td class="nth2">结束时间</td>';
    echo '<td class="nth3">城市</td >';
    echo '<td class="nth6">频率</td>';
    echo '<td class="nth6">热度</td>';
    echo '<td class="nth7">历史悠久程度</td>';
    echo '</tr>';
    //双重遍历得到元素
    echo '<tbody id="adminTbody">';
    for ($i = 0; $i < count($key); $i++) {
        for ($b = 0; $b < count($json[$key[$i]]); $b++) {
            echo '<tr>';
            echo '<td>' . $json[$key[$i]][$b]['event'] . '</td>';
            echo '<td>' . $key[$i] . '</td>';
            echo '<td>' . $json[$key[$i]][$b]['date'] . '</td>';

            echo '<td>' . $json[$key[$i]][$b]['endtime'] . '</td>';
            echo '<td>' . $json[$key[$i]][$b]['city'] . '</td>';

            //echo '<td>' . $json[$key[$i]][$b]['lng'] .'</td>';

            //echo '<td>' . $json[$key[$i]][$b]['lat'] .'</td>';
            echo '<td>' . $json[$key[$i]][$b]['rate'] . '</td>';
            echo '<td>' . $json[$key[$i]][$b]['hot'] . '</td>';
            echo '<td>' . $json[$key[$i]][$b]['history'] . '</td>';
            echo '</tr>';
        }
    }
    echo '</tbody>';
    echo '</table > ';
}

?>