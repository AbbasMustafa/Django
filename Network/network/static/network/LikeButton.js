
// Like Button Function
////////////////////////////////
    	function send_data(id){
    		const url = `/likes?id=${id}`
    		fetch(url)
    		.then(response => response.text())
    		.then((data) =>{
    			const count = data.match(/\d+/g);
				const letr =  data.match(/[a-zA-Z]+/g);

    			document.getElementById(`${id}count`).innerHTML = count;
    			document.getElementById(`${id}like`).innerHTML = letr;
    			if(letr.toString().localeCompare("Liked") === 0){
    				document.getElementById(`${id}div`).style.background = "#a4a4a4";
    			}else{
    				document.getElementById(`${id}div`).style.background = "#FFF";
    			}
    		})
    	}

    	function like(id){
    		send_data(parseInt(id,10));
    	}
///////////////////////////////////
///////////////////////////////////


// Follow Button
function send_follow(id) {

    let url = `/follow?id=${id}`;
    fetch(url)
    .then(response => response.json())
    .then(count=>{
        document.getElementById('follower').innerHTML = count.lenFollowers;
        document.getElementById('following').innerHTML = count.lenFollowing;
        document.getElementById(`${id}`).innerHTML = count.textFollow;
    }) 
}

function follow(id){
    send_follow(id)
}

//////////////////////////////


// edit Button
document.addEventListener('click', (event) => {
    const name = event.target.className;
    const id = event.target.id;

    // Post Edit
    ///////////////
    if(event.target.className.substring(0,3).localeCompare('abc') === 0){
            editPost(id)
    }

    // Cencel Edit Buton
    ///////////////////////////////////////
    if(event.target.className.substring(0,3).localeCompare('cls') === 0){
            document.querySelector('.black').style.display = "none";
            document.querySelector(`.p${id}`).style.display = "block";
            document.querySelector(`.p${id}`).parentNode.style.zIndex = 9;
            document.querySelector('.formDiv').remove();
    }

    if(name.substring(0,8).localeCompare('editPost') === 0){

        const parent = event.target.parentNode;
        const value = parent.childNodes[9].innerHTML;
        const formdiv = document.createElement("div");
        formdiv.classList.add("formDiv");
        formdiv.innerHTML = `<h4 class="display-4 small font-weight-bold">Post Editing</h4>
                            <form id="editForm">
                            <textarea class="editText" id="id_post" cols=60 rows=3>${value}</textarea>
                            <input type="submit" value="Post" id="${id}" style="width:150px; box-shadow:2px 2px 2px black;" class="abc btn btn-primary mt-1 mb-1">
                            <a id="${id}" class="cls btn btn-secondary" style="width:150px; color:white; box-shadow:2px 2px 2px black;">Close</a>
                            </form>`;
        parent.parentNode.append(formdiv);
        parent.parentNode.style.zIndex = 999;
        document.querySelector(".black").style.display = "block";
        document.querySelector(`.p${id}`).style.display = "none";
    }

    
})

// Post Eidt Logic
//////////////////////////////////////
function editPost(id){
    document.getElementById("editForm").onsubmit = (event)=>{

    value = document.querySelector(".editText").value
            
    const url = "/edit";
    fetch(url,{
        method:"POST",
        body:JSON.stringify({
        value:value,
        id:id,
        })
    })
    .then(response => response.text())
    .then(data=>{
        document.querySelector(".black").style.display = "none";
        document.querySelector(`.p${id}`).style.display = "block";
        document.querySelector(`#text${id}`).innerHTML = value;
        document.querySelector(`.p${id}`).parentNode.style.zIndex = 9;
        document.querySelector('.formDiv').remove()
    })
            
    event.preventDefault();
    }
}

///////////////////////////////////////////

document.getElementById('addPost').onclick = (event) => {
    document.querySelector('.newPost').style.display = "block";
    document.getElementById('addPost').style.display = "none";
}