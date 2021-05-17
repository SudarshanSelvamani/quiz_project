console.log('hi this is quiz')
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
const url = window.location.href
var titleQuiz = document.getElementById('titlequiz')
var reqscoretopass = document.getElementById('reqscoretopass')
const quizBox = document.getElementById('quiz-box')
const timeBox = document.getElementById('time-box')
const resultBox = document.getElementById('result-box')
const nextBtn = document.getElementById('next-btn')
const submitBtn = document.getElementById('submit-btn')
var minutesLabel = document.getElementById("minutes")
var secondsLabel = document.getElementById("seconds")
var valBoolean = null
var totalSeconds = 0
var secondsHolder = 0
var minutesHolder = 0
let index = 0
let resdiv 

setInterval(setTime, 1000)


function setTime() {
// for the timer
  ++totalSeconds;
  secondsHolder = pad(totalSeconds % 60)
  minutesHolder = pad(parseInt(totalSeconds / 60))
  secondsLabel.innerHTML = secondsHolder
  minutesLabel.innerHTML = minutesHolder
}

function pad(val) {
    // for stop at 60 and add it to minutes
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}

function finalResultPage(){
    // page responsible for the final result
    const timerData = {'minutes':minutesHolder,'seconds':secondsHolder}
    // console.log('tmerdata = ',timerData)
    quizBox.classList.add('not-visible')  // hiding all buttons
    submitBtn.classList.add('not-visible')
    timeBox.classList.add('not-visible')
    //  to post timer data
    jQuery.ajax({
        type:'POST',
        url:`${url}result/`,
        data:  {'minutes':minutesHolder,'seconds':secondsHolder},
        headers:{
            "X-CSRFToken": csrftoken
        },
        dataType: 'json',
        success: function(data) { console.log('Yippee! ' + data)
        console.log(data.quizname)
        titleQuiz.innerHTML = `<b>${data.message}</b>`
        titleQuiz.innerHTML += `<div id = "time-box"><button id = "logout" type="button" class="btn btn-primary">Logout</button></div>`
        const logout =  document.getElementById('logout')
        logout.addEventListener('click',()=>{
            window.location.href = '/logout/'
        })
        reqscoretopass.innerHTML = `You got <b>${data.percent}%</b>`
        resultBox.innerHTML = `<ul><li>The score you got is <b>${data.score}</b></li>
                                <li>Time you took is <b>${data.timerData}</b></li></ul>`

        resultBox.innerHTML += `<div><b>Detailed Result</b><hr></div>`

        data.answerSel.forEach(res=> {
        for(const[question,resp] of Object.entries(res)){

            const correctResponse = resp['correct_answer']
            const answerSelected = resp['answered']
            let subResult = ''
            if (correctResponse == answerSelected){ subResult = 'correct.'}
            else{subResult = 'wrong.'}
            resultBox.innerHTML += `<li>For the question <b>${question}</b> the right answer is <b>${correctResponse}</b> your response is <b>${answerSelected}</b>, for which your answer is ${subResult}</li><hr>`

        }})
    },
        error:function(error){
            console.log(':('+error)
        }
    })



}

$.ajax({
    type:'GET',
    url:`${url}data`,
    success:function(response){
        const data = response.data
        setNextQuestion(data,index)
        index++
        nextBtn.addEventListener('click',e =>{
            setNextQuestion(data,index)
            if (data.length > index){
            index++}
            })
    },
    error:function(error){
            console.log(error)
        }})



function setNextQuestion(data,index){
    if(index > 0){
        
        resDiv.remove()
    }
    if(index<data.length-1){
        valBoolean = true
    }else{
        valBoolean = false

    }
    showQuestion(data,index)
    var answerElements = document.getElementsByClassName("ans");
    for (var i = 0; i < answerElements.length; i++) {
        answerElements[i].addEventListener('click',onClickForAnswer)
    
}

}


function onClickForAnswer(){ // what happens when user clicks on an answer, only then nextbutton will appear
    var answerElements = document.getElementsByClassName("ans");
    for (var i = 0; i < answerElements.length; i++) {
        answerElements[i].removeEventListener('click',onClickForAnswer);
        
    }
    
    checkAnswer()
    

    if(valBoolean == true){
        submitBtn.classList.add('not-visible')
    }else{nextBtn.remove()
    submitBtn.classList.remove('not-visible')
    submitBtn.addEventListener('click',()=>{
        
        resDiv.remove()
        finalResultPage()
        
                })
                
        }
    
    nextBtn.classList.remove('not-visible')

}

function showQuestion(data,indexNum){  // to display question one by one
    nextBtn.classList.add('not-visible')
    submitBtn.classList.add('not-visible')
    let stuffInsideData = data[indexNum]
    const keyValue = (stuffInsideData) => Object.entries(stuffInsideData).forEach(([question,answers]) => {
        quizBox.innerHTML =`
            <hr>
            <div class = "mb-2">
            <b>${question}</b>
            </div>`

            answers.forEach(answer=> {
                quizBox.innerHTML += `
                <div>
                <input type = "radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                <label for="${question}">${answer}</label>
                `

            })
            
      })
    
      keyValue(stuffInsideData)

}






const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

function checkAnswer(){ // Evaluate user response.
    const elements = [...document.getElementsByClassName('ans')]
    const data ={}
    data['csrfmiddlewaretoken'] = csrf[0].value,
    elements.forEach(el=>{
        if (el.checked){
            data[el.name]=el.value
        }else{
            if(!data[el.name]){
                data[el.name]=null 
            }
        }
    }
    
    )
     
    $.ajax({
        type:'POST',
        url:`${url}save/`,
        data:data,
        success:function(response){
            const results = response.results

        results.forEach(res=> {
        resDiv = document.createElement("div")
        for (const[question,resp] of Object.entries(res)){

            resDiv.innerHTML += `<b> ${question} </b>`
            const cls = ['container','p-3','text-light','h8']
            resDiv.classList.add(...cls)
            
                const answer = resp['answered']
                const correct = resp['correct_answer']
                console.log(answer,correct)

                if (answer == correct){
                    resDiv.classList.add('bg-success')
                    resDiv.innerHTML += ` Answered: ${answer}`
                }else{
                    resDiv.classList.add('bg-danger')
                    resDiv.innerHTML += ` | Correct answer: ${correct}`
                    resDiv.innerHTML += `| Answered: ${answer}`

                }
           
        }

        resultBox.append(resDiv)})},
    
        error:function(error){
            console.log(error)
        }
    })
    }




