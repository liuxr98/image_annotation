<template>
  <div class="content">
   <el-card class="wrapper-card" >
      <el-tabs
          :active-name="$route.path.split('/')[1]"
          @tab-click="handleClick"
          type="card"
      >
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" ref="login-form" label-width="80px" :rules="loginFormRules">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" :maxlength="30"/>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="loginForm.password" :show-password="true"/>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleLogin">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="signup">
          <el-form :model="signupForm" ref="signup-form" label-width="80px" :rules="signupFormRules">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="signupForm.username" :maxlength="30"/>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="signupForm.password" :show-password="true"/>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPassword">
              <el-input type="password" v-model="signupForm.checkPassword" :show-password="true"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSignup">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
   </el-card>
  </div>
</template>

<script>
export default {
  name: "LoginOrSignupView",
  data(){
    let checkPasswordValidator = (rule, value, callback) =>{
      if(!value) {
        callback(new Error('请再次输入密码'))
      }else if(value !== this.signupForm.password){
        callback(new Error('两次输入的密码不一致'))
      }else{
        callback()
      }
    }
    return {
      activeName: '',
      loginForm: {
        username: '',
        password: ''
      },
      loginFormRules:{
        username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}]
      },
      signupForm:{
        username: '',
        password: '',
        checkPassword: ''
      },
      signupFormRules: {
        username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}],
        checkPassword:  [
          {validator: checkPasswordValidator, trigger: 'blur'},
          {required: true, message: '请输入密码', trigger: 'blur'}
        ],
      }
    }
  },
  methods:{
    handleClick(tab) {
      this.$router.push(tab.name)
    },
    handleLogin(){
      this.$refs["login-form"].validate((validate)=>{
        if(validate){
          this.$http.post('users/login',{
            username: this.loginForm.username,
            password: this.loginForm.password
          }).then(response=>{
            localStorage.setItem('accessToken', response.data['access_token'])
            this.$store.commit('auth/setLoggedUser', response.data['logged_user'])
            this.$router.push(this.$route.query.redirect ? this.$route.query.redirect : '/')
          }).catch(err=>{
            let message = err.response.data['message']
            if(message === 'UserNotExist'){
              this.$message.error('用户不存在')
            }else if(message === 'PasswordIncorrect'){
              this.$message.error('密码错误')
            }else{
              this.$message.error('登录错误')
            }
          })
        }
      })
    },
    handleSignup(){
      this.$refs["signup-form"].validate((validate)=>{
        if(validate){
          this.$http.post('/users/register', {
            username: this.signupForm.username,
            password: this.signupForm.password
          }).then(response =>{
            if(response.data.message === 'Success'){
              this.$message.success('注册成功')
              this.$router.push('login')
              this.resetSignupForm()
            }
          }).catch( err =>{
            if(err.response.data.message === 'UsernameDuplicate'){
              this.$message.error('用户名重复，请修改')
            }else{
              this.$message.error('注册错误，请重新注册')
            }
          })
        }
      })
    },
    resetSignupForm(){
      this.$refs["signup-form"].resetFields()
      this.signupForm = {
        username: '',
        password: '',
        checkPassword: ''
      }
    }
  }

}
</script>

<style scoped>
.content{
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.wrapper-card{
  width: 400px;
  margin-bottom: 25%;
}
</style>