/**
 * Created by hzl on 2016/11/29.
 */

var xmlHttp;

/**
 * 发送请求
 * @param str
 */
function showUser(str)
{
    xmlHttp=GetXmlHttpObject();
    if (xmlHttp==null)
    {
        alert ("Browser does not support HTTP Request");
        return
    }
    var url="getuser.php";
    url=url+"?q="+str;
    url=url+"&sid="+Math.random();
    xmlHttp.onreadystatechange=stateChanged;
    xmlHttp.open("GET",url,true);
    xmlHttp.send(null)
}

/**
 * 逻辑处理
 */
function stateChanged()
{
    if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
    {
        //解析json
        var status= $.parseJSON(xmlHttp.responseText);
        if(status.id===$("#nameinput").val()){
            document.getElementById("txtHint").innerHTML=status.FirstName;
        }else {
            document.getElementById("txtHint").innerHTML="nothing found";
        }

    }
}
/**
 * 根据不同浏览器，获得getxmlhttpobject对象
 * @returns {*}
 * @constructor
 */
function GetXmlHttpObject()
{
    var xmlHttp=null;
    try
    {
        // Firefox, Opera 8.0+, Safari
        xmlHttp=new XMLHttpRequest();
    }
    catch (e)
    {
        //Internet Explorer
        try
        {
            xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e)
        {
            xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    return xmlHttp;
}
