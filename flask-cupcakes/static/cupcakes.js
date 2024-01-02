//Handling API requests via axios

// JSON -> HTML function

function CupcakeHTML(cupcake){
  return `<li id= '${cupcake.id}'>
      ${cupcake.flavor}
      ${cupcake.size}
      ${cupcake.rating}
      <img src='${cupcake.image}'></img>
      <button id="delete">X</button>
    </li>`
}

// API get when page loads
async function showCupcakes(){
  //json get response
  const res = await axios.get('http://127.0.0.1:5000/api/cupcakes')
  // json -> HTML for each { } in cupcakes
  for (let cupcake of res.data.cupcakes){
    let html = $(CupcakeHTML(cupcake))
    $('#cupcakes').append(html)
  }
}
$(showCupcakes)

async function addCupcake(evt) {
  evt.preventDefault();
//json post response
  let res= await axios.post(`http://127.0.0.1:5000/api/cupcakes`, 
                      {'flavor':$("#flavor").val(), 
                        'size': $('#size').val(),
                        'rating': $("#rating").val(),
                        'image' : $("#image").val()
})
 let html = $(CupcakeHTML(res.data.cupcake))
 $('#cupcakes').append(html)
}
//API post upon submit
$('#cupcake_form').on('submit', addCupcake)

// Deletion
$('#cupcakes').on('click', '#delete', async function (evt){
  evt.preventDefault();
  let $li= $(evt.target).closest('li')
  let liID= $li.attr('id')
  //wait for response
  await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${liID}`)

  $li.remove();
})

// Completed getting the stuff on HTML
// Next step, add functions for other API requests






