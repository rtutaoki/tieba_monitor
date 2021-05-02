//添加响应事件
window.onload=function(){
    document.getElementById("searchBtn").addEventListener("click",query,false);
    document.getElementById("addWordBtn").addEventListener("click",addWord,false);

};

// 等待转圈圈实现


//用于添加禁用词
function addWord(){
    var word = document.getElementById("addWordInput").value;
    if(word === ""){
        alert("非法输入！");
        return;
    }
    var formData = new FormData();
    formData.append("word", word);
    var url = "http://127.0.0.1:5000/add_word";
    var request = new XMLHttpRequest();
    request.onload = function (){
        if(request.status === 200){
            var res = request.response;
            res = JSON.parse(res);
            console.log(res);
            alert(res);
            document.getElementById("addWordInput").value="";
        }
    }
    request.open("POST", url);
    request.send(formData);
}

//用于清空之前的内容
function clear(){
    var artTable = document.getElementById("table");
    console.debug(artTable.getElementsByTagName("thead")[0]);
    var artBody=artTable.tBodies[0];
    artBody.parentNode.outerHTML = artBody.parentNode.outerHTML.replace(artBody.innerHTML, "");
}

//查询按钮实现查询功能
function query(){
    document.getElementById("searchBtn").disabled = true
    clear();
    var url = "http://127.0.0.1:5000/search";
    var request = new XMLHttpRequest();
    request.onload = function (){
        if(request.status === 200){
            var res = request.response;
            res = JSON.parse(res);
            console.log(res);
            if(res.length === 0){
                alert("无结果！请添加禁用词或用户言论正常。");
            }
            else {
                for(var i in res){
                    var content = JSON.parse(res[i]);
                    addTableContent(content);
                }

            }
            document.getElementById("searchBtn").disabled = false
        }
    }
    request.open("GET", url);
    request.send();
}

//动态向表格中添加数据
function addTableContent(content){
    // var test = {"floor_id": "123123", "user_id": "111", "user_name": "xd", "floor_content": "哈哈哈", "tie_id": "999"}


    var trElt=document.createElement("tr");
    trElt.setAttribute("id","floor-"+content.floor_id);//设置tr的属性
    var floorId=document.createElement("td");
    var userId=document.createElement("td");
    var userName=document.createElement("td");
    var floorContent=document.createElement("td");
    var tieID = document.createElement("td");

    floorId.appendChild(document.createTextNode(content.floor_id));
    userId.appendChild(document.createTextNode(content.user_id));
    userName.appendChild(document.createTextNode(content.user_name));
    floorContent.appendChild(document.createTextNode(content.floor_content));
    tieID.appendChild(document.createTextNode(content.tie_id));

    trElt.appendChild(floorId);
    trElt.appendChild(userId);
    trElt.appendChild(userName);
    trElt.appendChild(floorContent);
    trElt.appendChild(tieID);

    document.getElementById("floor-body").appendChild(trElt);
}