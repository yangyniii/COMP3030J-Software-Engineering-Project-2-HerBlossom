// js for change the signin button to profile in the upper bar
document.addEventListener('DOMContentLoaded', function() {
    const authButton = document.getElementById('auth-button');

    // 检查登录状态
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            console.log("Received login data:", data);  // 用于检测收到的用户数据
            if (data.is_logged_in) {
                // 用户已登录
                authButton.textContent = 'Profile';
                authButton.href = '/profile';
                authButton.classList.remove('nav_btn');
                authButton.classList.add('nav_btn');
            } else {
                // 用户未登录
                authButton.textContent = 'Sign In';
                authButton.href = '/signin';
                authButton.classList.remove('nav_btn');
                authButton.classList.add('nav_btn');
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
            // 发生错误时默认显示登录链接
            authButton.textContent = 'Sign In';
            authButton.href = '/signin';
            authButton.classList.remove('nav_btn');
            authButton.classList.add('nav_btn');
        });
    });