<template>
  <el-container>
    <el-aside class="aside" >
      <TheSidebar/>
    </el-aside>
    <el-main>
      <router-view/>
    </el-main>
  </el-container>
</template>

<script>
import TheSidebar from "@/layouts/TheSidebar";
export default {
  name: "TheContent",
  components:{
    TheSidebar
  }
}
</script>

<style scoped lang="less">
.aside{
  width: 25%;
  height: 100%;
  .menu{
    height: 100%;
    el-menu-item{
      padding-left: 30px;
    }
  }
}
</style>