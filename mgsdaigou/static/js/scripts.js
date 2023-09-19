// Empty JS for your own code to be here
$(function () {
    //显示图片
    //hover某处显示悬浮框
    $(".disable-icon").mouseover(function(e){
        var __taskId = $(this).attr("id");
        //获取鼠标位置函数
        var mousePos = mousePosition(e);
        var  xOffset = 20;
        var  yOffset = 25;
        $("#pic__"+__taskId).css("display","block")
        .css("position","absolute").css("top",(mousePos.y - yOffset) + "px")
        .css("left",(mousePos.x + xOffset) + "px");

     });
     //鼠标离开表格隐藏悬浮框
     $(".disable-icon").mouseout(function(){
        var __taskId = $(this).attr("id");
         $("#pic__"+__taskId).css("display","none");
     });
});


//获取鼠标坐标
function mousePosition(ev){
    ev = ev || window.event;
    if(ev.pageX || ev.pageY){
        return {x:ev.pageX, y:ev.pageY};
    }
    return {
        x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
        y:ev.clientY + document.body.scrollTop - document.body.clientTop
    };
}



// 登出用户
function logout(){
    $(location).prop("href", "/logout");
}