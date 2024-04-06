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
let groupId = ""

function nav(loc) {
    console.log(loc);
    let s = "";
    s = "../mygroups/mygroups.html";

    window.location.href = s + '?userId=' + userId;
}

async function view_did_load() {

    var params = new URLSearchParams(window.location.search);
            // Retrieve data parameter
    
    userId = params.get('userId');
    groupId = params.get('groupId');
            // Display data on the page
    if (!userId) {
        userId = "000001";
    }
    console.log("Getting upcoming events" + groupId.toString())
    let groupinfo = await sendHTTPS("retreiveGroupInfo", body={"groupId":groupId});
    // !!!!!!!! Will need groupID from cookie


    console.log(groupinfo);
    let maxMembers = groupinfo.groupPeopleMax;
    let groupMembers = groupinfo.groupMembers;
    let currCount = groupMembers.length;

    //get group name, show it
    let name = groupinfo.groupName;
    let namehead = document.getElementById("groupname");
    namehead.innerText = name;

    
    let membershead = document.getElementById("members");
    membershead.innerText = "You have " + currCount.toString() + "/" + maxMembers.toString() + "members!";


    //Get group interests, display them in table
    let interests = groupinfo.groupInterests;
    let interests_div = document.getElementById("interestsdiv");


    for (var i = 0; i < interests.length; i++) {
        let tag = document.createElement("div");
        tag.className = "tagdiv";

        let tagp = document.createElement("p");
        tagp.innerText = interests[i];
        
        let tagbutton = document.createElement("button");
        tagbutton.innerText = "X"
        tagbutton.className = "delbutton";

        tag.appendChild(tagp);
        tag.appendChild(tagbutton);
        interests_div.appendChild(tag);
    }




    //Get group sujects, display them in table
    let subjects = groupinfo.groupSubjects;
    let subjects_div = document.getElementById("subjectsdiv");


    for (var i = 0; i < subjects.length; i++) {
        let tag = document.createElement("div");
        tag.className = "fetchdiv";

        let tagp = document.createElement("p");
        tagp.innerText = subjects[i];
        
        let tagbutton = document.createElement("button");
        tagbutton.innerText = "X"
        tagbutton.className = "delbutton";

        tag.appendChild(tagp);
        tag.appendChild(tagbutton);
        subjects_div.appendChild(tag);
    }

    //Get group member numbers
    

    

    //Display tables
    let tablestable =  document.getElementById("tablestable");

    var unseated_person = currCount;
    var empty_seats = maxMembers - currCount;

    console.log(unseated_person, empty_seats);

    var tables = [];
    
    while (unseated_person > 0 || empty_seats > 0) {
        var curr_table = [0,0];
        var s = 0;
        while (s < 6 && (unseated_person > 0 || empty_seats > 0)) {
            if (unseated_person > 0) {
                curr_table[0]++;
                unseated_person--;
            }
            else {
                curr_table[1]++;
                empty_seats--;
            }
            s++;
        }
        tables = tables.concat([curr_table]);
    }

    console.log(tables);
    var row;
    row = tablestable.insertRow(-1);

    const column = Math.floor(Math.sqrt(tables.length)+.9)

    for (var i = 0; i < tables.length; i++) {
        
        if (i % column == 0) {
            row = tablestable.insertRow(-1);
        }

        
        c = row.insertCell(-1);
        var img = document.createElement('img');
        curr_table = tables[i];
        img.src = "./assets/tables/" + (curr_table[0]+curr_table[1]).toString() + "-" + curr_table[0].toString() + ".png";
        
        img.style.width = (600/column).toString() + "px";
        img.style.height = (600/column).toString() + "px";
        console.log(img.style.width);
        c.appendChild(img);
        


    }

}



