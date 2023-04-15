import SmoothScroll from 'smooth-scroll'

const scroll = new SmoothScroll('a[href*="#"]', {
  speed: 5000,
  speedAsDuration: true
})
