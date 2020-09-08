const quizData = [{
        question: 'What is the programming laguage used for Ethereum?',
        a: 'Java',
        b: 'Solidity',
        c: 'Bitcoin',
        d: 'Ether',
        correct: 'b'
    },
    {
        question: 'What is the most popular programming laguage?',
        a: 'Java',
        b: 'C',
        c: 'Python',
        d: 'JavaScript',
        correct: 'd'
    },
    {
        question: 'What does the word "Fiat" mean?',
        a: 'Let it be',
        b: 'Decree',
        c: 'Car',
        d: 'Punto',
        correct: 'b'
    },
    {
        question: 'What is the name of the founder of Bitcoin?',
        a: 'Coin, Bit',
        b: 'Satoshi Nakamoto',
        c: 'Bill Gates',
        d: 'Donald Trump',
        correct: 'b'
    },
    {
        question: 'Who is the man?',
        a: 'Me',
        b: 'You',
        c: 'Him',
        d: 'Them',
        correct: 'a'
    }
]

const answerEls = document.querySelectorAll(".answer");

const questionEl = document.getElementById("question");
const quiz = document.getElementById("quiz");

const a_text = document.getElementById("a_text");
const b_text = document.getElementById("b_text");
const c_text = document.getElementById("c_text");
const d_text = document.getElementById("d_text");

const submitBtn = document.getElementById("submit")

let currentQuiz = 0;
let score = 0;

loadQuiz();

function loadQuiz() {
    deselectAnswers();

    const currentQuizData = quizData[currentQuiz];

    questionEl.innerHTML = currentQuizData.question;

    a_text.innerHTML = currentQuizData.a;
    b_text.innerHTML = currentQuizData.b;
    c_text.innerHTML = currentQuizData.c;
    d_text.innerHTML = currentQuizData.d;
}

function getSelected() {


    let answer = undefined;

    answerEls.forEach((answerEl) => {
        if (answerEl.checked) {
            answer = answerEl.id;
        }
    });

    return answer;
}

function deselectAnswers() {
    answerEls.forEach((answerEl) => {
        answerEl.checked = false;
    })
}

submitBtn.addEventListener("click", () => {

    if (submitBtn.innerHTML === 'Restart') {
        location.reload();
    }

    const answer = getSelected();

    if (answer) {
        if (answer === quizData[currentQuiz].correct) {
            score++;
            console.log(score)
        }
        currentQuiz++;
        if (currentQuiz < quizData.length) {
            loadQuiz();
        } else {
            quiz.innerHTML = `<h2> You Scored: ${score}/${quizData.length} </h2>`
            submitBtn.innerHTML = `Restart`
        }
    }
});