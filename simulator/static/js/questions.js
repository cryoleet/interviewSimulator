document.addEventListener('DOMContentLoaded', function() {
    const questionsDataTag = document.getElementById('questions-data');
    const questions = JSON.parse(questionsDataTag.textContent);
    console.log(questions);
    let currentIndex = 0;

    const questionBox = document.getElementById('current-question');
    const answerBtn = document.getElementById('answer-btn');
    const stopBtn = document.getElementById('stop-btn');
    const skipBtn = document.getElementById('skip-btn');
    const completeBtn = document.getElementById('complete-btn');

    let recorder;
    let audioChunks = [];
    let mediaStream;

    function displayQuestion() {
        if (currentIndex < questions.length) {
            questionBox.textContent = questions[currentIndex];
            answerBtn.classList.remove('d-none');
            stopBtn.classList.add('d-none');
        } else {
            questionBox.textContent = "You have answered all the questions!";
            answerBtn.classList.add('d-none');
            skipBtn.classList.add('d-none');
            stopBtn.classList.add('d-none');
            completeBtn.classList.remove('d-none');
        }
    }

    function startRecording() {
        return new Promise((resolve, reject) => {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    mediaStream = stream;
                    recorder = new MediaRecorder(stream);
                    recorder.start();
                    audioChunks = [];
    
                    recorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };

                    answerBtn.classList.add('d-none');
                    stopBtn.classList.remove('d-none');

                    resolve();
                })
                .catch(error => {
                    reject('Microphone access denied: ' + error);
                });
        });
    }

    function stopRecording() {
        return new Promise((resolve, reject) => {
            if (recorder && recorder.state !== 'inactive') {
                recorder.stop();
                
                recorder.onstop = () => {
                    // Stop all tracks in the media stream
                    if (mediaStream) {
                        mediaStream.getTracks().forEach(track => track.stop());
                    }
    
                    // Create a WAV blob
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    
                    // Upload audio
                    const formData = new FormData();
                    formData.append("audio_file", audioBlob, `question_${currentIndex + 1}.wav`);

                    console.log(formData);
    
                    fetch("/media/audio_uploads/", {
                        method: "POST",
                        body: formData,
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Upload failed');
                        }
                        return response.json();
                    })
                    .then(data => {
                        alert(`Recording for question ${currentIndex + 1} uploaded successfully!`);
                        resolve(audioBlob);
    
                        // Increment the question index and display the next question
                        currentIndex++;
                        displayQuestion();
                    })
                    .catch(error => {
                        console.error("Upload failed!", error);
                        alert(`Failed to upload recording for question ${currentIndex + 1}`);
                        reject(error);
                    });
                };
            } else {
                reject(new Error('No active recording'));
            }
        });
    }
    

    answerBtn.addEventListener('click', async function () {
        try {
            await startRecording();
        } catch (error) {
            alert(error);
        }
    });

    stopBtn.addEventListener('click', async function () {
        try {
            await stopRecording();
        } catch (error) {
            console.error(error);
        }
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
});
