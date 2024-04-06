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

let userId = ""


function nav(loc) {
    console.log(loc);
    let s = "";
    if (loc == 0) {
        s = "../creategroup/creategroup.html";
    }
    if (loc == 1) {
        s = "../addgroups/addgroups.html";
    }
    if (loc == 2) {
        s = "../home/home.html";
    }
    if (loc == 3) {
        s = "../mygroups/mygroups.html";
    }
    if (loc == 4) {
        s = "../profile/profile.html";
    }
    window.location.href = s + '?userId=' + userId;
}

async function gettable() {
    console.log("Getting upcoming events")
    var params = new URLSearchParams(window.location.search);
            // Retrieve data parameter
    
    userId = params.get('userId');
            // Display data on the page
    if (!userId) {
        userId = "000001";
    }
    console.log(userId);
    let eventlist = await sendHTTPS("retrieveUpcomingEvents", body={"userId":userId});
    // !!!!! WIll need to get userID from JSON Cookie
    console.log(eventlist);

    let event_count = eventlist.length;
    let table = document.getElementById("feedtable");
    console.log(table)

    for (var i = 0; i < event_count; i++) {
        var row = table.insertRow(-1);
        //time || G-name || E-NAME || LOCATIOn
        var ctime =  row.insertCell(0);
        var cgroupname =  row.insertCell(1);
        var ceventname =  row.insertCell(2);
        var clocation =  row.insertCell(3);

        ctime.innerText = eventlist[i]["eventTime"];
        cgroupname.innerText = eventlist[i]["groupName"];
        ceventname.innerText = eventlist[i]["eventName"];
        clocation.innerText = eventlist[i]["eventLocation"];
    }
}