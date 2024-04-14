new Vue({
    el: '#login-app',
    data: {
        username: '',
         password: '',
         user:{},
        
     },
    methods: {
        loginForm: function() {
            // Example: Post to Django view (adjust URL as needed)
            axios.post('/api/login/', {
                username: this.username,
                password: this.password,
             })
            .then(response => {
                var data=response.data
                this.user= data.user;
                console.log('====================================');
                console.log(this.user);
                console.log('====================================');
                localStorage.setItem('userDetails', JSON.stringify(this.user));

                console.log('====================================');
                        console.log(this.user.role);
                        console.log('====================================');
                switch (this.user.role) {
                    case 1:
                        console.log('====================================');
                        console.log(this.user.role);
                        console.log('====================================');
                        window.location.href = '/vendorhome'; // Adjust the path as needed
                        break;
                    case 2:
                        console.log('====================================');
                        console.log(this.user.role);
                        console.log('====================================');
                        window.location.href = '/clienthome'; // Adjust the path as needed
                        break;
                    default:
                        break;
                }
                
                 // Handle success (e.g., redirect to login)
             })
            .catch(error => {
                console.log(error);
                // Handle error (e.g., display error message)
            });
        }
    }
});
