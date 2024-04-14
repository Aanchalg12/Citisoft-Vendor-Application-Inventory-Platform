new Vue({
    el: '#signup-app',
    data: {
        username: '',
        email: '',
        password: '',
        emp_id:'',
        number:'',
        role_id: '0', // Default to Admin
    },
    methods: {
        submitForm: function() {
            // Example: Post to Django view (adjust URL as needed)
            axios.post('/api/signup/', {
                username: this.username,
                email: this.email,
                password: this.password,
                role_id: this.role_id,
                emp_id:this.emp_id,
                number:this.number
            })
            .then(response => {
                console.log(response);
                window.location.href = '/login';
                // Handle success (e.g., redirect to login) 
            })
            .catch(error => {
                console.log(error);
                // Handle error (e.g., display error message)
            });
        }
    }
});
