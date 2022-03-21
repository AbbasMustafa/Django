document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(-1));
  // sent email
  document.querySelector('#compose-form').onsubmit = sent_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

//---------------------------------------------------------------------
function compose_email(id) {
  console.log(id)
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if(id == -1){
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }else{
     fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = email.subject.substring(0,3).localeCompare("Re:") ? `Re: ${email.subject}` : email.subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n`;
    })
  }
}
//-------------------------------------------------------------------
function sent_email() {
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: compose_recipients,
          subject: compose_subject,
          body: compose_body
      })
  })
  .then(response => response.json())
  .then(result => {
          if( typeof result.message !== "undefined" ){
            document.querySelector('.sent_error').style.display = 'none';
            load_mailbox('sent');  
          }else{
            document.querySelector('.sent_error').style.display = 'block';
            document.querySelector('.sent_error').innerHTML = result.error;
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
          
      });
  // load_mailbox('sent');
  return false;
}
//-------------------------------------------------------------------
// Archive logic
function archive_logic(id, flag) {

fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
    archived: !flag
  })
})
.then(email => {
    if(flag == true){
      load_mailbox('inbox');
    }else{
      load_mailbox('archive');
    }
  });
}

//----------------------------------------------------------------------


//-----------------------------------------------------------------------
// Fetch individual Email
function load_email(id, mailbox) {
  document.querySelectorAll(".emailDiv").forEach(emailDiv => {
    emailDiv.style.display = 'none';
  })
  document.querySelector('h3').style.display = 'none';

  // Check if mesg is from sent don't show archive button
  if(mailbox == "sent") {
    display = 'none';
  }else{
    display = "inline-block";
  }

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {

      // archived logic
       if(email.archived == false) {
          archive_text = "Archive";
        }else{
          archive_text = "Un Archive";
        }
        flag = email.archived;
      const divTag = document.createElement('div');
      divTag.setAttribute('class','email_view');
      divTag.innerHTML = `<p><span>From: </span> ${email.sender}</p>
                          <p><span>To: </span> ${email.recipients}</p>
                          <p><span>Subject: </span> ${email.subject}</p>
                          <p><span>Timestamp: </span> ${email.timestamp}</p>
                          <button onclick="compose_email(this.id)" id="${email.id}" class="btn btn-outline-primary mt-2"> Replay </button>
                          <button onclick="archive_logic(this.id, ${flag})" style="display:${display};" id="${email.id}" class="btn btn-outline-secondary mt-2 ml-2"> ${archive_text} </button>
                          <hr>
                          <p>${email.body}</p>`;
      document.querySelector('#emails-view').append(divTag);
  })

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })  
  
}

//------------------------------------------------------------------------
function load_mailbox(mailbox) {

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      emails.forEach(email => email_list(email, mailbox));
      unreadCount();
    })


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

//---------------------------------------------------------------------------
//  Load Email list
function email_list(email, mailbox) {
  
  // Individaul Email div
  const divTag = document.createElement('div');
  divTag.setAttribute('class','border p-2 emailDiv')

  // Read Unread Logic
  if( email.read == true ){
    divTag.classList.add('bg-dark');
    divTag.classList.add('text-white');
  }else{
    divTag.classList.add('bg-white');
    divTag.classList.add('text-dark');
  }

  const senderTag = document.createElement('p');
  senderTag.setAttribute('class','float-left m-0')
  senderTag.innerHTML = email.sender;

  const subjectTag = document.createElement('p');
  subjectTag.setAttribute('class','float-left m-0 pl-5')
  subjectTag.innerHTML = email.subject;

  const timeTag = document.createElement('p');
  timeTag.innerHTML = email.timestamp;
  timeTag.setAttribute('class','float-right m-0');

  const clearFix = document.createElement('div');
  clearFix.setAttribute('class','clearfix');

  divTag.append(senderTag);
  divTag.append(subjectTag);
  divTag.append(timeTag);
  divTag.append(clearFix);

  divTag.addEventListener('click',() => load_email(email.id, mailbox));

  document.querySelector('#emails-view').append(divTag);
}

function unreadCount() {
  count = 0;
  fetch(`/emails/inbox`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails);
      for (var i = 0; i < emails.length; i++) {
        if(emails[i].read == false){
          count++;
        }
      }
      document.querySelector('#unreadCount').innerHTML = count;
    })

    
}