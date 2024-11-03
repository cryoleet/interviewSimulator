let topics = []


document.getElementById('topicAddBtn').addEventListener('click', function() {

  const topicInput = document.getElementById('topicInput').value.trim()

  if (!topicInput) {
    return
  }

  topics.push(topicInput)

  const tagTemplate = document.getElementById('tagTemplate');
  const newTag = tagTemplate.content.cloneNode(true);
  newTag.querySelector('span.topicName').textContent = topicInput;

  document.getElementById('tagContainer').appendChild(newTag);

  document.getElementById('topicInput').value = '';
  console.log(topics);
});


function removeTopic(tagElement) {

  let topicName = tagElement.querySelector('.topicName').textContent;
  topics.splice(topics.indexOf(topicName), 1);
  tagElement.remove();
}

