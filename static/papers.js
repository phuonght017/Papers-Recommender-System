const form = document.querySelector('#paper-filter-form')
const papersListDiv = document.querySelector('#papersList')
var pageNum = 1
const papersPerPage = 30
var papersList = window.papers
var maxPageNum = Math.ceil(papersList.length / papersPerPage)

// Helper function
function displayPapers(papers, pageNum) {
    const begin = papersPerPage * (pageNum - 1)
    const end = begin + papersPerPage - 1 < papers.length - 1 ? begin + papersPerPage - 1 : papers.length - 1
    const slicedPapers = papers.slice(begin, end + 1)
    papersListDiv.innerHTML = ''
    slicedPapers.forEach((paper, index) => {
        // Create card
        const card = document.createElement('div')
        card.className = "card"
        // Add image
        const img = document.createElement('img');
        img.className = "card-image"
        img.src = `../static/images/posters/poster (${index % 12}).jpg`
        img.alt = 'poster'
        card.appendChild(img)
        // Add title
        const title = document.createElement('div')
        title.className = "card-header"
        title.innerHTML = `<a href="/papers/${paper.id}"> ${paper.title} </a>`
        card.appendChild(title)
        // Add footer - published year
        const footer = document.createElement('div')
        footer.className ="card-footer"
        footer.innerHTML = `<div class="card-meta"> -- ${paper.published_year} -- </div>`
        card.appendChild(footer)
        papersListDiv.appendChild(card)
    })
}
// Handle filtering button

form.addEventListener('submit', async (event) => {
    event.preventDefault()
    const from_year = document.querySelector('#from_year').value
    const to_year = document.querySelector('#to_year').value 
    const years = {
        'from_year': from_year,
        'to_year': to_year
    }
    const response = await fetch(`/papers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(years)
    }) 

    papersListDiv.innerHTML = ''
    const data = await response.json()
    if (data.length === 0) {
        const mess = document.createElement('h1')
            mess.className = "error-msg"
            mess.innerHTML = 'No paper found in this period.'
            papersListDiv.appendChild(mess)
    } else {
        papersList = data
        maxPageNum = Math.ceil(papersList.length / papersPerPage)
        displayPapers(papersList, 1)
    }
})

// Handle prev-btn and next-btn

const nextBtn = document.getElementById('next-btn')
const prevBtn = document.getElementById('prev-btn')

function checkDisable () {
    if (pageNum == maxPageNum) {
        nextBtn.disabled = true
    } else {
        nextBtn.disabled = false
    }

    if (pageNum == 1) {
        prevBtn.disabled = true
    } else {
        prevBtn.disabled = false
    }
}

nextBtn.addEventListener("click", () => {
    pageNum += 1
    checkDisable()
    displayPapers(papersList, pageNum)
    form.scrollIntoView(true);
})

prevBtn.addEventListener("click", () => {
    pageNum -= 1
    checkDisable()
    displayPapers(papersList, pageNum)
    form.scrollIntoView(true);
})
