console.log('hello world')
//page responsible for home page

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const url = window.location.href
const logout = document.getElementById('logout')
const usernameBox = document.getElementById('user-name')
const username = 

logout.innerHTML += `<button type="button" class="btn btn-primary">Logout</button>`

logout.addEventListener('click',()=>{

    window.location.href = url+'logout/'
})
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const topic = modalBtn.getAttribute('data-topic')
    const numQuestions = modalBtn.getAttribute('data-question')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')





    modalBody.innerHTML =` 
    <div class = "h5 mb-3"> Ready to begin "<b>${name}</b>"? </div>
    <div class = "text-muted"> 
    <ul> 
        <li> Topic: <b> ${topic} </b> </li>
        <li> Difficulty: <b> ${difficulty} </b> </li>
        <li> Number of Questions: <b> ${numQuestions} </b> </li> 
        <li> Minimum marks required: <b> ${scoreToPass} </b> </li> 
        <li> Time: <b> ${time} </b> minutes </li>
    </ul> 
    </div>
    `
startBtn.addEventListener('click',()=>{
    console.log(window.location.href = url+pk)
})


}))