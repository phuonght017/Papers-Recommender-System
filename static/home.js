const form = document.querySelector('#recommendations-form')
const recommendationsDiv = document.querySelector('#recommendations')
const interestingsDiv = document.querySelector('#interestings')
const errorDiv = document.querySelector('#error')

form.addEventListener('submit', async (event) => {
    event.preventDefault()
    const user_id = document.querySelector('#user_id').value
    try {
        const response = await fetch(`/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `user_id=${user_id}`
        })
        
        if (!response.ok) {
            if (response.status == 404) {
                throw new Error('User not found');
            } else {
                throw new Error('Unexpected error');
            }
        }
        const data  = await response.json()
        const interesting_papers = JSON.parse(data.interestings)
        const recommendation_papers = JSON.parse(data.recommendations)

        // Edit error div
        errorDiv.innerHTML = ''

        // Edit interesting div
        interestingsDiv.innerHTML = ''
        if (interesting_papers.length === 0) {
            const mess = document.createElement('h1')
            mess.className = "error-msg"
            mess.innerHTML = 'No interested paper found.'
            interestingsDiv.appendChild(mess)
        } else {
            // Add headline
            const intHead = document.createElement('h1')
            intHead.className = "headline"
            var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-right-square" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm4.5 5.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/></svg>'
            intHead.innerHTML = svg + "  RECENTLY INTERESTED IN" + "<hr>"
            interestingsDiv.appendChild(intHead)
            // Add cards
            const cards = document.createElement('div')
            cards.className = "card-list"
            interesting_papers.forEach((paper, index) => {
                // Create card
                const interestingDiv = document.createElement('div')
                interestingDiv.className = "card"
                // Add image
                const img = document.createElement('img');
                img.className = "card-image"
                img.src = `../static/images/posters/poster (${index}).jpg`;
                img.alt = 'poster';
                interestingDiv.appendChild(img)
                // Add title
                const title = document.createElement('div')
                title.className = "card-header"
                title.innerHTML = `<a href="/papers/${paper.id}"> ${paper.title} </a>`
                interestingDiv.appendChild(title)
                // Add footer - published_year
                const footer = document.createElement('div')
                footer.className ="card-footer"
                footer.innerHTML = `<div class="card-meta"> -- ${paper.published_year} -- </div>`
                interestingDiv.appendChild(footer)
                cards.appendChild(interestingDiv)
            })
            interestingsDiv.appendChild(cards)
        }
    
        // Edit recommendations div
        recommendationsDiv.innerHTML = ''
        if (recommendation_papers.length === 0) {
            const mess = document.createElement('h1')
            mess.className = "error-msg"
            mess.innerHTML = 'No recommendations found.'
            recommendationsDiv.appendChild(mess)
        } else {
            // Add headline 
            const recHead = document.createElement('h1')
            recHead.className = "headline"
            var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-right-square" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm4.5 5.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/></svg>'
            recHead.innerHTML = svg + "  RECOMMENDED FOR YOU" + "<hr>"
            recommendationsDiv.appendChild(recHead)
            // Add cards      
            const cards = document.createElement('div')
            cards.className = "card-list"
            recommendation_papers.forEach((paper, index) => {
                // Create card
                const recommendationDiv = document.createElement('div')
                recommendationDiv.className = "card"
                // Add image
                const img = document.createElement('img');
                img.className = "card-image"
                img.src = `../static/images/posters/poster (${index}).jpg`;
                img.alt = 'poster';
                recommendationDiv.appendChild(img)
                // Add title
                const title = document.createElement('div')
                title.className = "card-header"
                title.innerHTML = `<a href="/papers/${paper.id}"> ${paper.title} </a>`
                recommendationDiv.appendChild(title)
                // Add footer - published_year
                const footer = document.createElement('div')
                footer.className ="card-footer"
                footer.innerHTML = `<div class="card-meta"> -- ${paper.published_year} -- </div>`
                recommendationDiv.appendChild(footer)
                cards.appendChild(recommendationDiv)
            })
            recommendationsDiv.appendChild(cards)
        }
    } catch (error) {
        console.error('Error:', error);
        interestingsDiv.innerHTML = ''
        recommendationsDiv.innerHTML = ''
        errorDiv.innerHTML = ''
        const mess = document.createElement('h1')
        mess.className = "headline"
        mess.innerHTML = 'Error: ' + error.message
        errorDiv.appendChild(mess)
    }  
})
