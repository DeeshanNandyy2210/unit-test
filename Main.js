document.addEventListener('DOMContentLoaded', () => {
            const tabs = document.querySelectorAll('.tab-button');
            const sections = document.querySelectorAll('.content-section');
            const codeBlocks = document.querySelectorAll('.interactive-code');

            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const target = tab.dataset.tab;
                    
                    tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    
                    sections.forEach(section => {
                        if (section.id === `${target}-content`) {
                            section.classList.add('active');
                        } else {
                            section.classList.remove('active');
                        }
                    });
                });
            });

            codeBlocks.forEach(block => {
                const runButton = block.querySelector('.run-button');
                const outputConsole = block.querySelector('.output-console');
                const outputText = outputConsole.dataset.output;

                runButton.addEventListener('click', () => {
                    outputConsole.textContent = 'Running...\n';
                    setTimeout(() => {
                        outputConsole.textContent = outputText;
                    }, 300);
                });
            });

            const quizData = [
                {
                    question: "What keyword is used to define a function in Python?",
                    options: ["func", "def", "function", "define"],
                    answer: "def"
                },
                {
                    question: "A variable created inside a function is said to have what kind of scope?",
                    options: ["Global", "Universal", "Local", "External"],
                    answer: "Local"
                },
                {
                    question: "What will a function return if it has no `return` statement?",
                    options: ["0", "An error", "False", "None"],
                    answer: "None"
                },
                {
                    question: "Which syntax correctly defines a parameter with a default value?",
                    options: ["def func(param = 10):", "def func(param: 10):", "def func(param is 10):", "def func(param == 10):"],
                    answer: "def func(param = 10):"
                },
                {
                    question: "What is the term for a function that calls itself?",
                    options: ["A loop", "An iteration", "A generator", "A recursive function"],
                    answer: "A recursive function"
                }
            ];

            const quizContainer = document.getElementById('quiz-container');
            const submitButton = document.getElementById('submit-quiz');
            const resultsContainer = document.getElementById('quiz-results');

            function buildQuiz() {
                quizData.forEach((q, index) => {
                    const questionDiv = document.createElement('div');
                    questionDiv.classList.add('quiz-question');
                    
                    const questionText = document.createElement('p');
                    questionText.classList.add('font-semibold', 'text-lg', 'mb-3');
                    questionText.textContent = `${index + 1}. ${q.question}`;
                    questionDiv.appendChild(questionText);
                    
                    const optionsDiv = document.createElement('div');
                    optionsDiv.classList.add('space-y-2');
                    
                    q.options.forEach(option => {
                        const label = document.createElement('label');
                        label.classList.add('block', 'p-3', 'border', 'rounded-lg', 'cursor-pointer', 'quiz-option');

                        const input = document.createElement('input');
                        input.type = 'radio';
                        input.name = `question${index}`;
                        input.value = option;
                        input.classList.add('mr-3');
                        
                        label.appendChild(input);
                        label.appendChild(document.createTextNode(option));
                        optionsDiv.appendChild(label);
                    });
                    
                    questionDiv.appendChild(optionsDiv);
                    quizContainer.appendChild(questionDiv);
                });
            }

            function showResults() {
                let score = 0;
                const questionDivs = quizContainer.querySelectorAll('.quiz-question');

                questionDivs.forEach((qDiv, index) => {
                    const selected = qDiv.querySelector(`input[name="question${index}"]:checked`);
                    const labels = qDiv.querySelectorAll('label');
                    const correctAnswer = quizData[index].answer;
                    
                    labels.forEach(label => {
                        const input = label.querySelector('input');
                        if(input.value === correctAnswer){
                            label.classList.add('correct');
                        }
                    });

                    if (selected) {
                        if (selected.value === correctAnswer) {
                            score++;
                        } else {
                            selected.parentElement.classList.add('incorrect');
                        }
                    }
                });

                resultsContainer.textContent = `You scored ${score} out of ${quizData.length}!`;
                resultsContainer.classList.remove('hidden');
                submitButton.disabled = true;
                submitButton.style.opacity = '0.5';
            }

            submitButton.addEventListener('click', showResults);
            
            buildQuiz();
        });