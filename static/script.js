// Enhanced JavaScript for dark theme animations
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dark theme JavaScript loaded!');
    
    // Add staggered animations to tables
    const tables = document.querySelectorAll('table');
    tables.forEach((table, index) => {
        table.style.opacity = '0';
        table.style.transform = 'translateY(30px) scale(0.95)';
        table.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        
        setTimeout(() => {
            table.style.opacity = '1';
            table.style.transform = 'translateY(0) scale(1)';
        }, index * 200);
    });

    // Enhanced form animations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
                
                // Revert after 3 seconds (for demo)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });

    // Enhanced card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.transition = 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.5)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.4)';
        });
    });

    // Add color coding to grades
    function colorCodeGrades() {
        const gradeCells = document.querySelectorAll('td:nth-last-child(2)');
        gradeCells.forEach(cell => {
            const gradeText = cell.textContent.trim();
            const grade = parseFloat(gradeText);
            
            if (!isNaN(grade)) {
                cell.classList.remove('grade-A', 'grade-B', 'grade-C', 'grade-D', 'grade-F');
                
                if (grade >= 90) cell.classList.add('grade-A');
                else if (grade >= 80) cell.classList.add('grade-B');
                else if (grade >= 70) cell.classList.add('grade-C');
                else if (grade >= 60) cell.classList.add('grade-D');
                else cell.classList.add('grade-F');
                
                // Add animation to grade cells
                cell.style.opacity = '0';
                cell.style.transform = 'translateX(-20px)';
                cell.style.transition = 'all 0.6s ease';
                
                setTimeout(() => {
                    cell.style.opacity = '1';
                    cell.style.transform = 'translateX(0)';
                }, 300);
            }
        });
    }
    
    // Run grade color coding
    colorCodeGrades();
    
    // Enhanced flash message animations
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach((message, index) => {
        message.style.opacity = '0';
        message.style.transform = 'translateX(-50px)';
        message.style.transition = 'all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        
        setTimeout(() => {
            message.style.opacity = '1';
            message.style.transform = 'translateX(0)';
        }, index * 200);
        
        // Auto-dismiss flash messages
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(50px)';
            setTimeout(() => {
                if (message.parentElement) {
                    message.parentElement.removeChild(message);
                }
            }, 600);
        }, 5000);
    });

    // Add floating animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((btn, index) => {
        setTimeout(() => {
            btn.classList.add('float');
        }, index * 100);
    });

    // Add typing animation to page titles
    const pageTitles = document.querySelectorAll('h2');
    pageTitles.forEach(title => {
        const text = title.textContent;
        title.textContent = '';
        
        let i = 0;
        const typeWriter = setInterval(() => {
            if (i < text.length) {
                title.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeWriter);
            }
        }, 50);
    });

    // Add parallax effect to background
    document.addEventListener('mousemove', function(e) {
        const moveX = (e.clientX - window.innerWidth / 2) / 25;
        const moveY = (e.clientY - window.innerHeight / 2) / 25;
        
        document.body.style.backgroundPosition = `${moveX}px ${moveY}px`;
    });

    // Add ripple effect to buttons
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add CSS for ripple effect
    const rippleStyle = document.createElement('style');
    rippleStyle.innerHTML = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
        }
        
        @keyframes ripple {
            to {
                transform: scale(2.5);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
});