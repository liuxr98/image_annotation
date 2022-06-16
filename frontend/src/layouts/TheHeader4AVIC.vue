<template>
  <div class="header-heading">
    <div class="header-left">
      <img src="~@/assets/avic-logo.jpg" class="logo"/>
      <span>
        图像标注平台
      </span>
    </div>
    <div class="ctrl-wrapper">
      <div class="user-info">
        <template v-if="isLoggedIn">
          <el-avatar>
            {{loggedUser}}
          </el-avatar>
          <span class="user-name">
            {{loggedUser}}
          </span>
          <el-divider direction="vertical"/>
          <el-button type="text" @click="handleLogout" style="color: white">
            登出
          </el-button>
        </template>
        <template v-else>
          <el-button type="text" @click="handleLogin" style="color: white">
            登录
          </el-button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "TheHeader4AVIC",
  computed:{
    isLoggedIn(){
      return !!this.loggedUser
    },
    ...mapState('auth', {
      loggedUser: 'loggedUser'
    })
  },
  methods:{
    handleLogout(){
      localStorage.removeItem('accessToken')
      this.$store.commit('auth/setLoggedUser', '')
      this.$router.push('/login')
    },
    handleLogin(){
      this.$router.push({name: 'login', query: {redirect: this.$route.path}})
    }
  },
  created() {
    this.$store.dispatch('auth/getLoggerUser')
  },
}
</script>

<style scoped lang="less">
.header-heading{
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
}
.header-left{
  display: flex;
  align-items: center;
  cursor: pointer;
  color: white;
}
.logo{
  margin-right: 10px;
  height: 70%;
}
.ctrl-wrapper{
  margin-left: auto;
  align-items: center;
  display: flex;
}
.user-info{
  color: white;
  display: flex;
  align-items: center;
}
.user-name{
  font-size: 14px;
  margin-left: 10px;
  max-width: 70px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>