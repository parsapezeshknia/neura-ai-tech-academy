const completed = new Set(JSON.parse(localStorage.getItem("neuraCompleted") || "[]"));
const lessonIds = ["ai-basics","machine-learning","neural-networks","large-language-models","prompt-engineering","responsible-ai"];
let activeLesson = null;

function updateProgress(){
  const count = completed.size;
  const percent = Math.round(count / lessonIds.length * 100);
  document.getElementById("completed-count").textContent = count;
  document.getElementById("ring-number").textContent = percent + "%";
  document.querySelector(".progress-ring").style.background = `conic-gradient(#a78bfa ${percent*3.6}deg,#292c3d 0deg)`;
  lessonIds.forEach(id => {
    const card = document.querySelector(`[data-lesson="${id}"]`);
    const label = document.getElementById(`done-${id}`);
    if(card) card.classList.toggle("is-complete", completed.has(id));
    if(label) label.style.display = completed.has(id) ? "block" : "none";
  });
}
updateProgress();

document.querySelectorAll("[data-open-lesson]").forEach(button => {
  button.addEventListener("click", () => openLesson(button.dataset.openLesson));
});
async function openLesson(id){
  try{
    const response = await fetch(`/api/lesson/${id}`);
    if(!response.ok) throw new Error("Could not load lesson");
    const lesson = await response.json();
    activeLesson = id;
    document.getElementById("modal-category").textContent = lesson.category;
    document.getElementById("modal-number").textContent = `${lesson.number} / 06`;
    document.getElementById("modal-title").textContent = lesson.title;
    document.getElementById("modal-description").textContent = lesson.description;
    document.getElementById("modal-content").innerHTML = lesson.content.map(item =>
      `<article><h3>${escapeHtml(item[0])}</h3><p>${escapeHtml(item[1])}</p></article>`
    ).join("");
    document.getElementById("modal-takeaway").textContent = lesson.takeaway;
    const completeButton = document.getElementById("complete-lesson");
    completeButton.innerHTML = completed.has(id) ? "Completed ✓" : "Mark as complete <span>✓</span>";
    document.getElementById("lesson-modal").classList.add("open");
    document.getElementById("lesson-modal").setAttribute("aria-hidden","false");
  }catch(error){ alert("Sorry, this lesson could not be loaded. Please try again."); }
}
function escapeHtml(value){
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
function closeModal(){
  document.getElementById("lesson-modal").classList.remove("open");
  document.getElementById("lesson-modal").setAttribute("aria-hidden","true");
}
document.getElementById("modal-close").addEventListener("click",closeModal);
document.getElementById("lesson-modal").addEventListener("click",e=>{if(e.target.id==="lesson-modal")closeModal();});
document.getElementById("complete-lesson").addEventListener("click",()=>{
  if(!activeLesson) return;
  completed.add(activeLesson);
  localStorage.setItem("neuraCompleted",JSON.stringify([...completed]));
  updateProgress();
  document.getElementById("complete-lesson").textContent="Completed ✓";
});

document.querySelectorAll(".nav-link").forEach(link=>{
  link.addEventListener("click",()=>{
    document.querySelectorAll(".nav-link").forEach(item=>item.classList.remove("active"));
    link.classList.add("active");
    document.getElementById("sidebar").classList.remove("open");
  });
});
document.getElementById("mobile-menu").addEventListener("click",()=>document.getElementById("sidebar").classList.toggle("open"));

const chatWindow=document.getElementById("chat-window");
function addMessage(text,kind){
  const div=document.createElement("div");
  div.className=`chat-message ${kind==="user"?"user-message":"bot-message"}`;
  div.textContent=text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop=chatWindow.scrollHeight;
}
async function askAssistant(prompt){
  if(!prompt.trim()) return;
  addMessage(prompt,"user");
  try{
    const response=await fetch("/api/assistant",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt})});
    const data=await response.json();
    if(!response.ok) throw new Error(data.error||"Request failed");
    addMessage(data.answer,"bot");
  }catch(error){addMessage("I couldn't process that request. Please try again.","bot");}
}
document.getElementById("assistant-form").addEventListener("submit",e=>{
  e.preventDefault();
  const input=document.getElementById("assistant-input");
  const value=input.value.trim();
  if(value){input.value="";askAssistant(value);}
});
document.querySelectorAll(".suggestion").forEach(button=>button.addEventListener("click",()=>askAssistant(button.textContent)));

let quizQuestions=[],quizAnswers=[],quizIndex=0,quizLocked=false;
const quizContent=document.getElementById("quiz-content");
document.getElementById("start-quiz").addEventListener("click",startQuiz);
async function startQuiz(){
  try{
    const response=await fetch("/api/quiz");
    const data=await response.json();
    quizQuestions=data.questions;quizAnswers=[];quizIndex=0;quizLocked=false;
    renderQuestion();
  }catch(error){quizContent.innerHTML="<p>Could not load the quiz. Please refresh and try again.</p>";}
}
function renderQuestion(){
  const q=quizQuestions[quizIndex];
  document.getElementById("quiz-progress-label").textContent=`QUESTION ${quizIndex+1} OF ${quizQuestions.length}`;
  quizContent.innerHTML=`<div class="quiz-question">${quizIndex+1}. ${escapeHtml(q.question)}</div><div class="quiz-options">${q.options.map((option,index)=>`<button class="quiz-option" data-option="${index}">${String.fromCharCode(65+index)}. ${escapeHtml(option)}</button>`).join("")}</div><div id="quiz-feedback"></div>`;
  quizContent.querySelectorAll(".quiz-option").forEach(button=>button.addEventListener("click",()=>selectAnswer(Number(button.dataset.option))));
  quizLocked=false;
}
async function selectAnswer(index){
  if(quizLocked)return;
  quizLocked=true;quizAnswers[quizIndex]=index;
  const buttons=[...quizContent.querySelectorAll(".quiz-option")];
  buttons.forEach(button=>{button.disabled=true;if(Number(button.dataset.option)===index)button.classList.add("selected");});
  if(quizIndex===quizQuestions.length-1){
    await showFinalResult();
    return;
  }
  const feedback=document.getElementById("quiz-feedback");
  feedback.innerHTML=`<button class="button button-primary quiz-next" id="next-question">Next question <span>→</span></button>`;
  document.getElementById("next-question").addEventListener("click",()=>{quizIndex++;renderQuestion();});
}
async function showFinalResult(){
  const response=await fetch("/api/quiz/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answers:quizAnswers})});
  const result=await response.json();
  const detail=result.results.map((item,index)=>`<div class="quiz-feedback ${item.correct?"good":"bad"}">${item.correct?"Correct":"Review"} · Q${index+1}: ${escapeHtml(item.explanation)}</div>`).join("");
  document.getElementById("quiz-progress-label").textContent="COMPLETED";
  quizContent.innerHTML=`<div class="quiz-result">${result.score} / ${result.total}</div><h3>${result.percentage>=80?"Excellent work!":result.percentage>=60?"Good progress!":"Keep exploring!"}</h3><p>You scored ${result.percentage}%. Review the explanations below to strengthen your understanding.</p>${detail}<button class="button button-primary quiz-next" id="retry-quiz">Try again ↻</button>`;
  document.getElementById("retry-quiz").addEventListener("click",startQuiz);
}
