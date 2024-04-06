// Data to be sent to the Flask server

const path = "https://64797083-dd51-442c-a36f-84a92c6265df-00-30ipml1u64wqw.worf.replit.dev/"

async function sendHTTPS(extension, body={"userId":"000001"}, method="POST") {
    let data = await fetch(
    path + extension, {method: method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)});
    let j = await data.json();
    return j;
}

var userId = ""

function gotopage(groupid) {
    window.location.href = '../group/group.html?userId=' + userId + '&groupId=' + groupid;
}

async function gettable() {
    console.log("Getting groups")

    var params = new URLSearchParams(window.location.search);
            // Retrieve data parameter
    
    userId = params.get('userId');
            // Display data on the page
    if (!userId) {
        userId = "000001";
    }
    let grouplist = await sendHTTPS("retreiveGroups", body={"userId":userId});
    // !!!!! WIll need to get userID from JSON Cookie
    console.log(grouplist);

    let group_count = grouplist.length;
    let table = document.getElementById("feedtable");
    console.log(table)

    for (var i = 0; i < group_count; i++) {
        var row = table.insertRow(-1);
        let groupid = grouplist[i].groupId;
        row.onclick = function() { gotopage(groupid); };
        //time || G-name || E-NAME || LOCATIOn
        var cname =  row.insertCell(0);
        var cdesc =  row.insertCell(1)
        var cmembercount =  row.insertCell(2);
        var cmax =  row.insertCell(3);

        
        cname.innerText = grouplist[i]["groupName"];
        cdesc.innerText = grouplist[i]["groupDesc"];
        cmembercount.innerText = grouplist[i]["groupMembers"].length;
        cmax.innerText = grouplist[i]["groupMax"];
    }
}