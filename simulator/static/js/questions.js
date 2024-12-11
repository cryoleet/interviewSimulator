
const questionsDataTag = document.getElementById('questions-data');
const questions = JSON.parse(questionsDataTag.textContent);
let currentIndex = 0;

const questionBox = document.getElementById('current-question');
const answerBtn = document.getElementById('answer-btn');
const skipBtn = document.getElementById('skip-btn');
const completeBtn = document.getElementById('complete-btn');


function displayQuestion() {
    if (currentIndex < questions.length) {
        questionBox.textContent = questions[currentIndex];
    } else {
        questionBox.textContent = "You have answered all the questions!";
        answerBtn.classList.add('d-none');
        skipBtn.classList.add('d-none');
        completeBtn.classList.remove('d-none');
    }
}

answerBtn.addEventListener('click', function () {

    // TODO: remove this alert and add logic for recording audio
    alert(`Answering question ${currentIndex + 1}: ${questions[currentIndex]}`);
    currentIndex++;
    displayQuestion();
});


skipBtn.addEventListener('click', function () {
    alert(`Skipping question ${currentIndex + 1}: ${questions[currentIndex]}`);
    currentIndex++;
    displayQuestion();
});


completeBtn.addEventListener('click', function () {
    alert("Interview Completed!");
    // TODO: redirect to feedback page (for now redirect to a placeholder view, make sure you pass the recorded audio for all questions)
});


displayQuestion();
