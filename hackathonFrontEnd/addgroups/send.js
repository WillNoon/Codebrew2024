// Data to be sent to the Flask server

const path = "https://64797083-dd51-442c-a36f-84a92c6265df-00-30ipml1u64wqw.worf.replit.dev/"

async function sendHTTPS(extension, body={"key":"val"}, method="POST") {
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

async function retrievegroups(){
        const searchbar = document.getElementById('searchBar');
        const chxHideFull = document.getElementById("chxHideFull");
        let searchText = '';
        let hideFullBool = false
        if(searchbar == null){searchText = ''}
        else{searchText = searchbar.value}
        if (chxHideFull == null){hideFullBool = false}
        else{hideFullBool = chxHideFull.checked}
        var params = new URLSearchParams(window.location.search);
            // Retrieve data parameter
    
         userId = params.get('userId');
            // Display data on the page
        if (!userId) {
            userId = "000001";
        }
        console.log(userId);

        const groups = await sendHTTPS('getFeed', body = {"userID": userId, "searchInput": searchText, "hideFull": hideFullBool});
        const container = document.getElementById('container');
        container.innerHTML = '';
        groups.forEach(group => {
            const tile = document.createElement("div");
            tile.classList.add('group-tile');
            tile.id = group.groupId;
            const name = document.createElement('h2');
            name.textContent = group.groupName;
            name.classList.add("groupName");
            tile.appendChild(name);
            const members = document.createElement("h2");
            members.classList.add("groupMembers");
            members.textContent = String(group.groupMembers.length) + "/" + String(group.groupMax);
            tile.appendChild(members);
            const desc = document.createElement('p');
            desc.textContent = group.groupDesc;
            desc.classList.add("groupDesc");
            tile.appendChild(desc);
            const interests = document.createElement("div")
            interests.classList.add("groupInterests");
            group.groupInterests.forEach(interest => {
                const interestTile = document.createElement("span");
                interestTile.textContent = interest;
                interestTile.classList.add("interestTile");
                interests.appendChild(interestTile);
            })
            tile.appendChild(interests);
            const subjects = document.createElement("div")
            subjects.classList.add("groupSubjects");
            group.groupSubjects.forEach(subject => {
                const subjectTile = document.createElement("span");
                subjectTile.textContent = subject;
                subjectTile.classList.add("subjectTile");
                subjects.appendChild(subjectTile);
            })
            tile.appendChild(subjects);

            container.appendChild(tile);
        })
}