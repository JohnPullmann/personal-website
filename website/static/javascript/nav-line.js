document.addEventListener('DOMContentLoaded', (event) => {
    const navMenu = document.querySelector('.navigation .nav-menu');

    const activeItem = document.querySelector('.navigation .nav-menu a.active');
    if (activeItem) {
      const rect = activeItem.getBoundingClientRect();
      navMenu.style.setProperty('--top', `${rect.top + rect.height / 2 - (rect.height - 25) / 2}px`, 'important');
      setTimeout(() => {
      navMenu.style.setProperty('--height', `${rect.height - 25}px`, 'important');
      }, 200);
    }
  
    document.querySelectorAll('.navigation .nav-menu a').forEach(item => {
      item.addEventListener('mouseenter', e => {
        const rect = e.target.getBoundingClientRect();
        navMenu.style.setProperty('--top', `${rect.top + rect.height / 2 - (rect.height - 25) / 2}px`, 'important');
        setTimeout(() => {
          navMenu.style.setProperty('--height', `${rect.height - 25}px`, 'important');
        }, 200);
      });
  
      item.addEventListener('mouseleave', e => {
        const activeItem = document.querySelector('.navigation .nav-menu a.active');
        if (activeItem) {
          const rect = activeItem.getBoundingClientRect();
          navMenu.style.setProperty('--top', `${rect.top + rect.height / 2 - (rect.height - 25) / 2}px`, 'important');
          setTimeout(() => {
            navMenu.style.setProperty('--height', `${rect.height - 25}px`, 'important');
          }, 200);
        }
      });
    });
});