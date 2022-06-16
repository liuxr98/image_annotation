<template>
  <el-container class="container">
    <el-header class="header">
      <TheHeader/>
<!--      <TheHeader4AVIC/>-->
    </el-header>
    <router-view/>
  </el-container>
</template>

<script>
import TheHeader from "@/layouts/TheHeader";
// import TheHeader4AVIC from "@/layouts/TheHeader4AVIC";

export default {
  name: "TheContainer",
  components:{
    // TheHeader4AVIC,
    TheHeader,
  }
}
</script>

<style scoped lang="less">
.container{
  height: 100%;
  width: 100%;
}
.header{
  //background: dodgerblue;
  box-shadow: 0 1px 1px 0 rgb(0 0 0 / 15%);
  z-index: 1;
}
</style>