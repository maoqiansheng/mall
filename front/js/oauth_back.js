// 保存
on_submit: function(){
    this.check_pwd();
    this.check_phone();
    this.check_sms_code();

    if(this.error_password == false && this.error_phone == false && this.error_sms_code == false) {
        axios.post(this.host + '/oauth/qq/users/', {
                password: this.password,
                mobile: this.mobile,
                sms_code: this.sms_code,
                access_token: this.access_token
            }, {
                responseType: 'json',
            })
            .then(response => {
                // 记录用户登录状态
                sessionStorage.clear();
                localStorage.clear();
                localStorage.token = response.data.token;
                localStorage.user_id = response.data.user_id;
                localStorage.username = response.data.username;
                location.href = this.get_query_string('state');
            })
            .catch(error=> {
                if (error.response.status == 400) {
                    this.error_sms_code_message = error.response.data.message;
                    this.error_sms_code = true;
                } else {
                    console.log(error.response.data);
                }
            })
    }
}