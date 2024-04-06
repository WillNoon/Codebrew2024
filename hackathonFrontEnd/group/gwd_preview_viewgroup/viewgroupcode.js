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

async function view_did_load() {

    console.log("Getting upcoming events")
    let groupinfo = await sendHTTPS("retreiveGroupInfo", body={"groupId":"000001"});
    // !!!!!!!! Will need groupID from cookie


    console.log(groupinfo);


    //Get group interests, display them in table
    let interests = groupinfo.groupInterests;


    //Get group sujects, display them in table
    let subjects = groupinfo.groupInterests;

    //Get group member numbers
    let maxMembers = groupinfo.groupPeopleMax;
    let groupMembers = groupinfo.groupMembers;
    let currCount = groupMembers.length;

    

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
        
        img.style.width = int(100/column).toString() + "%"
        img.style.height = int(100/column).toString() + "%"
        c.appendChild(img);
        
    }
}

